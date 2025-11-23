import xml.etree.ElementTree as ET
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
xml_file = os.path.join(script_dir, "unemployment", "un_rate_age.xml")
json_file = os.path.join(script_dir, "unemployment", "taiwan_unemployment_age.json")

tree = ET.parse(xml_file)
root = tree.getroot()

data = []

for item in root.findall("失業率"):
    record = {}

    # 年月
    ym = item.find("年月別_Year_and_month")
    record["year_month"] = ym.text if ym is not None else None

    # 年齡欄位
    age_fields = {
        "age_15-19_百分比": "15_19",
        "age_20-24_百分比": "20_24",
        "age_25-29_百分比": "25_29",
        "age_30-34_百分比": "30_34",
        "age_35-39_百分比": "35_39",
        "age_40-44_百分比": "40_44",
        "age_45-49_百分比": "45_49",
        "age_50-54_百分比": "50_54",
        "age_55-59_百分比": "55_59",
        "age_60-64_百分比": "60_64",
        "age_65_over_百分比": "65_over",
    }

    for xml_field, eng_field in age_fields.items():
        el = item.find(xml_field)
        if el is None or not el.text or el.text.strip() in ["", "-"]:
            record[eng_field] = None
        else:
            try:
                record[eng_field] = float(el.text.strip())
            except:
                record[eng_field] = el.text.strip()

    data.append(record)

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"轉換完成！共 {len(data)} 筆資料")
print(f"JSON 存在：{json_file}")
