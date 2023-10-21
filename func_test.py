import json
import os.path
import traceback

import pandas as pd

from FossologyFilter.beans import FileScanResult, LicenseScanResult
from FossologyFilter.export import FossologyFilter
from sklearn.metrics import classification_report

if __name__ == '__main__':
    # 载入400个SPDX许可证的Fossology扫描数据，并进行过滤
    spdx_test_scan_input_dir = "data/fossologyFilterTestData/term_testdata"
    spdx_test_fossology_scan_result_file = "data/fossologyFilterTestData/term_testdata_fso_result.json"
    spdx_test_fossology_scan_result = json.loads(open(spdx_test_fossology_scan_result_file).read())

    # 载入德赛的60个OSS代码的Fossology扫描数据，并进行过滤
    desai_test_scan_result_file = "data/fossologyFilterTestData/德赛部分软件许可证fossology扫描结果_带有文本来源_20230810_过滤了图像文件.xlsx"
    desai_test_scan_result = pd.read_excel(desai_test_scan_result_file)
    desai_test_scan_result.fillna(method="ffill", inplace=True)

    # 载入人工标注的refer判断依据标注
    refer_label_file = "data/fossologyFilterTestData/Fossology扫描结果refer文本分析.xlsx"
    refer_label_df = pd.read_excel(refer_label_file)
    refer_label_df["合理"] = refer_label_df["合理"].replace(9, 1)

    # 在其Fossology结果上进行过滤
    fossology_filter = FossologyFilter()
    input_sample_list = []
    origin_refer_list = []
    # SPDX
    for filename, origin_scan_result in spdx_test_fossology_scan_result.items():
        file_path = os.path.join(spdx_test_scan_input_dir, filename)
        print("file:{}".format(file_path))
        file_content = open(file_path).read()
        file_scan_result = FileScanResult()
        file_scan_result.origin_text = file_content
        file_scan_result.filename = filename
        file_scan_result.license_scan_result_list = []
        for i in origin_scan_result:
            license_scan_result = LicenseScanResult()
            license_scan_result.text = i["text"]
            origin_refer_list.append(license_scan_result.text)
            license_scan_result.license = i["license"]
            license_scan_result.position_start = i["position"]
            file_scan_result.license_scan_result_list.append(license_scan_result)
        input_sample_list.append(file_scan_result)

    # 德赛
    for i in desai_test_scan_result["refer text"].tolist():
        file_scan_result = FileScanResult()
        file_scan_result.origin_text = "content"
        file_scan_result.filename = "filename"
        file_scan_result.license_scan_result_list = []
        license_scan_result = LicenseScanResult()
        license_scan_result.text = i
        origin_refer_list.append(license_scan_result.text)
        license_scan_result.license = "license"
        license_scan_result.position_start = 0
        file_scan_result.license_scan_result_list.append(license_scan_result)
        input_sample_list.append(file_scan_result)

    filter_result = [i.to_dict() for i in fossology_filter.filter_scan_result(input_sample_list)]

    # 过滤后被标记为可用的refer列表
    filter_usable_refer_list = []
    for i in filter_result:
        for k in i["license_scan_result_list"]:
            filter_usable_refer_list.append(k["text"])
    filter_usable_refer_set = set(filter_usable_refer_list)

    # 计算原始可用率以及过滤后的可用率
    compare_list = []
    error_count = 0
    for i in origin_refer_list:
        try:
            compare_list.append({
                "refer text": i,
                "origin_usable": refer_label_df[refer_label_df["refer"] == i]["合理"].tolist()[0],
                "filter_usable": 1 if i in filter_usable_refer_set else 0,
            })
        except Exception:
            print("error on:{}".format(i))
            traceback.print_exc()
            error_count += 1

    print("error_count:{}".format(error_count))

    metric_df = pd.DataFrame.from_records(compare_list)
    metric_df.to_csv("metric_df.csv")

    data_size = metric_df.shape[0]
    origin_usable_size = metric_df[metric_df["origin_usable"] == 1].shape[0]
    origin_usable_rate = origin_usable_size / data_size
    print("refer文本共计 {} 条，原始可用率: {}".format(data_size, origin_usable_rate))

    print("过滤后的refer数量{}".format(metric_df[metric_df["filter_usable"] == 1].shape[0]))
    print(classification_report(y_true=metric_df["origin_usable"].tolist(),
                                y_pred=metric_df["filter_usable"].tolist()))
    pass
