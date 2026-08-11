"""city-signals — city open-data analysis toolkit by zAx4hub."""
from __future__ import annotations

import math
import statistics
from typing import Any


def moving_average(series: list[float], window: int = 3) -> list[float]:
    if window < 1:
        raise ValueError("window must be >= 1")
    out: list[float] = []
    for i in range(len(series)):
        lo = max(0, i - window + 1)
        chunk = series[lo : i + 1]
        out.append(round(sum(chunk) / len(chunk), 4))
    return out


def zscore_anomalies(series: list[float], threshold: float = 2.0) -> list[dict[str, Any]]:
    if len(series) < 2:
        return []
    mean = statistics.fmean(series)
    stdev = statistics.pstdev(series) or 1.0
    hits = []
    for i, v in enumerate(series):
        z = (v - mean) / stdev
        if abs(z) >= threshold:
            hits.append({"index": i, "value": v, "z": round(z, 3)})
    return hits


def correlation(a: list[float], b: list[float]) -> float:
    n = min(len(a), len(b))
    if n < 2:
        return 0.0
    a, b = a[:n], b[:n]
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return round(num / den, 4) if den else 0.0


def district_rollup(rows: list[dict[str, Any]], value_key: str = "value") -> list[dict[str, Any]]:
    buckets: dict[str, list[float]] = {}
    for r in rows:
        d = str(r.get("district", "unknown"))
        buckets.setdefault(d, []).append(float(r[value_key]))
    out = []
    for district, vals in sorted(buckets.items()):
        out.append(
            {
                "district": district,
                "count": len(vals),
                "sum": round(sum(vals), 4),
                "avg": round(statistics.fmean(vals), 4),
                "max": max(vals),
                "min": min(vals),
            }
        )
    return out


def congestion_index(speeds: list[float], free_flow: float) -> list[float]:
    if free_flow <= 0:
        raise ValueError("free_flow must be > 0")
    return [round(max(0.0, 1.0 - (s / free_flow)), 4) for s in speeds]


SAMPLE_TRAFFIC = [
    {"district": "north", "hour": h, "value": v}
    for h, v in enumerate([42, 40, 38, 35, 28, 22, 18, 20, 25, 33, 38, 41])
]
SAMPLE_AIR = [
    {"district": "north", "hour": h, "value": v}
    for h, v in enumerate([12, 13, 15, 18, 25, 30, 35, 32, 28, 20, 16, 14])
]
SAMPLE_SOUTH_TRAFFIC = [
    {"district": "south", "hour": h, "value": v}
    for h, v in enumerate([50, 48, 47, 45, 40, 36, 34, 35, 38, 44, 48, 49])
]


def run(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    traffic = payload.get("traffic") or (SAMPLE_TRAFFIC + SAMPLE_SOUTH_TRAFFIC)
    air = payload.get("air") or SAMPLE_AIR
    free_flow = float(payload.get("free_flow", 55))
    threshold = float(payload.get("z_threshold", 1.5))

    north_speed = [float(r["value"]) for r in traffic if r.get("district") == "north"]
    if not north_speed:
        north_speed = [float(r["value"]) for r in traffic]

    air_vals = [float(r["value"]) for r in air]
    cong = congestion_index(north_speed, free_flow)
    anomalies = zscore_anomalies(north_speed, threshold)
    corr = correlation(cong, air_vals)
    rollup = district_rollup(traffic)
    ma = moving_average(north_speed, 3)

    score = min(100, 50 + len(anomalies) * 8 + (20 if abs(corr) > 0.5 else 5))
    return {
        "project": "city-signals",
        "author": "zAx4hub",
        "summary": f"Analyzed {len(traffic)} traffic rows; {len(anomalies)} anomalies; corr(congestion,air)={corr}",
        "score": score,
        "congestion": cong,
        "moving_average": ma,
        "anomalies": anomalies,
        "correlation_congestion_air": corr,
        "districts": rollup,
        "metrics": {
            "traffic_rows": len(traffic),
            "air_rows": len(air),
            "anomalies": len(anomalies),
            "districts": len(rollup),
            "peak_congestion": max(cong) if cong else 0,
        },
    }


def demo() -> dict[str, Any]:
    return run({})


def inspect() -> dict[str, Any]:
    return {
        "name": "city-signals",
        "author": "zAx4hub",
        "oneLiner": "City open-data analysis toolkit",
        "version": "0.1.0",
        "signals": ["traffic-congestion", "air-correlation", "district-rollup", "zscore-anomalies"],
        "commands": ["demo", "run", "inspect"],
    }
