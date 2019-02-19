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

import json
import requests
from runreg.utils import create_filter, flatten_runs, convert_lookup_fields

url_format = (
    "https://cmsrunregistry.web.cern.ch/api/datasets/{workspace}/editable/{page}/"
)

PAGE_SIZE = 25


def _create_payload(page_size=PAGE_SIZE, **kwargs):
    return json.dumps(
        {"page_size": page_size, "sortings": [], "filter": create_filter(**kwargs)}
    )


def _get_page(page, workspace, **kwargs):
    url = url_format.format(workspace=workspace.lower(), page=page)
    headers = {"Content-type": "application/json"}
    payload = _create_payload(**(convert_lookup_fields(**kwargs)))
    return requests.post(url, headers=headers, data=payload).json()


def get(flat=False, workspace="tracker", **kwargs):
    initial_response = _get_page(0, workspace, **kwargs)

    if "err" in initial_response:
        raise ValueError(initial_response["err"])

    page_count = initial_response["pages"]
    resources = initial_response["datasets"]

    for page_number in range(1, page_count):
        page = _get_page(page_number, workspace, **kwargs)
        resources.extend(page.get("datasets"))

    if flat:
        return flatten_runs(resources)
    return resources
