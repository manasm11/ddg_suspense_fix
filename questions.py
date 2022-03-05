import questionary


def MAIN(choices):
    return questionary.select("What to do ?", choices=choices)


def GENERATE_TRANSACTIONS(default_excels_directory: str):
    return questionary.form(
        json_file=questionary.path(
            "Path of json file", default="output_jsons/transactions.json"
        ),
        input_excels_directory=questionary.path(
            "Path of input excels directory", default=default_excels_directory
        ),
    )
