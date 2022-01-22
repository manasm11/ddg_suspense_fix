import csv
from change_psv import change_psv
from upi import is_upi, get_upi_username

descriptionField = "Description"

columns = [
    "No.",
    "Transaction ID",
    descriptionField,
]

if __name__ == "__main__":
    filepath = input("Enter psv file path: ")

    change_psv(filepath, columns)
    upiSet = set()

    with open(filepath, "r") as csvfile:
        for row in csv.DictReader(csvfile, delimiter='|'):
            row[descriptionField] = row[descriptionField].upper()
            if is_upi(row[descriptionField]):
                upiSet.add(get_upi_username(row[descriptionField]))
