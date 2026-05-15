import argentina
import argentina.shapes
import argentina.geo.shapes


def test_shapes_wrapper_points_to_geo_shapes():
    assert argentina.shapes.provincias is argentina.geo.shapes.provincias
    assert argentina.shapes.departamentos is argentina.geo.shapes.departamentos
