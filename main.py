import csv
from change_psv import change_psv

descriptionField = "Description"

columns = [
    "No.",
    "Transaction ID",
    descriptionField,
]

if __name__ == "__main__":
    filepath = input("Enter psv file path: ")

    change_psv(filepath, columns)

    with open(filepath, "r") as csvfile:
        for row in csv.DictReader(csvfile, delimiter='|'):
            print(row[descriptionField])