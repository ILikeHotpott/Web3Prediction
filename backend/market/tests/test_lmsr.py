# market/tests/test_lmsr.py
import math
import random
import sys
from pathlib import Path

import pytest
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market.services.amm.lmsr import prices, cost, buy_amount_to_delta_q


ABS_TOL = 1e-12


# ---------- helpers ----------
def _rng() -> random.Random:
    # 固定种子：测试可复现
    return random.Random(20260101)


def _rand_q(rng: random.Random, n: int, scale: float = 1e6):
    # 生成有限 q（不含 inf/nan）
    return [rng.uniform(-scale, scale) for _ in range(n)]


def _unit(n: int, i: int):
    e = [0.0] * n
    e[i] = 1.0
    return e


def _add(q, v):
    return [a + b for a, b in zip(q, v)]


def _mul(q, k: float):
    return [a * k for a in q]


# ---------- basic sanity / input validation ----------
def test_invalid_inputs_raise():
    q = [0.0, 0.0]

    with pytest.raises(ValueError):
        prices(q, 0.0)
    with pytest.raises(ValueError):
        cost(q, -1.0)
    with pytest.raises(ValueError):
        buy_amount_to_delta_q(q, 10.0, 0, 0.0)
    with pytest.raises(ValueError):
        buy_amount_to_delta_q(q, 10.0, 0, -1.0)
    with pytest.raises(IndexError):
        buy_amount_to_delta_q(q, 10.0, -1, 1.0)
    with pytest.raises(IndexError):
        buy_amount_to_delta_q(q, 10.0, 2, 1.0)


def test_prices_output_is_probabilities():
    b = 10_000.0
    p = prices([0.0, 0.0], b)
    assert len(p) == 2
    assert all(math.isfinite(x) for x in p)
    assert all(0.0 <= x <= 1.0 for x in p)
    assert sum(p) == pytest.approx(1.0, abs=ABS_TOL)


# ---------- invariants: shift/scale properties ----------
def test_prices_shift_invariant():
    # p(q + c*1) == p(q)
    rng = _rng()
    for _ in range(50):
        n = rng.randint(2, 8)
        b = rng.uniform(1.0, 1e6)
        q = _rand_q(rng, n)
        c = rng.uniform(-1e6, 1e6)

        p0 = prices(q, b)
        p1 = prices([qi + c for qi in q], b)
        assert p1 == pytest.approx(p0, abs=1e-12)


def test_cost_shift_equiv():
    # C(q + c*1) = C(q) + c
    rng = _rng()
    for _ in range(50):
        n = rng.randint(2, 8)
        b = rng.uniform(1.0, 1e6)
        q = _rand_q(rng, n)
        c = rng.uniform(-1e5, 1e5)  # 避免太夸张

        c0 = cost(q, b)
        c1 = cost([qi + c for qi in q], b)
        assert math.isfinite(c0) and math.isfinite(c1)
        assert (c1 - c0) == pytest.approx(c, rel=0, abs=1e-9)


def test_prices_invariant_under_scaling_q_and_b():
    # p(q, b) == p(kq, kb)
    rng = _rng()
    for _ in range(50):
        n = rng.randint(2, 8)
        b = rng.uniform(1.0, 1e6)
        q = _rand_q(rng, n)
        k = rng.uniform(0.1, 10.0)

        p0 = prices(q, b)
        p1 = prices(_mul(q, k), b * k)
        assert p1 == pytest.approx(p0, abs=1e-12)


def test_cost_scales_with_q_and_b():
    # C(kq, kb) = k*C(q, b)
    rng = _rng()
    for _ in range(50):
        n = rng.randint(2, 8)
        b = rng.uniform(1.0, 1e6)
        q = _rand_q(rng, n)
        k = rng.uniform(0.1, 10.0)

        c0 = cost(q, b)
        c1 = cost(_mul(q, k), b * k)
        assert math.isfinite(c0) and math.isfinite(c1)
        assert c1 == pytest.approx(k * c0, rel=1e-12, abs=1e-6)


# ---------- key property: prices are gradient of cost ----------
def test_prices_match_cost_gradient_finite_difference():
    """
    LMSR 的定义：p_i = ∂C/∂q_i
    用有限差分验证（强回归保护）。
    """
    rng = _rng()
    for _ in range(40):
        n = rng.randint(2, 6)
        b = rng.uniform(100.0, 1e6)
        q = _rand_q(rng, n, scale=1e5)  # 控制差分误差
        p = prices(q, b)

        eps = 1e-6 * b  # 与 b 同量纲，数值稳定
        for i in range(n):
            ei = _unit(n, i)
            q_plus = _add(q, _mul(ei, eps))
            q_minus = _add(q, _mul(ei, -eps))

            # 中心差分近似导数
            d = (cost(q_plus, b) - cost(q_minus, b)) / (2.0 * eps)
            assert d == pytest.approx(p[i], rel=1e-6, abs=1e-8)


