"""Configurations

Copyright (c) 2021 Scott Lau
"""
import json
from sys import stdout, stderr
from traceback import print_exc

from githooks.base_check import BaseCheck

# =========================================
#       INSTANCES
# --------------------------------------
try:
    with open("/opt/hook_config/config.json", encoding="utf-8") as cf:
        content = cf.readlines()
        data = json.loads("".join(content))
    config = {fir_key + "." + sec_key: sec_value
              for fir_key, fir_value in data.items()
              if isinstance(fir_value, dict)
              for sec_key, sec_value in fir_value.items()}
except Exception as e:
    stdout.flush()
    print(file=stderr)
    print('{} failed to read configuration: {}'.format(BaseCheck.ERROR_MSG_PREFIX % "ERROR", e), file=stderr)
    print_exc()
