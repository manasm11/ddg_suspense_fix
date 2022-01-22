import os
import log

def confirm_file(filepath):
    if not os.path.isfile(filepath):
        log.error(filepath, "File Not Found")

def change_psv(psv_file):
    confirm_file(psv_file)
    with open(psv_file) as f:
        if f.readline().startswith("Detailed Statement"):
            log.info("Incorrect psv format, trying to correct...")