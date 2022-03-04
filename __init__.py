"""Entry point of the project."""

import os

from parse_excels import generate_json_from_excels


def main():
    """First function to be executed in the project."""
    generate_json_from_excels(
        "input_excels", os.path.join("output_jsons", "transactions.json")
    )


if __name__ == "__main__":
    main()
