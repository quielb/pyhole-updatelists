PIHOLE_ACTIONS = {"domains": ["allow", "deny"], "lists": ["allow", "block"]}

ENV_VALUES = {
    "COMMENT": "managed by pyhole-updatelists",
    "DOMAINS_ALLOW_URL": "",
    "DOMAINS_DENY_URL": "https://raw.githubusercontent.com/mmotti/pihole-regex/master/regex.list",  # pylint: disable=C0301
    "GROUP_ID": 0,
    "LISTS_ALLOW_URL": "",
    "LISTS_BLOCK_URL": "https://v.firebog.net/hosts/lists.php?type=tick",
    "LOG_LEVEL": "WARNING",
    "PIHOLE_API_KEY": None,
    "PIHOLE_URL": None,
    "UPDATE_GRAVITY": True,
    "VERIFY_SSL": True,
}
