"""Handle transaction json file."""
import json
import os

import jsonschema
from loguru import logger

from . import constants as c


class TransactionsJson:
    """Handle transactions json file."""

    def __init__(self, jsonFile: str):
        self._jsonFile = jsonFile
        self._json = []
        self._ids = set()
        self.__counter = 0
        if os.path.exists(jsonFile):
            logger.info(f"Reading json file {jsonFile}")
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
            assert isinstance(
                self._json, list
            ), f"self_json is of type {type(self._json)}"
            print(f"Saving {self._jsonFile} with {len(self._json)} items")
            json.dump(self._json, f)

    def add(self, row: dict):
        """Add the row if it already exists."""
        jsonschema.validate(row, c.JSON_SCHEMA)
        if not self.exists(row):
            self._ids.add(row["id"])
            self._json.append(row)
            self._check_and_save()

    def update(self, item: dict, data: dict):
        """Update the row the the data."""
        item.update(data)
        self._check_and_save()

    def items(self):
        """Iterate over the json list."""
        for item in self._json:
            yield item

    def _check_and_save(self):
        self.__counter += 1
        if not self.__counter % 1000:
            self.save()
