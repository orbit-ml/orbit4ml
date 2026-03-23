# orbit4ml — Ecosystem Design Spec

**Date:** 2026-03-22
**Author:** Mainak Mallick
**Status:** Draft

---

## 1. Vision

orbit4ml is an open-source monorepo ecosystem for training and deploying large ML models in space. It covers the full spectrum — ground-based development, in-orbit inference, and in-orbit training — with the four physical constraints of orbital compute as its core differentiator.

The project draws structural inspiration from [learn2learn](https://learn2learn.net) (unified ecosystem, MkDocs documentation, modular subpackages) but is focused on large model training and federated learning, not meta-learning.

## 2. Core Thesis

ML training in orbit is constrained by four physical facts that have no analogue in Earth data centers:

1. **Power is intermittent** — solar panels produce nothing during eclipse (~45 min per 90 min orbit in LEO)
2. **Cooling is position-dependent** — GPU thermal budget varies continuously with orbital position as radiator panels alternately face the sun and deep space
3. **Network topology changes** — in a multi-node cluster, inter-satellite links connect and disconnect as satellites move relative to each other
4. **No human intervention is possible** — every failure mode must be handled autonomously by software

No existing ML training infrastructure is designed around any of these constraints. orbit4ml is built around all four from the ground up.

## 3. Three Pillars of Societal Contribution

### 3.1 Simulation — Orbital Digital Twin

A physics-based simulator modeling orbital mechanics (SGP4/TLE), eclipse geometry, thermal radiation budgets, inter-satellite link availability with Doppler, and hardware fault injection. This lets anyone test space ML algorithms without access to a real satellite — democratizing experimentation.

### 3.2 Open Datasets & Benchmarks

Curated space ML datasets (satellite imagery, telemetry, sensor data) with standardized benchmarks and evaluation protocols. Today this data is scattered across agencies and gated behind access requests. Centralizing it is a major unlock for the research community.

### 3.3 Production-Ready Libraries

Battle-tested, well-documented code for constraint-aware training, federated learning, model compression, and edge deployment. Reference implementations adapted for orbital constraints that space companies and agencies can actually deploy.

## 4. Architecture

### 4.1 Monorepo Structure

Single repository, modular subpackages. One `pip install orbit4ml` gets everything.

```
orbit4ml/
├── orbit4ml/
│   ├── __init__.py
│   ├── sim/           # Orbital digital twin
│   ├── data/          # Datasets & loaders
│   ├── train/         # Constraint-aware training loops
│   ├── fed/           # Federated learning
│   ├── compress/      # Quantization, pruning, distillation
│   ├── edge/          # FPGA/SoC inference export
│   └── bench/         # Benchmarks & evaluation
├── docs/              # MkDocs Material site
├── examples/          # Notebooks & scripts
├── tests/
├── pyproject.toml
└── LICENSE
```

### 4.2 Module Descriptions

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `sim` | Orbital digital twin | SGP4 propagator, eclipse model, thermal radiation model, ISL link budget with Doppler, hardware fault injection |
| `data` | Space ML datasets | Dataset loaders (EuroSAT, telemetry), transforms, on-demand download wrappers (respecting upstream licenses) |
| `train` | Constraint-aware training | Power-aware scheduling, thermal throttling, checkpoint/resume across eclipse cycles, autonomous fault recovery |
| `fed` | Federated learning | Topology-aware aggregation, async SGD, bandwidth-constrained gradient exchange, constellation-scale coordination |
| `compress` | Model compression | Quantization, structured pruning, knowledge distillation targeting space hardware constraints |
| `edge` | Edge deployment | Model export for FPGAs, radiation-tolerant SoCs, embedded processors |
| `bench` | Benchmarks | Standardized evaluation protocols, reproducible experiment configs, leaderboards |

### 4.3 Module Dependencies

```
sim ← (standalone, no internal deps)
data ← (standalone, no internal deps)
train ← sim (uses constraint profiles)
fed ← sim (uses topology/link models), train (uses training loops)
compress ← (standalone)
edge ← compress (uses compressed models)
bench ← sim, data, train (orchestrates full experiments)
```

## 5. Simulator Design (orbit4ml.sim)

The simulator is the foundation that enables all other modules.

### 5.1 Core Components

- **Constellation** — defines orbital parameters (planes, satellites per plane, altitude, inclination)
- **Propagator** — SGP4-based orbit propagation from TLEs or Keplerian elements
- **EclipseModel** — computes sunlit/eclipse intervals per satellite using Earth shadow geometry (cylindrical shadow model)
- **ThermalModel** — v0.1 ships a simplified model: piecewise function of orbital angle (sunlit vs eclipse thermal budget). Higher-fidelity multi-node thermal networks deferred to v0.3+
- **ISLModel** — computes inter-satellite link availability and bandwidth based on relative positions and antenna constraints. Doppler shift modeling deferred to v0.3+
- **FaultInjector** — simulates single-event upsets (SEUs), thermal shutdowns, and link failures

### 5.2 Time Model

Propagation requires a start epoch. Options:
- Explicit: `twin.propagate(start=datetime(2026, 6, 1), hours=2)`
- Default: current UTC time (`datetime.utcnow()`)
- From TLE: if constellation is initialized from TLEs, the TLE epoch is used

Step size defaults to 60 seconds and is configurable via `step_seconds`.

### 5.3 Inter-Module Interface Contracts

Objects that cross module boundaries are defined as dataclasses:

```python
from dataclasses import dataclass

@dataclass
class PowerState:
    available: bool        # True when solar panels are generating power
    watts: float           # current solar power output (0.0 during eclipse)
    # available is always (watts > 0). Battery backup is not modeled in v0.1.

@dataclass
class ThermalState:
    gpu_budget_watts: float  # max GPU power before thermal throttle
    within_budget: bool      # whether current load is safe
    radiator_efficiency: float  # 0.0–1.0

@dataclass
class LinkState:
    active: list[tuple[str, str]]  # list of (this_sat_id, peer_sat_id) pairs
    bandwidth_mbps: float          # aggregate available bandwidth

@dataclass
class FaultState:
    active: list[str]      # fault type identifiers ("seu", "thermal_shutdown", "link_failure")

@dataclass
class SatelliteState:
    """Per-satellite constraint snapshot at a given timestep."""
    id: str
    position_eci: tuple[float, float, float]  # (x, y, z) in km, ECI frame
    power: PowerState
    thermal: ThermalState
    links: LinkState
    faults: FaultState

@dataclass
class EpochState:
    """Constellation state at a single timestep."""
    timestamp: datetime
    satellites: list[SatelliteState]
```

The `train` module (v0.2) will consume `SatelliteState` to make scheduling decisions. The `fed` module (v1.0) will consume `LinkState` to manage gradient exchange.

### 5.4 API Shape

```python
import orbit4ml
from datetime import datetime

# Define constellation
constellation = orbit4ml.sim.Constellation(
    planes=6, sats_per_plane=11, altitude=550, inclination=53.0
)

# Create digital twin
twin = orbit4ml.sim.DigitalTwin(constellation)

# Propagate and access constraints
for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=2, step_seconds=60):
    for sat in epoch.satellites:
        print(sat.power.available)          # bool
        print(sat.power.watts)              # float
        print(sat.thermal.gpu_budget_watts)  # float
        print(sat.links.active)             # list of ISL links
        print(sat.faults.active)            # list of active faults
```

## 6. MVP — First Release (v0.1)

### 6.1 Prerequisites

- Bootstrap Python package skeleton (`pyproject.toml`, `orbit4ml/__init__.py`, submodule `__init__.py` files)
- Set up CI workflow for tests on every PR

### 6.2 Scope

Ship `orbit4ml.sim` + `orbit4ml.data` as a bundle. Minimum viable slice:

- **sim**: Constellation definition, SGP4 propagation, eclipse model, simplified thermal model (piecewise orbital angle). ISL link availability (no Doppler yet). Basic fault injection.
- **data**: One curated dataset (EuroSAT satellite imagery). Download-on-demand wrapper respecting upstream CC-BY license.
- **Example notebook**: Use the simulator to generate orbital constraints, load data, and run a vanilla PyTorch training loop that respects the constraints.

### 6.3 Target Model Scale

"Large model" in the orbital context means models that stress space-grade hardware — typically 10M–1B parameters. This is far smaller than terrestrial "large" (100B+) but large enough that power/thermal constraints force non-trivial scheduling decisions. The simulator and training infrastructure should be designed with this range in mind.

### 6.4 MVP Example

v0.1 ships only `sim` and `data`. The training loop uses vanilla PyTorch — the constraint-aware `train` module comes in v0.2.

```python
import torch
import orbit4ml
from datetime import datetime

# 1. Create orbital environment
constellation = orbit4ml.sim.Constellation(
    planes=6, sats_per_plane=11, altitude=550, inclination=53.0
)
twin = orbit4ml.sim.DigitalTwin(constellation)

# 2. Load space dataset
dataset = orbit4ml.data.EuroSAT(root="./data")
loader = torch.utils.data.DataLoader(dataset, batch_size=32)

# 3. Vanilla PyTorch training, gated by orbital constraints
model = torch.nn.Sequential(torch.nn.Flatten(), torch.nn.Linear(3 * 64 * 64, 10))
optimizer = torch.optim.Adam(model.parameters())

for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=2):
    for sat in epoch.satellites:
        if sat.power.available and sat.thermal.within_budget:
            for batch in loader:
                loss = torch.nn.functional.cross_entropy(model(batch[0]), batch[1])
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
        else:
            # Eclipse — would checkpoint here (train module, v0.2)
            pass
```

### 6.5 MVP Test Cases

- Verify ISS-like orbit (altitude=408, inclination=51.6) produces eclipse intervals within 2 minutes of known values (~35 min eclipse per ~92 min orbit)
- Verify EuroSAT loader returns tensors of expected shape and dtype
- Verify `Constellation` with known parameters produces correct satellite count (`planes * sats_per_plane`)
- Verify `propagate()` yields correct number of timesteps for given duration and step size
- Integration test: full example notebook runs without error

## 7. Roadmap

| Version | Modules | What Ships |
|---------|---------|------------|
| v0.1 | sim + data | Digital twin + curated dataset, complete experiment loop |
| v0.2 | train + bench | Constraint-aware training for large models, first benchmarks |
| v0.3 | compress + edge | Model compression and deployment to space-grade hardware |
| v1.0 | fed | Federated learning across satellite constellations with dynamic topology |

**Note:** `fed` (v1.0) depends on a mature ISL model in `sim`. The ISL model should be progressively enhanced in v0.2 and v0.3 (adding Doppler, realistic bandwidth models) to avoid a bottleneck at v1.0.

## 8. Technology Stack

- **Language:** Python 3.10+
- **ML Framework:** PyTorch
- **Orbital mechanics:** sgp4, astropy
- **Docs:** MkDocs Material (dark theme)
- **CI/CD:** GitHub Actions
- **Hosting:** GitHub Pages (orbit-ml.github.io/orbit4ml), later custom domain
- **Package:** PyPI (orbit4ml)

## 9. Testing Strategy

- Unit tests for each module (pytest)
- Integration tests: sim + data end-to-end experiment
- Benchmark reproducibility tests
- CI via GitHub Actions on every PR (workflow to be added as part of v0.1 prerequisites)
- See Section 6.5 for MVP-specific test cases

### 9.1 Dataset Licensing

Datasets are wrapped as download-on-demand loaders — orbit4ml does not redistribute third-party data. Each dataset wrapper documents its upstream license (e.g., EuroSAT is CC-BY). Users download directly from the source.

## 10. Documentation Strategy

- MkDocs Material site (already scaffolded)
- Auto-generated API reference via mkdocstrings (Google-style docstrings)
- Tutorials for each module
- Example notebooks in `examples/`
- Changelog maintained per release
