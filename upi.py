import log

def is_upi(description: str):
    return description.upper().startswith("UPI")

def get_upi_username(description: str):
    upiSplits = description.split("/")
    if len(upiSplits) < 4:
        log.exception("Invalid upi description")
    return upiSplits[3]

def update_upi_exports(upiSet: set, exports: list, entryField: str, valueDate: str, exportFields: list):
    data = dict()
    for upiUsername in upiSet:
        data[entryField] = upiUsername
        exports.append(data)