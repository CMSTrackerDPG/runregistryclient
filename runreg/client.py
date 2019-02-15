import json
import requests
from runreg.utils import create_filter, flatten_runs

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
    payload = _create_payload(**kwargs)
    return requests.post(url, headers=headers, data=payload).json()


def get(flat=False, workspace="tracker", **kwargs):
    initial_response = _get_page(0, workspace, **kwargs)
    page_count = initial_response.get("pages")
    resources = initial_response.get("datasets")

    for page_number in range(1, page_count):
        page = _get_page(page_number, **kwargs)
        resources.extend(page.get("datasets"))

    if flat:
        return flatten_runs(resources)
    return resources
