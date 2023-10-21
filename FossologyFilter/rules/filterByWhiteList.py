import json
import os.path
from typing import Set

from FossologyFilter.beans import LicenseScanResult
from FossologyFilter.rules import RuleBaseAbs, RuleResultEnu
from FossologyFilter.tools.textTools import clearn_refer_text, check_is_independent_token


class FilterByWhiteList(RuleBaseAbs):
    name = "FilterByWhiteList"
    key_set: Set[str]

    def __init__(self):
        super().__init__()
        self.key_set = set()
        with open(os.path.join(os.path.dirname(__file__), "../resource/license_name_whitelist.json"), 'r',
                  encoding="utf-8") as fop:
            obj = json.loads(fop.read())
            for k, v in obj.items():
                for vi in v:
                    self.key_set.add(vi)
        print("load white key num: {}".format(len(self.key_set)))

    def process(self,
                filename: str,
                origin_text: str,
                license_scan_result: LicenseScanResult) -> str:
        result = RuleResultEnu.NEXT
        # clean text
        license_scan_result.clean_text = clearn_refer_text(license_scan_result.text)
        for key in self.key_set:
            if key in license_scan_result.clean_text:
                # 进一步判断key在句子中是否是一个单词，而不是一个单词的一部分，例如isc在disclaims中
                is_independent = check_is_independent_token(license_scan_result.clean_text,
                                                            key)
                if is_independent:
                    result = RuleResultEnu.ACCEPT
                    print("file: {} match rule: {} with key: [{}] refer: [{}]".format(filename,
                                                                                      self.name,
                                                                                      key,
                                                                                      license_scan_result.text))
                    break
        return result
