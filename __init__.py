"""Entry point of the project."""

import questions as q
from parse_excels import generate_json_from_excels


def main_questionary():
    """First function to be executed in the project."""
    choices = {
        "generate transactions.json from icici excels": generate_transactions_json,
        "start frontend": start_frontend,
        "update transactions.json from marg excels": update_transactions_json,
    }
    a = q.MAIN(choices.keys()).ask()
    print(a)
    choices[a]()


def generate_transactions_json():
    """Initiate generation of transactions json from icici excel files."""
    answers = q.GENERATE_TRANSACTIONS.ask()
    generate_json_from_excels(
        inExcelDirectory=answers["input_excels_directory"],
        outJsonFile=answers["output_file"],
    )


def start_frontend():
    """Start frontend."""
    pass


def update_transactions_json():
    """Update transactions json with the party details from marg excel files."""
    pass


if __name__ == "__main__":
    main_questionary()
