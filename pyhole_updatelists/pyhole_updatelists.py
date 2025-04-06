import logging

from . import settings
from . import http_actions
from . import pihole_api
from .const import PIHOLE_ACTIONS
from .utils import strip_comments

_LOGGER = logging.getLogger(__name__)


def update_lists(element_type: str) -> None:
    _LOGGER.info("Starting the update elements proccess")

    # Get existing managed elements from PiHole
    _LOGGER.info("STEP: Getting existing elements from PiHole")
    managed_elements = {"existing": [], "block": [], "allow": []}
    managed_elements["existing"] = pihole_api.get_managed_element(
        element_type=element_type
    )
    _LOGGER.info("STEP: Got %s existing elements", len(managed_elements["existing"]))

    # Get element (lists/domains) from URL spec'd
    for pihole_action in PIHOLE_ACTIONS[element_type]:
        env_string = f"{element_type.upper()}_{pihole_action.upper()}_URL"
        _LOGGER.info("STEP: Getting external elements to process from %s", env_string)
        for external_url in settings.app_config[env_string].split():
            request = {
                "url": external_url,
                "method": "get",
            }
            response_string = http_actions.send_it(http_request=request)
            response_string = strip_comments(response_string)
            managed_elements[pihole_action] = response_string.splitlines()
            _LOGGER.info(
                "Got %s item(s) from external element %s to process",
                len(managed_elements[pihole_action]),
                external_url,
            )
        # re-arrange existing PiHole elements into a Dict, keyed by address
        # and separate by pihole_action
        existing_elements = {}
        _LOGGER.info(
            "Arranging %s existing %s",
            len(managed_elements["existing"]),
            element_type,
        )
        for managed_element in managed_elements["existing"]:
            key = "address"
            if element_type == "domains":
                key = "domain"
            _LOGGER.debug(
                "Ordering element %s of type %s and action %s",
                managed_element[key],
                element_type,
                managed_element["type"],
            )
            if (
                managed_element["type"] == pihole_action
                and managed_element["comment"] == settings.app_config["COMMENT"]
            ):
                existing_elements[managed_element[key]] = managed_element

        # find new elements to add
        new_elements = list(
            set(managed_elements[pihole_action]) - set(existing_elements.keys())
        )
        _LOGGER.info(
            "STEP: Add %s of type %s and action %s to PiHole",
            len(new_elements),
            element_type,
            pihole_action,
        )
        if len(new_elements) != 0:
            pihole_api.add_managed_element(
                new_elements=new_elements, pihole_action=pihole_action
            )

        # disable removed elements
        disable_elements = list(
            set(existing_elements.keys()) - set(managed_elements[pihole_action])
        )
        for disable_element in disable_elements:
            modify_attributes = {
                "type": pihole_action,
                "enabled": False,
                "groups": [int(settings.app_config["GROUP_ID"])],
                "comment": settings.app_config["COMMENT"],
            }
            pihole_api.update_managed_element(
                modified_element=disable_element, modify_attributes=modify_attributes
            )
