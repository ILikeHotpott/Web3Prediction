import math

from .errors import QuoteInputError, QuoteMathError


def _max_gross_payout(p_k: float, b: float) -> float:
    # max gross payout when selling infinite shares of outcome k:
    # = -b*log(1-p_k)
    if not (0.0 < p_k < 1.0):
        raise QuoteMathError("invalid pre probability for max payout")
    return -b * math.log1p(-p_k)


def _solve_sell_shares_for_gross_payout(p_k: float, b: float, gross: float) -> float:
    """
    Solve s>0:
      gross = C(q) - C(q - s e_k)
    closed form:
      exp(-gross/b) = 1 + p_k*(exp(-s/b)-1)
      s = -b * log( 1 + (exp(-gross/b)-1)/p_k )
    """
    if gross <= 0.0 or not math.isfinite(gross):
        raise QuoteInputError("gross payout must be > 0")
    if not (0.0 < p_k < 1.0):
        raise QuoteMathError("pre prob must be in (0,1) for sell solve")

    max_gross = _max_gross_payout(p_k, b)
    if gross >= max_gross:
        raise QuoteMathError(f"desired sell gross too large (max gross={max_gross})")

    a = gross / b
    expm1_neg = math.expm1(-a)          # in (-1, 0]
    rhs = 1.0 + expm1_neg / p_k         # in (0, 1]
    if not (0.0 < rhs <= 1.0):
        raise QuoteMathError("sell solve invalid rhs (check inputs)")
    return -b * math.log(rhs)

