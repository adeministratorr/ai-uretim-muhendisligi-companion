import math

import pytest

from sampling_lab import LOGITS, softmax_with_temperature, top_k_filter, top_p_filter


def test_softmax_sums_to_one():
    probs = softmax_with_temperature(LOGITS, 1.0)
    assert math.isclose(sum(probs), 1.0, rel_tol=1e-9)


def test_low_temperature_sharpens_distribution():
    low = softmax_with_temperature(LOGITS, 0.2)
    high = softmax_with_temperature(LOGITS, 2.0)
    assert max(low) > max(high)


def test_temperature_zero_rejected():
    with pytest.raises(ValueError):
        softmax_with_temperature(LOGITS, 0)


def test_top_k_keeps_exactly_k_nonzero():
    probs = softmax_with_temperature(LOGITS, 1.0)
    filtered = top_k_filter(probs, 2)
    assert sum(1 for p in filtered if p > 0) == 2
    assert math.isclose(sum(filtered), 1.0, rel_tol=1e-9)


def test_top_p_keeps_highest_probability_candidate():
    probs = softmax_with_temperature(LOGITS, 1.0)
    filtered = top_p_filter(probs, 0.5)
    assert filtered[probs.index(max(probs))] > 0
    assert math.isclose(sum(filtered), 1.0, rel_tol=1e-9)