# ---------- buy: correctness + invariants ----------
def test_buy_increases_target_probability_and_decreases_others():
    rng = _rng()
    for _ in range(60):
        n = rng.randint(2, 8)
        b = rng.uniform(100.0, 1e6)
        q = _rand_q(rng, n, scale=1e5)
        i = rng.randrange(n)
        amount = rng.uniform(0.01 * b, 2.0 * b)  # 覆盖常见交易规模

        p0 = prices(q, b)
        delta = buy_amount_to_delta_q(q, b, option_index=i, amount_net=amount)
        assert math.isfinite(delta) and delta > 0.0

        q2 = list(q)
        q2[i] += delta
        p1 = prices(q2, b)

        assert p1[i] > p0[i]
        for j in range(n):
            if j != i:
                assert p1[j] < p0[j]
        assert sum(p1) == pytest.approx(1.0, abs=ABS_TOL)


def test_buy_cost_difference_equals_amount():
    rng = _rng()
    for _ in range(80):
        n = rng.randint(2, 8)
        b = rng.uniform(100.0, 1e6)
        q = _rand_q(rng, n, scale=1e5)
        i = rng.randrange(n)
        amount = rng.uniform(0.01 * b, 5.0 * b)

        c0 = cost(q, b)
        delta = buy_amount_to_delta_q(q, b, option_index=i, amount_net=amount)
        q2 = list(q)
        q2[i] += delta
        c1 = cost(q2, b)

        diff = c1 - c0
        assert math.isfinite(diff)
        # 按定义必须等于 amount（允许极小浮点误差）
        assert diff == pytest.approx(amount, rel=1e-12, abs=1e-8)


def test_buy_delta_monotonic_in_amount():
    # 同一市场/同一 outcome：花更多钱 -> delta_q 更大
    rng = _rng()
    for _ in range(50):
        n = rng.randint(2, 8)
        b = rng.uniform(100.0, 1e6)
        q = _rand_q(rng, n, scale=1e5)
        i = rng.randrange(n)

        a1 = rng.uniform(0.01 * b, 0.5 * b)
        a2 = rng.uniform(0.6 * b, 2.0 * b)

        d1 = buy_amount_to_delta_q(q, b, i, a1)
        d2 = buy_amount_to_delta_q(q, b, i, a2)
        assert d2 > d1 > 0.0


def test_cost_is_convex_midpoint():
    # LMSR cost 是凸函数：C((q+r)/2) <= (C(q)+C(r))/2
    rng = _rng()
    for _ in range(40):
        n = rng.randint(2, 8)
        b = rng.uniform(100.0, 1e6)
        q = _rand_q(rng, n, scale=1e5)
        r = _rand_q(rng, n, scale=1e5)

        mid = [(qi + ri) / 2.0 for qi, ri in zip(q, r)]
        lhs = cost(mid, b)
        rhs = (cost(q, b) + cost(r, b)) / 2.0
        assert lhs <= rhs + 1e-8  # 允许微小数值误差


def test_small_trade_linear_approximation():
    """
    小额交易近似：amount ≈ p_i * delta  => delta ≈ amount / p_i
    （这是“直觉一致性”测试：非常有用）
    """
    rng = _rng()
    for _ in range(60):
        n = rng.randint(2, 8)
        b = rng.uniform(1e4, 1e6)
        q = _rand_q(rng, n, scale=1e5)
        i = rng.randrange(n)

        p0 = prices(q, b)[i]
        # 小额：远小于 b（保证“近似”成立）
        amount = 1e-6 * b

        delta = buy_amount_to_delta_q(q, b, i, amount)
        approx = amount / p0

        # 近似允许更宽松误差
        assert delta == pytest.approx(approx, rel=1e-4, abs=1e-6)


def test_large_trade_pushes_probability_toward_one_binary():
    # 二元市场极大买入：目标概率应非常接近 1
    b = 10_000.0
    q = [0.0, 0.0]
    amount = 20.0 * b  # 非常大

    p0 = prices(q, b)
    delta = buy_amount_to_delta_q(q, b, 0, amount)
    q2 = [q[0] + delta, q[1]]
    p1 = prices(q2, b)

    assert p0[0] == pytest.approx(0.5, abs=ABS_TOL)
    assert p1[0] > 0.999999  # 接近 1
    assert p1[1] < 0.000001
    assert sum(p1) == pytest.approx(1.0, abs=ABS_TOL)
