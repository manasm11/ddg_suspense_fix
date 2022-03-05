"""Entry point of the project."""

from loguru import logger

import questions as q
from parse_excels import (
    generate_json_from_icici_excels,
    update_transactions_json_from_marg_excels,
)

logger.add("logs/{time}.log", level="DEBUG")
logger.add("logs/warns_{time}.log", level="WARNING")
logger.add("logs/errors_{time}.log", level="ERROR")


def main_questionary():
    """First function to be executed in the project."""
    choices = {
        "generate transactions.json from icici excels": generate_transactions_json,
        "update transactions.json from marg excels": update_transactions_json,
        "start frontend": start_frontend,
    }
    answer = q.MAIN(choices.keys()).ask()
    if answer is None:
        print("B-Bye !!!")
        exit(0)
    logger.debug(f"User selected {answer}")
    choices[answer]()


def generate_transactions_json():
    """Initiate generation of transactions json from icici excel files."""
    answers = q.GENERATE_TRANSACTIONS("input_icici_excels").ask()
    generate_json_from_icici_excels(
        inExcelDirectory=answers["input_excels_directory"],
        outJsonFile=answers["json_file"],
    )


def update_transactions_json():
    """Update transactions json with the party details from marg excel files."""
    answers = q.GENERATE_TRANSACTIONS("input_marg_excels").ask()
    update_transactions_json_from_marg_excels(
        inExcelDirectory=answers["input_excels_directory"],
        jsonFile=answers["json_file"],
    )


def start_frontend():
    """Start frontend."""
    pass


if __name__ == "__main__":
    main_questionary()
