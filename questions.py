import questionary
from datetime import date


def MAIN(choices):
    return questionary.select("What to do ?", choices=choices)


def GENERATE_TRANSACTIONS(default_excels_directory: str):
    year_now = date.today().year
    return questionary.form(
        json_file=questionary.path(
            "Path of json file",
            default=f"output_jsons/transactions_{date.today()}.json",
        ),
        input_excels_directory=questionary.path(
            "Path of input excels directory", default=default_excels_directory
        ),
    )


def UPDATE_TRANSACTIONS(default_excels_directory: str):
    year_now = date.today().year
    return questionary.form(
        json_file=questionary.path(
            "Path of json file",
            default=f"output_jsons/transactions_{date.today()}.json",
        ),
        input_excels_directory=questionary.path(
            "Path of input excels directory", default=default_excels_directory
        ),
        start_fy=questionary.select(
            "Start Financial Year: ",
            choices=list(map(lambda d: str(d), range(year_now - 15, year_now + 1))),
            default=str(year_now),
        ),
    )


def COMBINE_JSONS():
    return questionary.form(
        json_files_directory=questionary.path(
            "Path of directory to output json files", default="output_jsons/"
        ),
        output_file=questionary.path(
            "Path of final output json file", default="output_jsons/transactions.json"
        ),
    )
