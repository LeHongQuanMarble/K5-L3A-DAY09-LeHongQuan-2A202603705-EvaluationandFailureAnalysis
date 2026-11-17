from __future__ import annotations

from collections.abc import Sequence

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
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    # TODO M4
    raise NotImplementedError


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
