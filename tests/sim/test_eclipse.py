from orbit4ml.sim.eclipse import is_in_eclipse

EARTH_RADIUS_KM = 6371.0


def test_satellite_on_sunlit_side():
    sun_eci = (1.496e8, 0.0, 0.0)
    sat_eci = (EARTH_RADIUS_KM + 550, 0.0, 0.0)
    assert is_in_eclipse(sat_eci, sun_eci) is False


def test_satellite_behind_earth():
    sun_eci = (1.496e8, 0.0, 0.0)
    sat_eci = (-(EARTH_RADIUS_KM + 550), 0.0, 0.0)
    assert is_in_eclipse(sat_eci, sun_eci) is True


def test_satellite_perpendicular_to_sun():
    sun_eci = (1.496e8, 0.0, 0.0)
    sat_eci = (0.0, EARTH_RADIUS_KM + 550, 0.0)
    assert is_in_eclipse(sat_eci, sun_eci) is False


def test_returns_bool():
    sun_eci = (1.496e8, 0.0, 0.0)
    sat_eci = (EARTH_RADIUS_KM + 550, 0.0, 0.0)
    result = is_in_eclipse(sat_eci, sun_eci)
    assert isinstance(result, bool)
