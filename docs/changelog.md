# Changelog

## v0.1.0

### orbit4ml.sim — Orbital Digital Twin
- `Constellation` — Walker-delta constellation definition
- `DigitalTwin` — orchestrator with propagation loop yielding `EpochState` snapshots
- SGP4-based orbit propagation from Keplerian elements
- Cylindrical shadow eclipse model
- Simplified piecewise thermal model (sunlit vs eclipse)
- Distance-based inter-satellite link availability
- Stochastic hardware fault injection (SEU, thermal shutdown, link failure)
- Approximate Sun position calculator

### orbit4ml.data — Space ML Datasets
- `EuroSAT` — download-on-demand wrapper for Sentinel-2 land use classification (CC-BY-4.0)

### Infrastructure
- Package skeleton with pyproject.toml
- MkDocs Material documentation site
- GitHub Actions CI (pytest on Python 3.10/3.11/3.12)
- GitHub Pages deployment
