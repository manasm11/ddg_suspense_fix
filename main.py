import csv
from collections import defaultdict
from change_psv import change_psv
import log
from upi import is_upi, get_upi_username, update_upi_exports

descriptionField = "Description"

columns = [
    "No.",
    "Transaction ID",
    descriptionField,
]

def populate_with_dummy_data(exports, exportFields):
    pass

if __name__ == "__main__":
    filepath = input("Enter psv file path: ")

    change_psv(filepath, columns)
    upiSet = set()
    exports = []
    entryField = "Entry"
    partyField = "Party"
    valueDateField = "Value Date"
    exportPsv = "export.psv"
    exportFields = [
        entryField,
        partyField,
        valueDateField,
    ]

    with open(filepath, "r") as csvfile:
        for row in csv.DictReader(csvfile, delimiter='|'):
            row[descriptionField] = row[descriptionField].upper()
            if is_upi(row[descriptionField]):
                upiSet.add(get_upi_username(row[descriptionField]))
    populate_with_dummy_data(exports, exportFields)
    update_upi_exports(upiSet, exports, entryField, valueDateField, exportFields)
    with open(exportPsv, "w", newline="") as f:
        log.info("Exporting data to", exportPsv)
        writer = csv.DictWriter(f, fieldnames=dict(exports[0]).keys(), delimiter="|")
        writer.writeheader()
        writer.writerows(exports)