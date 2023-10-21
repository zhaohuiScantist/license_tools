import json

from FossologyFilter.beans import FileScanResult, LicenseScanResult
from FossologyFilter.export import FossologyFilter


def main():
    # 准备过滤器输入数据，这里使用一个Fossology的扫描结果样例
    input_sample_list = []
    file_scan_result = FileScanResult()  # 一个文件的扫描结果
    file_scan_result.origin_text = "扫描的文本文件原文 eg: under mit license, are permitted provided that"
    file_scan_result.filename = "扫描的文本文件名称 eg: license.txt"
    file_scan_result.license_scan_result_list = []
    input_sample_list.append(file_scan_result)

    # 一个扫描结果
    license_scan_result = LicenseScanResult()
    license_scan_result.text = "判断依据文本 eg: under mit license"
    license_scan_result.license = "许可证名称 eg: mit"
    license_scan_result.position_start = "文本在原文中的位置 eg: 7"
    file_scan_result.license_scan_result_list.append(license_scan_result)

    # 第二个扫描结果
    license_scan_result2 = LicenseScanResult()
    license_scan_result2.text = "判断依据文本 eg: are permitted provided that"
    license_scan_result2.license = "许可证名称 eg: mit"
    license_scan_result2.position_start = "文本在原文中的位置 eg: 27"
    file_scan_result.license_scan_result_list.append(license_scan_result2)

    # 调用过滤器进行扫描
    fossology_filter = FossologyFilter()
    filter_result = [i.to_dict() for i in fossology_filter.filter_scan_result(input_sample_list)]

    # 这个用例经过过滤后，应当只有第一个扫描结果被保留下来，第二个扫描结果会被自动过滤掉
    print(json.dumps(filter_result, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
