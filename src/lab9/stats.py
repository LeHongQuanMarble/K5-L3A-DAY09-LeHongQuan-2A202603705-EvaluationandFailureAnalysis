from __future__ import annotations

from collections.abc import Sequence
from math import comb
from numbers import Integral

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge):
        raise ValueError('human and judge must have the same length')
    counts = {'tp':0, 'fp':0, 'fn':0, 'tn':0}
    for h, j in zip(human, judge):
        h_fail = h == POS 
        j_fail = j == POS 
        if h_fail and j_fail:
            counts['tp'] += 1
        elif j_fail:
            counts['fp'] += 1
        elif h_fail:
            counts['fn'] += 1
        else:
            counts['tn'] += 1
    return counts

def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    # TODO M2: precision = tp/(tp+fp), recall = tp/(tp+fn); return 0.0 when the denominator is 0
    c = confusion(human, judge)
    flagged = c['tp'] + c['fp']
    actual = c['tp'] + c['fn']
    precision = c['tp'] / flagged if flagged else 0.0
    recall = c['tp'] / actual if actual else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    c = confusion(human, judge)
    n = c["tp"] + c["fp"] + c["fn"] + c["tn"]
    if n == 0:
        raise ValueError("kappa undefined: no items")
    p_o = (c["tp"] + c["tn"]) / n                  # tỉ lệ đồng ý thực tế
    h_fail = (c["tp"] + c["fn"]) / n               # P(người nói FAIL)
    j_fail = (c["tp"] + c["fp"]) / n               # P(judge nói FAIL)
    p_e = h_fail * j_fail + (1 - h_fail) * (1 - j_fail)   # đồng ý do may mắn
    if p_e >= 1.0:
        raise ValueError("kappa undefined: p_e == 1 (constant labels, no signal)")
    return (p_o - p_e) / (1 - p_e)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denom = sensitivity + specificity - 1
    if denom <= 0:
        raise ValueError("judge is no better than chance (sens + spec <= 1)")
    corrected = (observed_rate + specificity - 1) / denom
    return max(0.0, min(1.0, corrected))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("a and b must be the same items in the same order")
    diff = float(np.mean(a)-np.mean(b))
    if len({x-y for x,y in zip(a,b)}) <= 1:
        return (diff, diff, diff)
    res = bootstrap(
        (a, b),
        lambda x, y: np.mean(x) - np.mean(y),
        paired=True,
        n_resamples=n_resamples,
        method="percentile",
        confidence_level=confidence,
        rng=np.random.default_rng(rng),
    )
    return (diff, float(res.confidence_interval.low), float(res.confidence_interval.high))


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    _check_nck(n, c, k)
    return 1.0 - comb(n - c, k) / comb(n, k)      # comb(a, k) == 0 when k > a


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    _check_nck(n, c, k)
    return comb(c, k) / comb(n, k)


def _check_nck(n: int, c: int, k: int) -> None:
    """Shared argument check: integers with n >= 1, 0 <= c <= n, 1 <= k <= n."""
    for name, v in (("n", n), ("c", c), ("k", k)):
        if isinstance(v, bool) or not isinstance(v, Integral):
            raise ValueError(f"{name} must be an int, got {v!r}")
    n, c, k = int(n), int(c), int(k)
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if not 0 <= c <= n:
        raise ValueError(f"c must be in [0, n={n}], got {c}")
    if not 1 <= k <= n:
        raise ValueError(f"k must be in [1, n={n}], got {k}")
