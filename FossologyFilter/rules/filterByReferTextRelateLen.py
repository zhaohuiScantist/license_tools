import json
from typing import Set

from FossologyFilter.beans import LicenseScanResult
from FossologyFilter.rules import RuleBaseAbs, RuleResultEnu
from FossologyFilter.tools.textTools import clearn_refer_text


class FilterByReferTextRelateLen(RuleBaseAbs):
    """
    合理-文本占了许可证全文的30%以上
    适用于一些较短的许可证，例如zlib，能命中这条说明几乎命中了整个许可证原文
    """
    name = "filterByReferTextRelateLen"

    def __init__(self, relate_rate: float = 0.3):
        super().__init__()
        self.relate_rate = relate_rate

    def process(self,
                filename: str,
                origin_text: str,
                license_scan_result: LicenseScanResult) -> str:
        origin_text_len = len(origin_text)

        refer_text_len = len(license_scan_result.text)
        relate = 1.0 * refer_text_len / origin_text_len
        if relate >= self.relate_rate:
            return RuleResultEnu.ACCEPT
        else:
            return RuleResultEnu.NEXT
