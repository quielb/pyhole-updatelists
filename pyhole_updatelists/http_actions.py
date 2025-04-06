import logging
import warnings

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning  # type: ignore

_LOGGER = logging.getLogger(__name__)
logging.captureWarnings(True)


def send_it(http_request: dict) -> str:
    _LOGGER.info(
        "Getting ready to internet things (%s) at %s ",
        http_request["method"],
        http_request["url"],
    )
    if not http_request.get("verify", True):
        warnings.simplefilter("ignore", InsecureRequestWarning)
    response = requests.request(
        url=requests.utils.requote_uri(http_request["url"]),  # type: ignore
        method=http_request["method"],
        headers=http_request.get("headers", None),
        json=http_request.get("body", None),
        timeout=http_request.get("timeout", None),
        verify=http_request.get("verify", True),
    )
    if response.status_code != http_request.get("return_code", 200):
        _LOGGER.error(
            "Error attempting http action: %s: %s",
            response.status_code,
            response.text,
        )
        raise SystemExit(1)
    _LOGGER.debug("Data returned from http action: %s", response.text)

    return response.text
