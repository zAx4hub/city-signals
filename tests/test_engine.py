from city_signals.engine import (
    congestion_index,
    correlation,
    district_rollup,
    moving_average,
    zscore_anomalies,
    demo,
    inspect,
    run,
)


def test_moving_average():
    assert moving_average([1, 2, 3], 2) == [1.0, 1.5, 2.5]


def test_anomalies_and_corr():
    series = [10, 11, 10, 12, 50, 11]
    hits = zscore_anomalies(series, threshold=1.5)
    assert any(h["index"] == 4 for h in hits)
    assert correlation([1, 2, 3], [2, 4, 6]) == 1.0


def test_rollup_and_congestion():
    rows = [
        {"district": "a", "value": 1},
        {"district": "a", "value": 3},
        {"district": "b", "value": 5},
    ]
    r = district_rollup(rows)
    assert r[0]["avg"] == 2.0
    assert congestion_index([55, 27.5], 55) == [0.0, 0.5]


def test_demo_inspect():
    d = demo()
    assert "zAx4hub" in d["author"]
    assert d["metrics"]["traffic_rows"] > 0
    assert "traffic-congestion" in inspect()["signals"]
    assert run({})["project"] == "city-signals"
