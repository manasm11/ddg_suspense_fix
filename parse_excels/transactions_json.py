"""Handle transaction json file."""
import json
import os

import jsonschema

from . import constants as c


class TransactionsJson:
    """Handle transactions json file."""

    def __init__(self, jsonFile: str):
        self._jsonFile = jsonFile
        self._json = []
        self._ids = set()
        if os.path.exists(jsonFile):
            print(f"Reading json file {jsonFile}")
            with open(jsonFile, "r") as f:
                self._json = json.load(f)
                assert isinstance(self._json, list), f"Invalid json file: '{jsonFile}'"
        for row in self._json:
            jsonschema.validate(row, c.JSON_SCHEMA)

    def exists(self, row: dict) -> bool:
        """Check if the row exists."""
        return row["id"] in self._ids

    def save(self):
        """Save the updated json."""
        with open(self._jsonFile, "w") as f:
            json.dump(self._json, f)

    def add(self, row):
        """Add the row if it already exists."""
        jsonschema.validate(row, c.JSON_SCHEMA)
        if not self.exists(row):
            self._ids.add(row["id"])
            self._json.append(row)
