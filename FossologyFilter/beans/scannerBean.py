from typing import List


class LicenseScanResult(object):
    license: str
    text: str
    clean_text: str
    position_start: int

    def to_dict(self):
        return {
            "license": self.license,
            "text": self.text,
            "position_start": self.position_start
        }


class FileScanResult(object):
    filename: str
    origin_text: str
    license_scan_result_list: List[LicenseScanResult]

    def to_dict(self):
        return {
            "filename": self.filename,
            "origin_text": self.origin_text,
            "license_scan_result_list": [i.to_dict() for i in self.license_scan_result_list]
        }
