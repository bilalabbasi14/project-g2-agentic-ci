"""Hand-calculated metric examples."""
import pytest

from src.eval.metrics import all_metrics, apfdc, dtc, package_of, sapfdc, sds

D = {"a.x.T1": 2.0, "a.x.T2": 4.0, "a.y.T3": 2.0, "b.T4": 2.0}


def test_apfdc_hand_computed():
    # order T1,T2,T3,T4 ; failing T2,T4 ; C_total = 10, n = 4, m = 2
    # T2: before 2 + 4/2 = 4 ; T4: before 8 + 2/2 = 9 ; sum = 13
    # APFDc = 1 - 13/(2*10) + 1/8 = 1 - 0.65 + 0.125 = 0.475
    order = ["a.x.T1", "a.x.T2", "a.y.T3", "b.T4"]
    assert apfdc(order, D, {"a.x.T2", "b.T4"}) == pytest.approx(0.475)


def test_apfdc_edge_cases():
    assert apfdc(["a.x.T1"], D, set()) == 1.0
    assert apfdc(["z"], {"z": 0.0}, {"z"}) == 0.0


def test_dtc():
    assert dtc(["a.x.T1", "a.x.T2"], {"a.x.T2", "b.T4"}) == 0.5
    assert dtc(["a.x.T1"], set()) is None


def test_sapfdc_hand_computed():
    # selected T2,T1 ; failing T2,T4 -> %DTC = 0.5
    # subset: C_total = 6, n = 2, m = 1 ; T2 first: 0 + 4/2 = 2
    # APFDc_subset = 1 - 2/6 + 1/4 = 0.916667 ; SAPFDc = 0.458333
    assert sapfdc(["a.x.T2", "a.x.T1"], D, {"a.x.T2", "b.T4"}) == pytest.approx(0.5 * (1 - 2 / 6 + 0.25))
    assert sapfdc(["a.x.T1"], D, {"b.T4"}) == 0.0
    assert sapfdc(["a.x.T1"], D, set()) is None


def test_sds():
    assert package_of("a.x.T1$Inner") == "a.x"
    # packages a.x, a.x, a.y -> 2 distinct / 3
    assert sds(["a.x.T1", "a.x.T2", "a.y.T3"]) == pytest.approx(2 / 3)
    assert sds([]) is None


def test_all_metrics():
    m = all_metrics(["a.x.T2"], D, {"a.x.T2"}, full_order=list(D))
    assert m["dtc"] == 1.0 and m["found"] == 1 and m["selected_duration"] == 4.0
    # full order T1,T2,T3,T4 with failing T2: (2 + 2)/(1*10) -> 1 - 0.4 + 0.125
    assert m["apfdc_full"] == pytest.approx(0.725)
