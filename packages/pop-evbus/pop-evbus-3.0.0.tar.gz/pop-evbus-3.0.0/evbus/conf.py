CLI_CONFIG = {
    "ingress_profiles": {"nargs": "*", "group": "evbus"},
    "random": {"action": "store_true", "group": "evbus"},
    # acct options
    "acct_file": {"source": "acct", "os": "ACCT_FILE"},
    "acct_key": {"source": "acct", "os": "ACCT_KEY"},
    # rend options
    "output": {"source": "rend"},
}
CONFIG = {
    "ingress_profiles": {
        "help": "The acct profile names to allowlist.  If none are specified then all profiles will be used",
        "default": [],
    },
    "random": {
        "help": "Run the random number generator that automatically populates the event bus",
        "default": False,
        "type": bool,
    },
}
SUBCOMMANDS = {}
DYNE = {
    "acct": ["acct"],
    "log": ["log"],
    "evbus": ["evbus"],
    "ingress": ["ingress"],
}
