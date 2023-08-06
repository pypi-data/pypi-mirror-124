import re
from pathlib import Path
from typing import Union

import click


class RegexType(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        try:
            return re.compile(value, re.IGNORECASE)
        except re.error as e:
            self.fail(
                "Regex error: " + str(e),
                param,
                ctx,
            )


def get_craft_name(filename: Union[str, Path], default: str) -> str:
    """Return the craft name (or a default) from the filename."""
    m = re.search("([^_]+)_", Path(filename).name)
    if not m:
        return default
    return m.group(1)
