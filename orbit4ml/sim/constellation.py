"""Constellation definition for orbit4ml.sim.

Defines orbital parameters and generates Keplerian elements for each
satellite in a Walker-delta constellation pattern.
"""

EARTH_RADIUS_KM = 6371.0


class Constellation:
    """Defines a Walker-delta satellite constellation.

    Args:
        planes: Number of orbital planes.
        sats_per_plane: Number of satellites per plane.
        altitude: Orbital altitude in km above Earth's surface.
        inclination: Orbital inclination in degrees.
    """

    def __init__(
        self,
        planes: int,
        sats_per_plane: int,
        altitude: float,
        inclination: float,
    ) -> None:
        self.planes = planes
        self.sats_per_plane = sats_per_plane
        self.altitude = altitude
        self.inclination = inclination

    @property
    def total_satellites(self) -> int:
        return self.planes * self.sats_per_plane

    @property
    def satellite_ids(self) -> list[str]:
        return [
            f"plane{p}-sat{s}"
            for p in range(self.planes)
            for s in range(self.sats_per_plane)
        ]

    @property
    def semi_major_axis(self) -> float:
        return EARTH_RADIUS_KM + self.altitude

    @property
    def orbital_elements(self) -> list[dict]:
        elements = []
        for p in range(self.planes):
            raan = (360.0 / self.planes) * p
            for s in range(self.sats_per_plane):
                true_anomaly = (360.0 / self.sats_per_plane) * s
                elements.append(
                    {
                        "id": f"plane{p}-sat{s}",
                        "altitude": self.altitude,
                        "inclination": self.inclination,
                        "raan": raan,
                        "true_anomaly": true_anomaly,
                        "eccentricity": 0.0,
                    }
                )
        return elements
