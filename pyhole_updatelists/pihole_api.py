import json
import logging

import validators

from . import settings
from .http_actions import send_it
from .utils import is_valid_regex

_LOGGER = logging.getLogger(__name__)

API_CALLS = {
    "add_domains": {
        "api": "/api/domains/{type}/{kind}",
        "method": "post",
        "return_code": 201,
    },
    "add_lists": {"api": "/api/lists", "method": "post", "return_code": 201},
    "get_lists": {"api": "/api/lists", "method": "get", "return_code": 200},
    "get_domains": {"api": "/api/domains", "method": "get", "return_code": 200},
    "modify_domians": {
        "api": "/api/domains/{type}/{kind}/{domain}",
        "method": "put",
        "return_code": 200,
    },
    "modify_lists": {"api": "/api/lists/{}", "method": "put", "return_code": 200},
}


def add_managed_element(new_elements: list, pihole_action: str) -> None:
    _LOGGER.info("Adding new elements to PiHole")
    # Setup for a element type of List
    api_type = "add_lists"
    url = f"{settings.app_config["PIHOLE_URL"]}{API_CALLS[api_type]["api"]}"
    http_body = {
        "type": pihole_action,
        "comment": settings.app_config["COMMENT"],
        "groups": [int(settings.app_config["GROUP_ID"])],
        "enabled": True,
        "address": new_elements,
    }
    # Override a few things if element type is Domain
    if not validators.url(new_elements[0]):
        api_type = "add_domains"
        domain_kind = "exact"
        if is_valid_regex(new_elements[0]):
            domain_kind = "regex"
        url = f"{settings.app_config["PIHOLE_URL"]}{API_CALLS[api_type]["api"].format(type=pihole_action, kind=domain_kind)}"  # pylint: disable=C0301
        del http_body["address"]
        del http_body["type"]
        http_body["domain"] = new_elements
    _LOGGER.info(
        "STEP: %s action: %s qty: %s", api_type, pihole_action, len(new_elements)
    )

    http_request = {
        "url": url,
        "method": API_CALLS[api_type]["method"],
        "headers": {"X-FTL-SID": settings.app_config.get("AUTH_TOKEN")},
        "body": http_body,
        "return_code": API_CALLS[api_type]["return_code"],
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    response = send_it(http_request=http_request)
    response = json.loads(response)
    if len(response["processed"]["errors"]) > 0:
        _LOGGER.error("Adding new elements had the following error(s)")
        for response_error in response["processed"]["errors"]:
            _LOGGER.error("%s %s", response_error["item"], response_error["error"])


def deauth() -> None:
    _LOGGER.info("Closing auth session with Pihole")
    http_request = {
        "url": f"{settings.app_config["PIHOLE_URL"]}/api/auth",
        "method": "delete",
        "headers": {"X-FTL-SID": settings.app_config.get("AUTH_TOKEN")},
        "return_code": 204,
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    send_it(http_request=http_request)


def get_auth_token() -> None:
    _LOGGER.info(
        "Getting auth token from PiHole server: %s", settings.app_config["PIHOLE_URL"]
    )
    http_request = {
        "url": f"{settings.app_config["PIHOLE_URL"]}/api/auth",
        "method": "post",
        "return_code": 200,
        "body": {"password": settings.app_config["PIHOLE_API_KEY"]},
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    response = json.loads(send_it(http_request=http_request))

    if not response["session"]["valid"]:
        _LOGGER.error(
            "Unable to authenticate to PiHole server: %s", response["message"]
        )
        raise SystemExit(1)
    settings.app_config["AUTH_TOKEN"] = response["session"]["sid"]


def get_managed_element(element_type: str) -> list:
    _LOGGER.info("Getting managed element from PiHole server of type %s", element_type)
    api_type = f"get_{element_type}"
    request = {
        "url": f"{settings.app_config["PIHOLE_URL"]}{API_CALLS[api_type]["api"]}",
        "method": API_CALLS[api_type]["method"],
        "headers": {"X-FTL-SID": settings.app_config.get("AUTH_TOKEN")},
        "return_code": API_CALLS[api_type]["return_code"],
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    response = json.loads(send_it(http_request=request))

    return response[element_type]


def update_gravity() -> None:
    _LOGGER.info("Closing auth session with Pihole")
    http_request = {
        "url": f"{settings.app_config["PIHOLE_URL"]}/api/action/gravity",
        "method": "post",
        "headers": {"X-FTL-SID": settings.app_config.get("AUTH_TOKEN")},
        "return_code": 200,
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    send_it(http_request=http_request)


def update_managed_element(modified_element: str, modify_attributes: dict) -> None:
    _LOGGER.info("Modifing element %s")
    api_type = "modify_domains"
    url = ""
    if validators.url(modified_element):
        api_type = "modify_lists"
        url = f"{settings.app_config["PIHOLE_URL"]}{API_CALLS[api_type]["api"].format(modified_element)}"  # pylint: disable=C0301
    _LOGGER.info("STEP: %s item: %s", api_type, modified_element)
    request = {
        "url": url,
        "method": API_CALLS[api_type]["method"],
        "headers": {"X-FTL-SID": settings.app_config.get("AUTH_TOKEN")},
        "body": modify_attributes,
        "return_code": API_CALLS[api_type]["return_code"],
        "verify": settings.app_config.get("VERIFY_SSL", True),
    }
    send_it(http_request=request)
