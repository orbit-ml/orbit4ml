"""Inter-module interface contracts for orbit4ml.sim.

These dataclasses define the objects that cross module boundaries.
The train module (v0.2) consumes SatelliteState for scheduling.
The fed module (v1.0) consumes LinkState for gradient exchange.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PowerState:
    """Solar power state for a satellite at a given timestep.

    Attributes:
        available: True when solar panels are generating power.
        watts: Current solar power output (0.0 during eclipse).
            available is always (watts > 0). Battery backup is not
            modeled in v0.1.
    """

    available: bool
    watts: float


@dataclass
class ThermalState:
    """Thermal constraint state for a satellite at a given timestep.

    Attributes:
        gpu_budget_watts: Maximum GPU power draw before thermal throttle.
        within_budget: Whether the current thermal load is safe.
        radiator_efficiency: Radiator panel efficiency, 0.0 to 1.0.
    """

    gpu_budget_watts: float
    within_budget: bool
    radiator_efficiency: float


@dataclass
class LinkState:
    """Inter-satellite link state for a satellite at a given timestep.

    Attributes:
        active: List of (this_sat_id, peer_sat_id) pairs for active links.
        bandwidth_mbps: Aggregate available bandwidth in Mbps.
    """

    active: list[tuple[str, str]]
    bandwidth_mbps: float


@dataclass
class FaultState:
    """Hardware fault state for a satellite at a given timestep.

    Attributes:
        active: List of active fault type identifiers.
            Valid values: "seu", "thermal_shutdown", "link_failure".
    """

    active: list[str]


@dataclass
class SatelliteState:
    """Per-satellite constraint snapshot at a given timestep.

    Attributes:
        id: Unique satellite identifier (e.g., "plane0-sat3").
        position_eci: (x, y, z) position in km, ECI frame.
        power: Solar power state.
        thermal: Thermal constraint state.
        links: Inter-satellite link state.
        faults: Hardware fault state.
    """

    id: str
    position_eci: tuple[float, float, float]
    power: PowerState
    thermal: ThermalState
    links: LinkState
    faults: FaultState


@dataclass
class EpochState:
    """Constellation state at a single simulation timestep.

    Attributes:
        timestamp: UTC timestamp for this state snapshot.
        satellites: List of per-satellite state snapshots.
    """

    timestamp: datetime
    satellites: list[SatelliteState]
