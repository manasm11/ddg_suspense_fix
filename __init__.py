"""Entry point of the project."""

import os

from parse_excels import generate_json_from_excels

# import csv
# from collections import defaultdict

# from loguru import logger as log

# from parse_excels import change_psv

# descriptionField = "Description"
# dateField = "Value Date"
# valueField = "Transaction Amount(INR)"

# columns = ["No.", "Transaction ID", descriptionField, dateField]


# def get_dictionary(upiUser: str, dateValues: list, type):
#     return {
#         "Type": type,
#         "Entry": upiUser,
#         "Party": "",
#         "Dates Count": len(dateValues),
#         "Dates and Values": ", ".join(dateValues),
#     }


# upiDatesValues = defaultdict(list)
# exports = []
# exportPsv = "export.psv"


def main():
    """First function to be executed in the project."""
    generate_json_from_excels(
        "input_excels", os.path.join("output_jsons", "transactions.json")
    )


if __name__ == "__main__":
    main()
    # filepaths = input("Enter psv file path (file1,file2): ")

    # for filepath in filepaths.split(","):
    #     filepath = filepath.strip()
    #     log.info(f"Processing {filepath}...")
    #     change_psv(filepath, columns)

    #     with open(filepath, "r") as csvfile:
    #         for row in csv.DictReader(csvfile, delimiter="|"):
    #             row[descriptionField] = row[descriptionField].upper()
    #             if is_upi(row[descriptionField]):
    #                 dateValue = "[" + row[dateField] + " : " + row[valueField] + "] "
    #                 upiDatesValues[get_upi_username(row[descriptionField])].append(
    #                     dateValue
    #                 )

    # for upiUser in upiDatesValues.keys():
    #     exports.append(get_dictionary(upiUser, upiDatesValues[upiUser], type="UPI"))

    # with open(exportPsv, "w", newline="") as f:
    #     log.info("Exporting data to", exportPsv)
    #     writer = csv.DictWriter(f, fieldnames=dict(exports[0]).keys(), delimiter="|")
    #     writer.writeheader()
    #     writer.writerows(exports)
