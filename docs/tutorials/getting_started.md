# Getting Started

This tutorial walks you through installing orbit4ml and running your first orbital ML experiment.

## Prerequisites

- Python 3.10+
- PyTorch 2.0+

## Installation

```bash
pip install orbit4ml
```

Or install from source for the latest development version:

```bash
git clone https://github.com/orbit-ml/orbit4ml.git
cd orbit4ml
pip install -e .
```

## Step 1: Define a Constellation

A constellation describes the satellites in your simulation. orbit4ml uses the
[Walker-delta pattern](https://en.wikipedia.org/wiki/Satellite_constellation#Walker_Constellation),
which is the standard arrangement for LEO mega-constellations like Starlink.

```python
from orbit4ml.sim import Constellation

constellation = Constellation(
    planes=6,            # 6 orbital planes
    sats_per_plane=11,   # 11 satellites per plane
    altitude=550,        # 550 km above Earth
    inclination=53.0,    # 53 degrees orbital tilt
)

print(f"Total satellites: {constellation.total_satellites}")  # 66
```

Each satellite gets a unique ID like `plane0-sat0`, `plane2-sat7`, etc.

## Step 2: Create a Digital Twin

The `DigitalTwin` wraps the constellation with physics models — orbit propagation
(SGP4), eclipse detection, thermal constraints, inter-satellite links, and
fault injection.

```python
from orbit4ml.sim import DigitalTwin

twin = DigitalTwin(constellation)
```

## Step 3: Simulate Orbital Constraints

Call `propagate()` to step through time. At each timestep you get an `EpochState`
containing the state of every satellite — its position, power, thermal budget,
links, and any active faults.

```python
from datetime import datetime

for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=1, step_seconds=60):
    sunlit = sum(1 for s in epoch.satellites if s.power.available)
    eclipsed = len(epoch.satellites) - sunlit
    print(f"[{epoch.timestamp.strftime('%H:%M')}] Sunlit: {sunlit}, Eclipse: {eclipsed}")
```

You'll see satellites cycling in and out of eclipse as they orbit — in LEO, each
satellite spends roughly 35 minutes in shadow per 92-minute orbit.

## Step 4: Train Under Constraints

The key insight: **you can only train when a satellite has power and is within
thermal budget**. In v0.1, you gate a standard PyTorch loop with these checks.

```python
import torch

model = torch.nn.Sequential(
    torch.nn.Flatten(),
    torch.nn.Linear(3 * 64 * 64, 10),
)
optimizer = torch.optim.Adam(model.parameters())

train_steps = 0
idle_steps = 0

for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=0.5):
    for sat in epoch.satellites:
        if sat.power.available and sat.thermal.within_budget:
            # Satellite has power and thermal headroom — train
            batch = torch.randn(8, 3, 64, 64)
            labels = torch.randint(0, 10, (8,))
            loss = torch.nn.functional.cross_entropy(model(batch), labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            train_steps += 1
        else:
            # Eclipse or thermal limit — idle (checkpoint in v0.2)
            idle_steps += 1

total = train_steps + idle_steps
print(f"Training utilization: {train_steps / total * 100:.1f}%")
```

With the default 66-satellite constellation you should see around 70% training
utilization — the rest is lost to eclipse periods and thermal constraints.

## Step 5: Load Real Data

Replace the synthetic batches with the EuroSAT satellite imagery dataset:

```python
from orbit4ml.data import EuroSAT

dataset = EuroSAT(root="./data")  # downloads ~90 MB on first use
loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

print(f"Dataset size: {len(dataset)} images")
print(f"Classes: 10 land use categories")
print(f"Image shape: 3x64x64 RGB (Sentinel-2)")
```

EuroSAT contains 27,000 Sentinel-2 satellite images across 10 land use classes
(residential, industrial, forest, river, etc.), licensed under CC-BY-4.0.

## Next Steps

- Browse the [API Reference](../documentation/index.md) for detailed docs on every class and function
- See the [MVP Example](../examples/index.md) for a complete training script
- Check the [Changelog](../changelog.md) for what shipped in v0.1
