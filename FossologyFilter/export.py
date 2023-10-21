from typing import List

from . import beans
from . import rules
from .beans import FileScanResult


class FossologyFilter(object):
    rule_list: List[rules.RuleBaseAbs]

    def __init__(self):
        self.rule_list = [
            rules.FilterByWhiteList(),
            # rules.FilterByReferTextRelateLen(relate_rate=0.4),
            # rules.FilterByReferTextLen(min_len=40),
        ]

    def filter_scan_result(self, all_file_scan_result_list: List[beans.FileScanResult]):
        new_file_scan_result_list = []
        # 依次遍历所有的文件扫描结果
        for file_scan_result in all_file_scan_result_list:
            new_file_scan_result = FileScanResult()
            new_file_scan_result.origin_text = file_scan_result.origin_text
            new_file_scan_result.filename = file_scan_result.filename
            new_file_scan_result.license_scan_result_list = []
            # 依次遍历所有的refer text
            for refer_result in file_scan_result.license_scan_result_list:
                # 依次遍历所有的规则
                default_rule_result = rules.RuleResultEnu.REJECT
                final_rule_result = default_rule_result
                for rule in self.rule_list:
                    rule_result = rule.process(filename=file_scan_result.filename,
                                               origin_text=file_scan_result.origin_text,
                                               license_scan_result=refer_result)
                    if rule_result in [rules.RuleResultEnu.ACCEPT, rules.RuleResultEnu.REJECT]:
                        # 规则命中
                        final_rule_result = rule_result
                        # 中断规则链
                        break
                if final_rule_result == rules.RuleResultEnu.ACCEPT:
                    # 只有当规则命中结果为ACCEPT的时候，才保留这条扫描结果
                    new_file_scan_result.license_scan_result_list.append(refer_result)
                    pass
            if len(new_file_scan_result.license_scan_result_list) > 0:
                # 只有当前文件有扫描结果时才返回许可证扫描结果
                new_file_scan_result_list.append(new_file_scan_result)
        return new_file_scan_result_list
