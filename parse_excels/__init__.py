"""Entry point to parse_excels."""
import jsonschema
from loguru import logger

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
        # TODO make function handle withdraws also
        is_valid_entry = (
            item["deposit"]
            and excel.is_date_in_range(item["date"])
            and not _is_return_or_reject(item["desc"])
            and not _is_cheque(item["desc"])
        )
        if not is_valid_entry:
            continue
        party_name = _get_party_name(excel, item)
        json_.update(item, {"party_name": party_name})
    json_.save()


def _get_party_name(excel: TransactionsExcelMarg, item: dict):
    if _is_shop_cash_deposit(item["desc"]):
        party_name = c.CASH_ACC
    elif _is_pnb_deposit(item["desc"]):
        party_name = c.PNB_ACC
    else:
        row = excel.row_by_item(item)
        not row and logger.error(f"No row found for item {item}")
        party_name = row["PARTICULARS"] if row else c.SUSPENSE_ACC
    return party_name


def _is_shop_cash_deposit(desc: str):
    return (
        all([s in desc for s in ["-", "BY CASH", "KANPUR", "BIRHANA ROAD"]])
        or desc == "THIRD PARTY DEPOSIT"
    )


def _is_pnb_deposit(desc: str):
    return "1882002100089076-PUNB0025500" in desc


def _is_return_or_reject(desc: str):
    return "REJECT" in desc or "RETURN" in desc


def _is_cheque(desc: str):
    return desc.startswith("CLG")
