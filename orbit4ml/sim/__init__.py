"""orbit4ml.sim — Orbital digital twin simulator.

Provides physics-based simulation of satellite constellations,
including orbital mechanics, eclipse modeling, thermal constraints,
inter-satellite links, and hardware fault injection.
"""

from orbit4ml.sim.constellation import Constellation
from orbit4ml.sim.twin import DigitalTwin
from orbit4ml.sim.types import (
    EpochState,
    FaultState,
    LinkState,
    PowerState,
    SatelliteState,
    ThermalState,
)

__all__ = [
    "Constellation",
    "DigitalTwin",
    "EpochState",
    "FaultState",
    "LinkState",
    "PowerState",
    "SatelliteState",
    "ThermalState",
]
