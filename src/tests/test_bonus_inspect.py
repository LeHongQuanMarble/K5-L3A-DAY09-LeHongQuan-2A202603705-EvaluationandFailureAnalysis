"""Bonus: the Inspect AI port must agree with pydantic-evals, including on the positive (violation)
branch that no public variant exercises. Skipped when inspect-ai is not installed (CI installs only
requirements.txt + requirements-lab9.txt). Run: python -m pytest -q -o addopts= tests/test_bonus_inspect.py
"""
import copy
from pathlib import Path

import pytest

pytest.importorskip("inspect_ai")


def test_inspect_port_agrees_on_sibling_refund_bypass(tmp_path):
    from lab8.shapes import SHAPES
    from lab9.eval import load_spec
    from lab9.variant_agent import make_shape
    from bonus.inspect_port import compare

    SHAPES.setdefault("t_sibling_refund", make_shape("t_sibling_refund", {"no_override", "sibling_refund"}))
    spec = copy.deepcopy(load_spec(Path("config/metric_spec.yaml")))
    spec["seeds"] = [11]
    res = compare("t_sibling_refund", spec, str(tmp_path / "logs"))
    assert res["disagreements"] == []
    bypass = res["metrics"]["approval_bypass"]
    assert bypass["pydantic_evals"] == bypass["inspect"] > 0       # FM-07 caught by both
    assert res["metrics"]["refund_amount_correct"]["inspect"] < 1.0
