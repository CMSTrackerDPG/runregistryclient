operator_dict = {"eq": "=", "lt": "<", "lte": "<=", "gte": ">=", "gt": ">"}


def to_runreg_filter_operator(operator):
    try:
        return operator.replace(operator, operator_dict[operator])
    except KeyError:
        return operator


def attribute_to_run_reg_filter(attribute):
    if type(attribute) == tuple:
        assert len(attribute) <= 2, "Attribute can only be key, value pair"
        if len(attribute) == 2:
            return {to_runreg_filter_operator(attribute[1]): str(attribute[0])}
        return {"=": attribute[0]}
    return {"=": str(attribute)}


def to_runreg_filter(attributes):
    if type(attributes) != list:
        return attribute_to_run_reg_filter(attributes)
    if len(attributes) == 1:
        return attribute_to_run_reg_filter(attributes[0])
    assert len(attributes) <= 3, "Maximum 3 filter attributes are allowed"
    return {"and": [attribute_to_run_reg_filter(attribute) for attribute in attributes]}


def create_filter(**kwargs):
    return {key: to_runreg_filter(value) for key, value in kwargs.items()}


def flatten_run(run):
    """discards lumisection, flattens attributes"""
    flat_run = {}

    for key, value in run.items():
        if type(value) != dict:
            flat_run[key] = value
        elif "lumisections" not in key and key != "run":
            if "value" in value.keys():
                flat_run[key] = value["value"]
                assert "status" not in value.keys()
                assert "comment" not in value.keys()
                assert "cause" not in value.keys()
            else:
                flat_run["{}_status".format(key)] = value["status"]
                flat_run["{}_comment".format(key)] = value["comment"]
                flat_run["{}_cause".format(key)] = value["cause"]

    for key, value in run["run"].items():
        flat_run[key] = value["value"]

    return flat_run


def flatten_runs(runs):
    return [flatten_run(run) for run in runs]
