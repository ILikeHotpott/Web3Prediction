from __future__ import annotations

import logging
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Dict, Optional, Sequence, List

from django.db import IntegrityError, transaction

from ...models import AmmPool, AmmPoolOptionState, Event, Market, MarketOption

logger = logging.getLogger(__name__)

DEFAULT_AMM_MODEL = "lmsr"
DEFAULT_AMM_B = Decimal("10000")
DEFAULT_AMM_FEE_BPS = 0
DEFAULT_COLLATERAL_TOKEN = "USDC"


class AmmSetupError(ValueError):
    """Raised when AMM parameters are invalid or setup invariants are violated."""


class AmmModel(str, Enum):
    LMSR = "lmsr"
    CPMM = "cpmm"


class GroupRule(str, Enum):
    STANDALONE = "standalone"
    EXCLUSIVE = "exclusive"
    INDEPENDENT = "independent"


class OptionSide(str, Enum):
    YES = "yes"
    NO = "no"


@dataclass(frozen=True)
class AmmParams:
    model: str
    b: Decimal
    fee_bps: int
    collateral_token: str


def _to_decimal(value: Any, *, field: str) -> Decimal:
    try:
        d = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise AmmSetupError(f"{field} must be a valid number")
    if not d.is_finite():
        raise AmmSetupError(f"{field} must be finite")
    return d


