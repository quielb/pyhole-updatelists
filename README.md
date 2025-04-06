# Update Pi-Holes lists/domains from remote sources

This project is inspired by jacklul/pihole-updatelists and attempts to replicate that functionality. But it uses the Pihole API rather than the CLI tools.
Refer to jacklul/pihole-updatelists for an overview

> [!WARNING]
> This project is in the vary early stages. It works, but use at your own risk.
> Check issues for what doesn't work.

## Requirements

- Pi-Hole V6
- Python > 3.8

## ENVIRONEMNT VARIABLES

URL environment variables support multiple URLs separated by a space

> [!NOTE]
> String values should be put between `" "`, otherwise weird things might happen.

| Variable | Default | Description |
|----------|---------|-------------|
| COMMENT | "managed by pyhole-updatelists" | Comment string to identify managed entries |
| DOMAINS_ALLOW_URL | "" | Remote list of exact or regex domains to allow |
| DOMAINS_DENY_URL | https://raw.githubusercontent.com/mmotti/pihole-regex/master/regex.list | Remote list of exact or regex domains to allow |
| GROUP_ID  | 0 | Assign lists to group |
| LISTS_ALLOW_URL| "" | Remote list contatining list of block lists to import |
| LISTS_BLOCK_URL| https://v.firebog.net/hosts/lists.php?type=tick | Remote list contatining list of block lists to import |
| LOG_LEVEL | WARNING | Standard Log Levels are available to set output to STDOUT |
| PIHOLE_API_KEY | "" | Either admin password or app password must be provided |
| PIHOLE_URL | "" | |
| UPDATE_GRAVITY | True | Force Gravity to update after updating managed elements |
| VERIFY_SSL | True | Only effects verification of the Pi-Hole cert |

## Current State

- This runs best on a new Pi-Hole instance. It will add new managed elements. It will disable removed managed elements.
- Group assignment doesn't work for any other group than default.
- Check the repo issues to see what is being worked on. If you don't see your problem there, open a new issue.

## Installing

- For now pull the repo.
- Setup a venv.
- Install requirements.
- Setup necessary environment variables.
- Run it with Python -m

There are plans to add other methods of running.
