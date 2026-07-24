"""
© Battelle Memorial Institute 2026
Made available under the MIT License (MIT)

BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.
"""

import yaml
from pathlib import Path
from collections import defaultdict

with open(Path(__file__).parent / "config.yaml") as f:
    CONFIG = yaml.safe_load(f)

LOCATIONS = CONFIG["locations"]

# Build indexes
INDEX = defaultdict(dict)

def _register(index_name, obj_key, category):
    values = category.get(obj_key)
    if values is None:
        return
    if not isinstance(values, list):
        values = [values]
    for v in values:
        INDEX[index_name][v] = category

# Build reverse lookups once
for cat in LOCATIONS:
    _register("full_name", "full_name", cat)
    _register("short_name", "short_name", cat)
    _register("fema_key", "fema_keys", cat)
    _register("nsi_key", "nsi_keys", cat)

def lookup(key_from, value_from, key_to):
    """
    Example:
        lookup("fema_key", "Education", "short_name") --> "edu"
    """
    category = INDEX[key_from].get(value_from)
    if category is None:
        return None
    return category.get(key_to)
