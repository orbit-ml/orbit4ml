from orbit4ml.sim.constellation import Constellation


def test_constellation_creation():
    c = Constellation(planes=6, sats_per_plane=11, altitude=550, inclination=53.0)
    assert c.planes == 6
    assert c.sats_per_plane == 11
    assert c.altitude == 550
    assert c.inclination == 53.0


def test_satellite_count():
    c = Constellation(planes=6, sats_per_plane=11, altitude=550, inclination=53.0)
    assert c.total_satellites == 66


def test_satellite_ids():
    c = Constellation(planes=2, sats_per_plane=3, altitude=550, inclination=53.0)
    ids = c.satellite_ids
    assert len(ids) == 6
    assert "plane0-sat0" in ids
    assert "plane1-sat2" in ids


def test_orbital_elements():
    c = Constellation(planes=2, sats_per_plane=3, altitude=550, inclination=53.0)
    elements = c.orbital_elements
    assert len(elements) == 6
    for elem in elements:
        assert elem["altitude"] == 550
        assert elem["inclination"] == 53.0
    plane0_raans = {e["raan"] for e in elements if e["id"].startswith("plane0")}
    plane1_raans = {e["raan"] for e in elements if e["id"].startswith("plane1")}
    assert len(plane0_raans) == 1
    assert len(plane1_raans) == 1
    assert plane0_raans != plane1_raans


def test_single_satellite():
    c = Constellation(planes=1, sats_per_plane=1, altitude=408, inclination=51.6)
    assert c.total_satellites == 1
    elems = c.orbital_elements
    assert elems[0]["inclination"] == 51.6
    assert elems[0]["altitude"] == 408
