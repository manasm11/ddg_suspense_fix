import questionary


def MAIN(choices):
    return questionary.select("What to do ?", choices=choices)


GENERATE_TRANSACTIONS = questionary.form(
    output_file=questionary.path(
        "Path of output file", default="output_jsons/transactions.json"
    ),
    input_excels_directory=questionary.path(
        "Path of input icici excels directory", default="input_icici_excels"
    ),
)
