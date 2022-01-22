import csv
from change_psv import change_psv

filepath = input("Enter psv file path: ")

change_psv(filepath)
descriptionField = "Description"

with open(filepath, "r") as csvfile:
    for row in csv.DictReader(csvfile, delimiter='|'):
        pass
        # print(row)