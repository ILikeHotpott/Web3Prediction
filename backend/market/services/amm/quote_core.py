from __future__ import annotations

import math
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from typing import Dict, Optional

from .errors import QuoteInputError, QuoteMathError
from .lmsr import buy_amount_to_delta_q, cost, prices
from .money import (
    Number,
    _bps_from_probabilities,
    _fee_rate_from_bps,
    _finite_pos_float,
    _quantize_money,
    _to_decimal,
)
from .quote_math import _max_gross_payout, _solve_sell_shares_for_gross_payout
from .state import PoolState, _resolve_target_idx


def quote_from_state(
    state: PoolState,
    *,
    option_id: Optional[str] = None,
    option_index: Optional[int] = None,
    side: str = "buy",
    amount_in: Optional[Number] = None,
    shares: Optional[Number] = None,
    money_quant: Decimal = Decimal("0.01"),
) -> Dict:
    """
    Pure function quote:
      - NO database access
      - Deterministic rounding:
          buy money: ROUND_UP (user pays)
          sell money: ROUND_DOWN (user receives)

    Exactly one of (amount_in, shares) must be provided.

    Semantics:
      BUY:
        - amount_in provided: fee taken from amount_in, net goes to AMM -> shares_out
        - shares provided: compute net_cost, gross-up with fee -> amount_in

      SELL:
        - shares provided: compute gross proceeds, fee taken -> amount_out (net)
        - amount_in provided: interpret as desired NET amount_out, gross-up -> solve shares_in
    """
    side = (side or "").lower()
    if side not in {"buy", "sell"}:
        raise QuoteInputError("side must be 'buy' or 'sell'")

    if (amount_in is None and shares is None) or (amount_in is not None and shares is not None):
        raise QuoteInputError("provide exactly one of amount_in or shares")

    fee_rate = _fee_rate_from_bps(state.fee_bps)  # Decimal
    one_minus_fee = (Decimal("1") - fee_rate)

    target_idx = _resolve_target_idx(state, option_id=option_id, option_index=option_index)

    pre_probs = prices(state.q, state.b)
    pre_prob_bps = _bps_from_probabilities(pre_probs)
    p_k = float(pre_probs[target_idx])

    def post_prob_bps_for(q_post):
        return _bps_from_probabilities(prices(q_post, state.b))

    # ---------------- BUY ----------------
    if side == "buy":
        if amount_in is not None:
            gross_in_dec = _to_decimal(amount_in, "amount_in")
            if gross_in_dec <= 0:
                raise QuoteInputError("amount_in must be > 0")

            # fee & net with explicit rounding (system-favorable)
            fee_dec = _quantize_money(gross_in_dec * fee_rate, money_quant, ROUND_UP)
            net_dec = gross_in_dec - fee_dec
            if net_dec <= 0:
                raise QuoteMathError("Amount too low to cover fees")

            net_float = _finite_pos_float(net_dec, "amount_net")

            delta = float(buy_amount_to_delta_q(state.q, state.b, target_idx, net_float))
            if not (math.isfinite(delta) and delta > 0.0):
                raise QuoteMathError("Amount too low to produce any shares (after fees / rounding)")

            q_post = list(state.q)
            q_post[target_idx] += delta
            post_prob_bps = post_prob_bps_for(q_post)

            # avg price uses gross user paid (rounded) / shares
            avg_price_bps = int(round(float(gross_in_dec) / delta * 10000.0))

            return {
                "market_id": state.market_id,
                "pool_id": state.pool_id,
                "option_id": state.option_ids[target_idx],
                "side": "buy",
                "amount_in": str(_quantize_money(gross_in_dec, money_quant, ROUND_UP)),
                "shares_out": str(Decimal(str(delta))),
                "fee_amount": str(fee_dec),
                "avg_price_bps": avg_price_bps,
                "pre_prob_bps": pre_prob_bps,
                "post_prob_bps": post_prob_bps,
                "option_ids": state.option_ids,
                "option_indexes": state.option_indexes,
            }

        # buy with shares
        shares_dec = _to_decimal(shares, "shares")
        if shares_dec <= 0:
            raise QuoteInputError("shares must be > 0")
        shares_float = _finite_pos_float(shares_dec, "shares")

        q_post = list(state.q)
        q_post[target_idx] += shares_float

        net_cost_float = float(cost(q_post, state.b) - cost(state.q, state.b))
        if not (math.isfinite(net_cost_float) and net_cost_float > 0.0):
            raise QuoteMathError("invalid net cost for buy(shares)")

        net_cost_dec = _quantize_money(Decimal(str(net_cost_float)), money_quant, ROUND_UP)
        if one_minus_fee <= 0:
            raise QuoteInputError("fee too high")

        gross_in_dec = _quantize_money(net_cost_dec / one_minus_fee, money_quant, ROUND_UP)
        fee_dec = gross_in_dec - net_cost_dec

        post_prob_bps = post_prob_bps_for(q_post)
        avg_price_bps = int(round(float(gross_in_dec) / shares_float * 10000.0))

        return {
            "market_id": state.market_id,
            "pool_id": state.pool_id,
            "option_id": state.option_ids[target_idx],
            "side": "buy",
            "amount_in": str(gross_in_dec),
            "shares_out": str(shares_dec),
            "fee_amount": str(fee_dec),
            "avg_price_bps": avg_price_bps,
            "pre_prob_bps": pre_prob_bps,
            "post_prob_bps": post_prob_bps,
            "option_ids": state.option_ids,
            "option_indexes": state.option_indexes,
        }

    # ---------------- SELL ----------------
    if shares is not None:
        shares_dec = _to_decimal(shares, "shares")
        if shares_dec <= 0:
            raise QuoteInputError("shares must be > 0")
        shares_float = _finite_pos_float(shares_dec, "shares")

        q_post = list(state.q)
        q_post[target_idx] -= shares_float

        gross_float = float(cost(state.q, state.b) - cost(q_post, state.b))
        if not (math.isfinite(gross_float) and gross_float > 0.0):
            raise QuoteMathError("invalid gross proceeds for sell(shares)")

        gross_dec = _quantize_money(Decimal(str(gross_float)), money_quant, ROUND_DOWN)
        fee_dec = _quantize_money(gross_dec * fee_rate, money_quant, ROUND_UP)
        net_out_dec = _quantize_money(gross_dec - fee_dec, money_quant, ROUND_DOWN)

        if net_out_dec <= 0:
            raise QuoteMathError("Proceeds too low after fees / rounding")

        post_prob_bps = post_prob_bps_for(q_post)
        avg_price_bps = int(round(float(net_out_dec) / shares_float * 10000.0))

        return {
            "market_id": state.market_id,
            "pool_id": state.pool_id,
            "option_id": state.option_ids[target_idx],
            "side": "sell",
            "amount_out": str(net_out_dec),
            "shares_in": str(shares_dec),
            "fee_amount": str(fee_dec),
            "avg_price_bps": avg_price_bps,
            "pre_prob_bps": pre_prob_bps,
            "post_prob_bps": post_prob_bps,
            "option_ids": state.option_ids,
            "option_indexes": state.option_indexes,
        }

    desired_net_out_dec = _to_decimal(amount_in, "amount_in")
    if desired_net_out_dec <= 0:
        raise QuoteInputError("amount_in (desired amount_out) must be > 0")

    desired_net_out_dec = _quantize_money(desired_net_out_dec, money_quant, ROUND_DOWN)

    if one_minus_fee <= 0:
        raise QuoteInputError("fee too high")

    gross_needed_dec = _quantize_money(desired_net_out_dec / one_minus_fee, money_quant, ROUND_UP)
    gross_needed_float = float(gross_needed_dec)

    max_gross = _max_gross_payout(p_k, state.b)
    if gross_needed_float >= max_gross:
        max_net = Decimal(str(max_gross)) * one_minus_fee
        raise QuoteMathError(
            f"desired amount_out too large (max net≈{_quantize_money(max_net, money_quant, ROUND_DOWN)})"
        )

    shares_needed = _solve_sell_shares_for_gross_payout(p_k, state.b, gross_needed_float)
    if not (math.isfinite(shares_needed) and shares_needed > 0.0):
        raise QuoteMathError("invalid shares_in solved for sell(amount_out)")

    q_post = list(state.q)
    q_post[target_idx] -= shares_needed

    gross_float = float(cost(state.q, state.b) - cost(q_post, state.b))
    gross_dec = _quantize_money(Decimal(str(gross_float)), money_quant, ROUND_DOWN)
    fee_dec = _quantize_money(gross_dec * fee_rate, money_quant, ROUND_UP)
    net_out_dec = _quantize_money(gross_dec - fee_dec, money_quant, ROUND_DOWN)

    post_prob_bps = post_prob_bps_for(q_post)
    avg_price_bps = int(round(float(net_out_dec) / shares_needed * 10000.0))

    return {
        "market_id": state.market_id,
        "pool_id": state.pool_id,
        "option_id": state.option_ids[target_idx],
        "side": "sell",
        "amount_out": str(net_out_dec),
        "shares_in": str(Decimal(str(shares_needed))),
        "fee_amount": str(fee_dec),
        "avg_price_bps": avg_price_bps,
        "pre_prob_bps": pre_prob_bps,
        "post_prob_bps": post_prob_bps,
        "option_ids": state.option_ids,
        "option_indexes": state.option_indexes,
        "requested_amount_out": str(desired_net_out_dec),
        "gross_needed": str(gross_needed_dec),
    }

