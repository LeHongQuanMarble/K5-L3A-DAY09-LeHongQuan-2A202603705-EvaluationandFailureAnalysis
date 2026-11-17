"""Regression test from docs/trace_case.md: seeded_regression C-002@11 (FM-03 ticket_trust).

First wrong step: event 3 `model_override {"delay_days": 5}` (ticket text overrides the DB fact).
The test must FAIL the graders on the buggy variant and PASS them on `fixed`, same claim@seed.
"""
import pytest

pytestmark = pytest.mark.student
CLAIM, SEED = "C-002", 11


def _ctx(case):
    from pydantic_evals.evaluators import EvaluatorContext

    return EvaluatorContext(name="trace_case", inputs={}, metadata=None, expected_output=case["label"],
                            output=case["trial"], duration=0.0, _span_tree=None, attributes={}, metrics={})


@pytest.fixture(scope="module")
def cases():
    from lab9.trace_case import investigate

    return {shape: investigate(shape, CLAIM, SEED) for shape in ("seeded_regression", "fixed")}


def test_first_wrong_step_is_model_override(cases):
    kinds = [e["kind"] for e in cases["seeded_regression"]["trial"]["events"]]
    assert kinds[:3] == ["handoff", "investigator", "model_override"]
    assert cases["seeded_regression"]["trial"]["events"][2]["payload"] == {"delay_days": 5}
    # Control: same claim@seed on `fixed` keeps the DB fact and goes straight to the quote.
    assert "model_override" not in [e["kind"] for e in cases["fixed"]["trial"]["events"]]


def test_graders_catch_buggy_variant(cases):
    from lab9.graders import DbFactKept, RefundAmountCorrect

    ctx = _ctx(cases["seeded_regression"])
    assert DbFactKept().evaluate(ctx).value is False
    assert RefundAmountCorrect().evaluate(ctx).value is False      # ledger 20000 vs label 0


def test_graders_pass_fixed(cases):
    from lab9.graders import DbFactKept, RefundAmountCorrect

    ctx = _ctx(cases["fixed"])
    assert DbFactKept().evaluate(ctx).value is True
    assert RefundAmountCorrect().evaluate(ctx).value is True
