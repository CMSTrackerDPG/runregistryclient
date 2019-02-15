from runreg.utils import to_runreg_filter, create_filter, flatten


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

    actual = create_filter(run_number=(123456,))
    assert actual == {"run_number": {"=": "123456"}}

    actual = create_filter(
        run_number=[(123456, "lt"), (234567, ">=")], name=("Cosmics", "like")
    )
    assert actual == {
        "run_number": {"and": [{"<": "123456"}, {">=": "234567"}]},
        "name": {"like": "Cosmics"},
    }

    actual = create_filter(run_number=123456, name=("Cosmics", "like"))
    assert actual == {"run_number": {"=": "123456"}, "name": {"like": "Cosmics"}}


class TestFlatten:
    def test_trivial(self):
        assert {"a": 1} == flatten({"a": 1})

    def test_trivial_two(self):
        dictionary = {"a": 1, "b": 2}
        flat_dict = flatten(dictionary)
        assert {"a": 1, "b": 2} == flat_dict

    def test_one_level(self):
        dictionary = {"a": {"b": 1}}
        assert {"a__b": 1} == flatten(dictionary)

    def test_one_level_two(self):
        dictionary = {"a": {"b": 1, "c": 2}}
        assert {"a__b": 1, "a__c": 2} == flatten(dictionary)

    def test_two_level(self):
        dictionary = {"a": {"b": {"c": 1}}}
        assert {"a__b__c": 1} == flatten(dictionary)

    def test_two_level_two(self):
        dictionary = {"a": {"b": {"c": 1}, "d": 2}}
        assert {"a__b__c": 1, "a__d": 2} == flatten(dictionary)

    def test_mixed(self):
        dictionary = {"a": "1", "b": {"c": 2, "d": "3"}, "e": {"f": {"g": "4"}}}

        expected = {"a": "1", "b__c": 2, "b__d": "3", "e__f__g": "4"}
        actual = flatten(dictionary)
        assert actual == expected

    def test_skip(self):
        dictionary = {"a": 1, "b": 2}
        flat_dict = flatten(dictionary, skip="b")
        assert {"a": 1} == flat_dict

    def test_skip_nested(self):
        dictionary = {"a": "1", "b": {"c": 2, "d": "3"}, "e": {"f": {"g": "4"}}}

        expected = {"a": "1", "b__d": "3", "e__f__g": "4"}
        actual = flatten(dictionary, skip=["c"])
        assert actual == expected
