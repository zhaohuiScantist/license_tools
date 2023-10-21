from FossologyFilter.beans import LicenseScanResult


class RuleResultEnu(object):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    NEXT = "NEXT"


class RuleBaseAbs(object):
    name: str

    def __init__(self):
        pass

    def process(self, filename: str,
                origin_text: str,
                license_scan_result: LicenseScanResult) -> str:
        pass

    pass
