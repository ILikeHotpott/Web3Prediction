from decimal import Decimal
from typing import Optional

from .money import Number
from .quote_core import quote_from_state
from .quote_loader import load_pool_state
from .state import PoolState


def quote(
    *,
    market_id,
    option_id: Optional[str] = None,
    option_index: Optional[int] = None,
    side: str = "buy",
    amount_in: Optional[Number] = None,
    shares: Optional[Number] = None,
    money_quant: Decimal = Decimal("0.01"),
):
    """
    Backward-compatible wrapper.
    For list pages / batch quotes, prefer:
      state = load_pool_state(...)
      quote_from_state(state, ...)
    """
    state: PoolState = load_pool_state(market_id)
    return quote_from_state(
        state,
        option_id=option_id,
        option_index=option_index,
        side=side,
        amount_in=amount_in,
        shares=shares,
        money_quant=money_quant,
    )


__all__ = ["quote", "quote_from_state", "load_pool_state", "PoolState", "Number"]

