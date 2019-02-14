from runreg.utils import to_runreg_filter, create_filter


class TestRunRegFilter:
    def test_trivial_case(self):
        attribute = 123456
        assert to_runreg_filter(attribute) == {"=": "123456"}

    def test_gte(self):
        attribute = (123456, "gte")
        assert to_runreg_filter(attribute) == {">=": "123456"}
        attribute = (123456, ">=")
        assert to_runreg_filter(attribute) == {">=": "123456"}

    def test_equal(self):
        attribute = (123456, "=")
        assert to_runreg_filter(attribute) == {"=": "123456"}

    def test_list_single(self):
        attribute = [123456]
        assert to_runreg_filter(attribute) == {"=": "123456"}

        attribute = [(123456, "=")]
        assert to_runreg_filter(attribute) == {"=": "123456"}

    def test_list(self):
        attributes = [(327696, "<="), (327589, ">")]

        assert to_runreg_filter(attributes) == {
            "and": [{"<=": "327696"}, {">": "327589"}]
        }


def test_create_filter():
    actual = create_filter(run_number=123456)
    assert actual == {"run_number": {"=": "123456"}}

    actual = create_filter(run_number=(123456, "lt"))
    assert actual == {"run_number": {"<": "123456"}}

    actual = create_filter(
        run_number=[(123456, "lt"), (234567, ">=")], name=("Cosmics", "like")
    )
    assert actual == {
        "run_number": {"and": [{"<": "123456"}, {">=": "234567"}]},
        "name": {"like": "Cosmics"},
    }

    actual = create_filter(run_number=123456, name=("Cosmics", "like"))
    assert actual == {"run_number": {"=": "123456"}, "name": {"like": "Cosmics"}}
