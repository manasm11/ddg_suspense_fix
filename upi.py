import log

def is_upi(description: str):
    if description.upper().startswith("UPI"):
        if len(description.split("/")) >= 4:
            return True
        log.error(f"startswith upi but not sufficient /s {description}")
        return False

def get_upi_username(description: str):
    upiSplits = description.split("/")
    if len(upiSplits) < 4:
        log.exception(f"Invalid upi description: {description}. Skipping...")
    return upiSplits[3]