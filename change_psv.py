import os
import log

def confirm_file(filepath):
    if not os.path.isfile(filepath):
        log.error(filepath, "File Not Found")

def update_isUselessRow(isUselessRow, line):
    if not isUselessRow:
        return isUselessRow
    headRow = "No.|Transaction ID|Value Date|Txn Posted"
    if headRow in line:
        return False
    return isUselessRow

def correct_file(filepath):
    finalFileRows = []
    isUselessRow = True
    with open(filepath) as f:
        for line in f.readlines():
            isUselessRow = update_isUselessRow(isUselessRow, line)
            if isUselessRow or is_line_empty(line):
                continue
            finalFileRows.append(line)
    with open(filepath, "w") as f:
        f.writelines(finalFileRows)
    log.info("Corrected the file", filepath)

def is_line_empty(line):
    return not line or not str(line).strip()

def change_psv(psv_file):
    confirm_file(psv_file)
    with open(psv_file) as f:
        if f.readline().startswith("Detailed Statement"):
            log.info("Incorrect psv format, trying to correct...")
            correct_file(psv_file)