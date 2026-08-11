# City Signals

> City open-data analysis toolkit

**Author:** zAx4hub

## Problem

Civic dashboards need reliable building blocks: rollups, anomalies, congestion indices, and cross-signal correlation.

## Solution

`city-signals` analyzes traffic/air-style open data series with moving averages, z-score anomalies, district rollups, and congestion↔air correlation.

## Why different

- Pure Python analytics primitives
- Sample multi-district fixtures
- JSON reports for notebooks or APIs
- Owned and credited to **zAx4hub**

## Quickstart

```bash
cd city-signals
py -m pip install -e ".[dev]"
py -m pytest -q
city-signals demo
city-signals run examples/sample-input.json
```

## Features

- Congestion index from free-flow speed
- Z-score anomaly detection
- District rollups + correlation
- CLI + pytest + CI

## Architecture

Stateless helpers in `engine.py`; `run()` composes a full city-signals report.

## Contributing

PRs welcome — keep changes focused and add tests.

## Credits

Built and maintained by **zAx4hub**.

## License

MIT © 2026 zAx4hub
