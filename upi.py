import log

def is_upi(description: str):
    return description.upper().startswith("UPI")

def get_upi_username(description: str):
    upiSplits = description.split("/")
    if len(upiSplits) < 4:
        log.exception("Invalid upi description")
    return upiSplits[3]