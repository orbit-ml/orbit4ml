"""Hardware fault injection for orbit4ml.sim.

Simulates single-event upsets (SEUs), thermal shutdowns, and link
failures using configurable per-step probabilities.
"""

import random

from orbit4ml.sim.types import FaultState

DEFAULT_SEU_RATE = 0.001
DEFAULT_THERMAL_SHUTDOWN_RATE = 0.0005
DEFAULT_LINK_FAILURE_RATE = 0.002


class FaultInjector:
    """Stochastic fault injector for satellite hardware.

    Args:
        seed: Random seed for reproducibility.
        seu_rate: Probability of a single-event upset per timestep.
        thermal_shutdown_rate: Probability of thermal shutdown per timestep.
        link_failure_rate: Probability of link failure per timestep.
    """

    def __init__(
        self,
        seed: int = 0,
        seu_rate: float = DEFAULT_SEU_RATE,
        thermal_shutdown_rate: float = DEFAULT_THERMAL_SHUTDOWN_RATE,
        link_failure_rate: float = DEFAULT_LINK_FAILURE_RATE,
    ) -> None:
        self._rng = random.Random(seed)
        self._rates = {
            "seu": seu_rate,
            "thermal_shutdown": thermal_shutdown_rate,
            "link_failure": link_failure_rate,
        }

    def sample(self) -> FaultState:
        active = []
        for fault_type, rate in self._rates.items():
            if self._rng.random() < rate:
                active.append(fault_type)
        return FaultState(active=active)
