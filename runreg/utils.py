#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2019 CERN
#
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

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
        return {"=": str(attribute[0])}
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


def flatten(dictionary, parent_keys=(), seperator="__", skip=()):
    """
    Recursively flatten a dictionary

    :param dictionary: dictionary
    :param parent_keys: list of prefixes seperated by seperator
    :param seperator: parent key seperator
    :param skip: skip keys that contain any of these items
    :return: flattened dictionary
    """
    try:
        key, value = dictionary.popitem()
        if any([item in key for item in skip]):
            return {**flatten(dictionary, parent_keys, seperator, skip)}
        if isinstance(value, dict):
            return {
                **flatten(dictionary, parent_keys, seperator, skip),
                **flatten(value, [*parent_keys, key], seperator, skip),
            }
        return {
            **flatten(dictionary, parent_keys, seperator, skip),
            seperator.join([*parent_keys, key]): value,
        }
    except KeyError:
        return {}


def flatten_runs(runs, skip=("history", "lumisections"), **kwargs):
    return [flatten(run, skip=skip, **kwargs) for run in runs]


def convert_lookup_fields(**field_lookups):
    """
    Converts Django like field lookups to RunRegistry compatible filters.

    See:
    https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups
    """
    kwargs = {}
    for key, value in field_lookups.items():
        if "__" in key:
            new_key, operator = tuple(key.split("__"))
            if new_key in kwargs:
                if type(kwargs[new_key]) != list:
                    existing_value = kwargs[new_key]
                    kwargs[new_key] = [existing_value]
                kwargs[new_key].append((value, operator))
            else:
                kwargs[new_key] = (value, operator)
        else:
            if key in kwargs:
                if type(kwargs[key]) != list:
                    existing_value = kwargs[key]
                    kwargs[key] = [existing_value]
                kwargs[key].append(value)
            else:
                kwargs[key] = value
    return kwargs
