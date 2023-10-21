from FossologyFilter.beans import LicenseScanResult
from FossologyFilter.rules import RuleBaseAbs, RuleResultEnu


class FilterByReferTextLen(RuleBaseAbs):
    """
    合理-文本长度超过30个单词
    适用于一些较长的许可证，例如apache，能命中这条说明几乎命中整个许可证原文段落
    """
    name = "FilterByReferTextLen"

    def __init__(self, min_len: int = 30):
        super().__init__()
        self.min_len = min_len

    def process(self,
                filename: str,
                origin_text: str,
                license_scan_result: LicenseScanResult) -> str:
        token_list = license_scan_result.text.split(" ")
        if len(token_list) >= self.min_len:
            return RuleResultEnu.ACCEPT
        else:
            return RuleResultEnu.NEXT
