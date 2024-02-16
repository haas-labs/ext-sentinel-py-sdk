STATUS_CODES = {
    0: "Failed",
    1: "Success",
    2: "Awaiting Others",
    3: "Accepted",
    4: "Lower Limit or Insufficient",
    5: "Receiver Action Requested",
    6: "Upper Limit",
}


def eth_status_description(status_code: int) -> str:
    """
    returns status description by status code
    """
    if status_code in STATUS_CODES:
        return STATUS_CODES[status_code]
    else:
        return f"Status_{status_code}"
