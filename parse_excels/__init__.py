"""Entry point to parse_excels."""
import jsonschema

from . import constants as c
from .transactions_excel import TransactionsExcel
from .transactions_json import TransactionsJson


def generate_json_from_excels(inExcelDirectory: str, outJsonFile: str):
    """Convert excel row to a json file."""
    excel = TransactionsExcel(inExcelDirectory)
    json_ = TransactionsJson(outJsonFile)
    for row in excel.rows():
        jsonschema.validate(row, c.ROW_SCHEMA)
        json_.add(row)
    json_.save()
