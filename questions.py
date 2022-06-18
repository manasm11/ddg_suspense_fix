import questionary
from datetime import date

def MAIN(choices):
    return questionary.select("What to do ?", choices=choices)


def GENERATE_TRANSACTIONS(default_excels_directory: str):
    return questionary.form(
        json_file=questionary.path(
            "Path of json file", default=f"output_jsons/transactions_{date.today()}.json"
        ),
        input_excels_directory=questionary.path(
            "Path of input excels directory", default=default_excels_directory
        ),
    )

def COMBINE_JSONS():
    return questionary.form(
        json_files_directory=questionary.path("Path of directory to output json files", default="output_jsons/"),
        output_file=questionary.path("Path of final output json file", default="output_jsons/transactions.json")
    ) 
