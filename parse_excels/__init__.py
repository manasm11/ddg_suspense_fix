"""Entry point to parse_excels."""
import jsonschema

from . import constants as c
from .transactions_excel_icici import TransactionsExcelIcici
from .transactions_excel_marg import TransactionsExcelMarg
from .transactions_json import TransactionsJson


def generate_json_from_icici_excels(inExcelDirectory: str, outJsonFile: str):
    """Parse over icici excels rows and generate json."""
    excel = TransactionsExcelIcici(inExcelDirectory)
    json_ = TransactionsJson(outJsonFile)
    for row in excel.rows():
        jsonschema.validate(row, c.JSON_SCHEMA)
        json_.add(row)
    json_.save()


def update_transactions_json_from_marg_excels(inExcelDirectory: str, jsonFile: str):
    """Parse over marg excels rows and update transactions json."""
    excel = TransactionsExcelMarg(inExcelDirectory)
    json_ = TransactionsJson(jsonFile)
    for item in json_.items():
        jsonschema.validate(item, c.JSON_SCHEMA)
        row = excel.row_by_item(item)
        assert row, f"Row not found for {item}"
        json_.update(item, {"party_name": row["party_name"]})
    json_.save()
