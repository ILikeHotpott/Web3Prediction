from dataclasses import dataclass
from typing import Dict, List, Optional

from .errors import QuoteInputError


@dataclass(frozen=True)
class PoolState:
    market_id: str
    pool_id: str
    b: float
    fee_bps: int
    option_ids: List[str]
    option_indexes: List[int]
    q: List[float]
    option_id_to_idx: Dict[str, int]
    option_index_to_idx: Dict[int, int]

    def resolve_target_idx(self, *, option_id: Optional[str], option_index: Optional[int]) -> int:
        return _resolve_target_idx(self, option_id=option_id, option_index=option_index)


def _resolve_target_idx(
    state: PoolState,
    *,
    option_id: Optional[str],
    option_index: Optional[int],
) -> int:
    if option_id is not None:
        oid = str(option_id)
        if oid in state.option_id_to_idx:
            return state.option_id_to_idx[oid]
        raise QuoteInputError("target option_id not found in this pool")

    if option_index is not None:
        if option_index in state.option_index_to_idx:
            return state.option_index_to_idx[option_index]
        raise QuoteInputError("target option_index not found in this pool")

    raise QuoteInputError("must provide option_id or option_index")

