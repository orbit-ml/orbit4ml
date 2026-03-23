# orbit4ml.sim

Physics-based orbital digital twin simulator. Provides satellite constellation
definition, SGP4 orbit propagation, eclipse modeling, thermal constraints,
inter-satellite link availability, and hardware fault injection.

## Quick Example

```python
from datetime import datetime
from orbit4ml.sim import Constellation, DigitalTwin

constellation = Constellation(
    planes=6, sats_per_plane=11, altitude=550, inclination=53.0
)
twin = DigitalTwin(constellation)

for epoch in twin.propagate(start=datetime(2026, 6, 1), hours=1):
    for sat in epoch.satellites:
        print(f"{sat.id}: power={sat.power.available}, thermal={sat.thermal.within_budget}")
```

---

## Constellation

::: orbit4ml.sim.constellation.Constellation
    options:
      show_root_heading: true
      show_source: true
      members_order: source

## DigitalTwin

::: orbit4ml.sim.twin.DigitalTwin
    options:
      show_root_heading: true
      show_source: true
      members_order: source

---

## State Dataclasses

These dataclasses represent the constraint snapshot produced at each simulation
timestep. Downstream modules (`train`, `fed`) consume these to make scheduling
and communication decisions.

### EpochState

::: orbit4ml.sim.types.EpochState
    options:
      show_root_heading: true
      show_source: true

### SatelliteState

::: orbit4ml.sim.types.SatelliteState
    options:
      show_root_heading: true
      show_source: true

### PowerState

::: orbit4ml.sim.types.PowerState
    options:
      show_root_heading: true
      show_source: true

### ThermalState

::: orbit4ml.sim.types.ThermalState
    options:
      show_root_heading: true
      show_source: true

### LinkState

::: orbit4ml.sim.types.LinkState
    options:
      show_root_heading: true
      show_source: true

### FaultState

::: orbit4ml.sim.types.FaultState
    options:
      show_root_heading: true
      show_source: true

---

## Internal Modules

These are used internally by `DigitalTwin` but are documented here for
advanced users who need to call them directly.

### Propagator

::: orbit4ml.sim.propagator.propagate_satellite
    options:
      show_root_heading: true
      show_source: true

### Eclipse Model

::: orbit4ml.sim.eclipse.is_in_eclipse
    options:
      show_root_heading: true
      show_source: true

### Thermal Model

::: orbit4ml.sim.thermal.compute_thermal_state
    options:
      show_root_heading: true
      show_source: true

### Inter-Satellite Links

::: orbit4ml.sim.isl.compute_link_state
    options:
      show_root_heading: true
      show_source: true

### Fault Injection

::: orbit4ml.sim.faults.FaultInjector
    options:
      show_root_heading: true
      show_source: true
      members_order: source

### Sun Position

::: orbit4ml.sim.sun.sun_position_eci
    options:
      show_root_heading: true
      show_source: true
