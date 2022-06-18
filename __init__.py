"""Entry point of the project."""

import os

from loguru import logger

import questions as q
from parse_excels import (
    generate_json_from_icici_excels,
    update_transactions_json_from_marg_excels,
)
from combine_jsons import combine_all_json_files

logger.add("logs/{time}.log", level="DEBUG")
# logger.add("logs/warns_{time}.log", level="WARNING")
# logger.add("logs/errors_{time}.log", level="ERROR")


def main_questionary():
    """First function to be executed in the project."""
    choices = {
        "generate transactions.json from icici excels": generate_transactions_json,
        "update transactions.json from marg excels": update_transactions_json,
        "combine and clean jsons": combine_jsons,
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


def combine_jsons():
    """Combine all json files and remove entries without "party_name" field"""
    answers = q.COMBINE_JSONS().ask()
    logger.debug(f"Answers: {answers}")
    combine_all_json_files(
        jsons_directory=answers["json_files_directory"],
        output_json=answers["output_file"],
    )


def start_frontend():
    """Start frontend."""
    os.system("./run _ui")


if __name__ == "__main__":
    main_questionary()
