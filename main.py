import csv
from collections import defaultdict
from change_psv import change_psv
import log
from upi import is_upi, get_upi_username

descriptionField = "Description"
dateField = "Value Date"

columns = [
    "No.",
    "Transaction ID",
    descriptionField,
    dateField
]

def get_dictionary(upiUser: str, dates: list, type):
    return {
        "Type": type,
        "Entry": upiUser,
        "Party": "",
        "Dates Count": len(dates),
        "Dates": ','.join(dates),
    }

if __name__ == "__main__":
    filepath = input("Enter psv file path: ")

    change_psv(filepath, columns)
    upiDates = defaultdict(list)
    exports = []
    exportPsv = "export.psv"

    with open(filepath, "r") as csvfile:
        for row in csv.DictReader(csvfile, delimiter='|'):
            row[descriptionField] = row[descriptionField].upper()
            if is_upi(row[descriptionField]):
                upiDates[get_upi_username(row[descriptionField])].append(row[dateField])
    for upiUser in upiDates.keys():
        exports.append(get_dictionary(upiUser, upiDates[upiUser], type="UPI"))
    with open(exportPsv, "w", newline="") as f:
        log.info("Exporting data to", exportPsv)
        writer = csv.DictWriter(f, fieldnames=dict(exports[0]).keys(), delimiter="|")
        writer.writeheader()
        writer.writerows(exports)