def normalize_amm_params(
    raw: Optional[Dict[str, Any]] = None, *, defaults: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Merge/validate AMM config coming from API payload.
    Falls back to safe defaults so legacy clients still work.

    Aligns with DB constraints:
      - model in {'lmsr','cpmm'}
      - b > 0
      - fee_bps in [0, 10000]
      - collateral_token non-empty
    """
    merged: Dict[str, Any] = {}
    merged.update(defaults or {})
    merged.update(raw or {})

    # Model
    model_raw = merged.get("model") or DEFAULT_AMM_MODEL
    model = str(model_raw).strip().lower()
    if model not in {m.value for m in AmmModel}:
        raise AmmSetupError(f"amm.model must be one of {[m.value for m in AmmModel]}")

    # Liquidity parameter b
    b_raw = merged.get("b")
    b = DEFAULT_AMM_B if b_raw is None else _to_decimal(b_raw, field="amm.b")
    if b <= 0:
        raise AmmSetupError("amm.b must be positive")

    # Fee (basis points) supports legacy feeBps
    fee_raw = merged.get("fee_bps") if "fee_bps" in merged else merged.get("feeBps")
    fee_bps = DEFAULT_AMM_FEE_BPS if fee_raw is None else fee_raw
    try:
        fee_bps_int = int(fee_bps)
    except (TypeError, ValueError):
        raise AmmSetupError("amm.fee_bps must be an integer")

    # DB allows 0..10000 inclusive
    if fee_bps_int < 0 or fee_bps_int > 10000:
        raise AmmSetupError("amm.fee_bps must be between 0 and 10000")

    # Collateral token symbol/address supports legacy keys
    collateral_token = (
        merged.get("collateral_token")
        or merged.get("collateral")
        or merged.get("collateralToken")
        or DEFAULT_COLLATERAL_TOKEN
    )
    collateral_token = str(collateral_token).strip() if collateral_token is not None else ""
    if not collateral_token:
        raise AmmSetupError("amm.collateral_token is required")

    return {
        "model": model,
        "b": b,
        "fee_bps": fee_bps_int,
        "collateral_token": collateral_token,
    }


def _select_exclusive_event_option_ids(event: Event) -> List[int]:
    """
    For exclusive events: pick ONE canonical option per market (prefer side='yes').

    Risk-handling:
      - market_options.side is nullable at DB level; if we can't find side='yes',
        we fall back to option_index smallest and emit a warning (to avoid silent inversion).

    Returns option_ids ordered by market sort order.
    """
    markets = list(
        Market.objects.filter(event=event)
        .order_by("sort_weight", "-created_at", "id")
        .values_list("id", flat=True)
    )
    if not markets:
        return []

    # All options for these markets; deterministic ordering
    rows = list(
        MarketOption.objects.filter(market_id__in=markets, is_active=True)
        .order_by("market_id", "option_index", "id")
        .values_list("market_id", "id", "side", "option_index")
    )

    chosen: Dict[str, Dict[str, Any]] = {}
    for market_id, option_id, side, option_index in rows:
        k = str(market_id)
        if k not in chosen:
            chosen[k] = {"id": option_id, "side": side, "idx": option_index}
            continue
        # Prefer YES
        if chosen[k]["side"] != OptionSide.YES.value and side == OptionSide.YES.value:
            chosen[k] = {"id": option_id, "side": side, "idx": option_index}

    # Preserve market order + warn if fallback is not YES
    result: List[int] = []
    for market_id in markets:
        k = str(market_id)
        if k not in chosen:
            continue
        if chosen[k]["side"] != OptionSide.YES.value:
            logger.warning(
                "exclusive pool: market %s has no side='yes' option; using option_id=%s side=%s idx=%s",
                market_id,
                chosen[k]["id"],
                chosen[k]["side"],
                chosen[k]["idx"],
            )
        result.append(chosen[k]["id"])

    return result


def _get_active_market_option_ids(market: Market) -> List[int]:
    return list(
        MarketOption.objects.filter(market=market, is_active=True)
        .order_by("option_index", "id")
        .values_list("id", flat=True)
    )


@transaction.atomic
def ensure_pool_initialized(
    *,
    market: Optional[Market] = None,
    event: Optional[Event] = None,
    amm_params: Optional[Dict[str, Any]] = None,
    created_by_id: Optional[str] = None,
) -> AmmPool:
    """
    Create AMM pool + option states if missing (idempotent).

    Scope rules:
      - event-level pool ONLY for event.group_rule == 'exclusive'
      - market-level pool for 'standalone' and 'independent' markets

    Concurrency + safety:
      - unique(market_id) / unique(event_id) in DB => handle IntegrityError on create
      - option states PK is (pool_id, option_id) => bulk_create(ignore_conflicts=True)
      - do NOT overwrite existing pool params (model/b/fee/collateral); only backfill states

    Note on transaction scope:
      - We keep a single atomic block because trading code typically assumes pool+states
        appear together (avoid "pool exists but states missing" window).
    """
    if (market is None) == (event is None):
        raise AmmSetupError("Provide exactly one of market= or event=")

    params = normalize_amm_params(amm_params or {})

    # Precompute option_ids with simple read queries (still inside transaction if caller already has one)
    if event is not None:
        rule = (event.group_rule or "").strip().lower()
        if rule != GroupRule.EXCLUSIVE.value:
            raise AmmSetupError("event-level pool is only allowed for group_rule='exclusive'")
        option_ids = _select_exclusive_event_option_ids(event)
    else:
        option_ids = _get_active_market_option_ids(market)

    # Create or fetch pool
    if event is not None:
        pool = AmmPool.objects.filter(event=event).first()
        if pool is None:
            try:
                pool = AmmPool.objects.create(
                    event=event,
                    model=params["model"],
                    b=params["b"],
                    fee_bps=params["fee_bps"],
                    collateral_token=params["collateral_token"],
                    created_by_id=created_by_id or event.created_by_id,
                )
            except IntegrityError:
                pool = AmmPool.objects.get(event=event)
    else:
        pool = AmmPool.objects.filter(market=market).first()
        if pool is None:
            try:
                pool = AmmPool.objects.create(
                    market=market,
                    model=params["model"],
                    b=params["b"],
                    fee_bps=params["fee_bps"],
                    collateral_token=params["collateral_token"],
                    created_by_id=created_by_id or market.created_by_id,
                )
            except IntegrityError:
                pool = AmmPool.objects.get(market=market)

    # Backfill option states (idempotent)
    if option_ids:
        # For huge N, avoid constructing massive lists at once
        batch_size = 2000
        to_create: List[AmmPoolOptionState] = []
        for opt_id in option_ids:
            to_create.append(AmmPoolOptionState(pool=pool, option_id=opt_id, q=Decimal("0")))
            if len(to_create) >= batch_size:
                AmmPoolOptionState.objects.bulk_create(to_create, ignore_conflicts=True, batch_size=batch_size)
                to_create = []
        if to_create:
            AmmPoolOptionState.objects.bulk_create(to_create, ignore_conflicts=True, batch_size=batch_size)

    return pool
