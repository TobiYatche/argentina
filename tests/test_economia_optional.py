from argentina.economia import series


def test_require_economia_dependencies_callable():
    assert callable(series._require_economia_dependencies)
