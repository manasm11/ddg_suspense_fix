import csv

filepath = input("Enter psv file path: ")

descriptionField = "Description"

with open(filepath, "rb") as csvfile:
    for row in csv.DictReader(csvfile, dialect='piper'):
        print(row[descriptionField])