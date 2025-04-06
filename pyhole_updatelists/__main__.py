import logging
import sys


from . import settings
from .const import PIHOLE_ACTIONS
from .pihole_api import get_auth_token, deauth, update_gravity
from .pyhole_updatelists import update_lists


_LOGGER = logging.getLogger(__name__)


def main() -> int:

    settings.load_settings()
    logging.basicConfig(
        level=settings.app_config.get("LOG_LEVEL", logging.ERROR).upper()
    )

    # If PiHole API key or URL not specified then bail.
    if settings.app_config.get("PIHOLE_API_KEY", None) is None:
        _LOGGER.error("Missing PiHole API key, exiting.")
        return 1
    if settings.app_config.get("PIHOLE_URL", None) is None:
        _LOGGER.error("Missing PiHole URL, exiting.")
        return 1

    # attempt to connect to PiHole API and get an auth token
    get_auth_token()
    for element in PIHOLE_ACTIONS.keys():  # pylint: disable=C0201
        update_lists(element_type=element)
    if settings.app_config["UPDATE_GRAVITY"]:
        update_gravity()
    deauth()
    return 0


if __name__ == "__main__":
    sys.exit(main())
