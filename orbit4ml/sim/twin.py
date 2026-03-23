"""DigitalTwin orchestrator for orbit4ml.sim.

Combines constellation definition, SGP4 propagation, eclipse model,
thermal model, ISL model, and fault injection into a single simulation
loop that yields EpochState snapshots.
"""

from collections.abc import Iterator
from datetime import datetime, timezone

from orbit4ml.sim.constellation import Constellation
from orbit4ml.sim.eclipse import is_in_eclipse
from orbit4ml.sim.faults import FaultInjector
from orbit4ml.sim.isl import compute_link_state
from orbit4ml.sim.propagator import propagate_satellite
from orbit4ml.sim.sun import sun_position_eci
from orbit4ml.sim.thermal import compute_thermal_state
from orbit4ml.sim.types import EpochState, PowerState, SatelliteState

SOLAR_PANEL_WATTS = 500.0


class DigitalTwin:
    """Orbital digital twin simulator.

    Args:
        constellation: The constellation to simulate.
        fault_seed: Random seed for fault injection reproducibility.
    """

    def __init__(self, constellation: Constellation, fault_seed: int = 0) -> None:
        self._constellation = constellation
        self._fault_seed = fault_seed

    def propagate(
        self,
        hours: float,
        step_seconds: float = 60.0,
        start: datetime | None = None,
    ) -> Iterator[EpochState]:
        """Propagate the constellation and yield state snapshots.

        Args:
            hours: Duration to simulate in hours.
            step_seconds: Time step in seconds. Defaults to 60.
            start: Start time (UTC). Defaults to current UTC time.

        Yields:
            EpochState for each timestep.
        """
        if start is None:
            start = datetime.now(tz=timezone.utc).replace(tzinfo=None)

        elements = self._constellation.orbital_elements

        # Pre-propagate all satellite positions
        all_trajectories = {}
        for elem in elements:
            positions = propagate_satellite(
                altitude=elem["altitude"],
                inclination=elem["inclination"],
                raan=elem["raan"],
                true_anomaly=elem["true_anomaly"],
                eccentricity=elem["eccentricity"],
                start=start,
                duration_hours=hours,
                step_seconds=step_seconds,
            )
            all_trajectories[elem["id"]] = positions

        # Create per-satellite fault injectors
        fault_injectors = {
            elem["id"]: FaultInjector(seed=self._fault_seed + i)
            for i, elem in enumerate(elements)
        }

        # Determine number of timesteps from first satellite
        first_key = next(iter(all_trajectories))
        num_steps = len(all_trajectories[first_key])

        for step_idx in range(num_steps):
            positions_at_step = {}
            timestamp = None
            for sat_id, trajectory in all_trajectories.items():
                if step_idx < len(trajectory):
                    ts, x, y, z = trajectory[step_idx]
                    positions_at_step[sat_id] = (x, y, z)
                    timestamp = ts

            if timestamp is None:
                continue

            sun_eci = sun_position_eci(timestamp)

            satellites = []
            for sat_id, pos in positions_at_step.items():
                in_eclipse = is_in_eclipse(pos, sun_eci)

                power = PowerState(
                    available=not in_eclipse,
                    watts=SOLAR_PANEL_WATTS if not in_eclipse else 0.0,
                )

                thermal = compute_thermal_state(in_eclipse)
                links = compute_link_state(sat_id, positions_at_step)
                faults = fault_injectors[sat_id].sample()

                satellites.append(
                    SatelliteState(
                        id=sat_id,
                        position_eci=pos,
                        power=power,
                        thermal=thermal,
                        links=links,
                        faults=faults,
                    )
                )

            yield EpochState(timestamp=timestamp, satellites=satellites)
