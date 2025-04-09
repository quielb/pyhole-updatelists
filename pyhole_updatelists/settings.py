from os import getenv
from dotenv import load_dotenv

from .const import ENV_VALUES
from .utils import string_to_bool

global app_config  # pylint: disable=W0604
app_config = {}


def load_settings() -> dict:
    load_dotenv()

    for env_var in ENV_VALUES:
        app_config[env_var] = getenv(env_var, ENV_VALUES.get(env_var, None))
    # clean up format of some of ENV Vairiables
    app_config["LOG_LEVEL"] = app_config["LOG_LEVEL"].upper()
    app_config["UPDATE_GRAVITY"] = string_to_bool(app_config["UPDATE_GRAVITY"])
    app_config["VERIFY_SSL"] = string_to_bool(app_config["VERIFY_SSL"])
    app_config["GROUP_ID"] = int(app_config["GROUP_ID"])
    return app_config
