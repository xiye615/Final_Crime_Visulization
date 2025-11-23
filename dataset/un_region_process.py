import xml.etree.ElementTree as ET
import json
import os

# ===== 你的 XML 路徑 =====
# 使用相對於腳本文件的路徑，確保無論從哪裡運行都能找到文件
script_dir = os.path.dirname(os.path.abspath(__file__))
xml_file = os.path.join(script_dir, "unemployment", "un_rate_region.xml")
json_file = os.path.join(script_dir, "unemployment", "taiwan_unemployment_region.json")

# ===== 欄位對應表 =====
field_map = {
    "項目別_Iterm": "period",
    "臺灣地區_Taiwan_Area": "taiwan_total",
    "北部地區_Northern_region": "north_region",
    "新北市_New_Taipei_City": "new_taipei_city",
    "臺北市_Taipei_City": "taipei_city",
    "桃園市_Taoyuan_City": "taoyuan_city",
    "基隆市_Keelung_City": "keelung_city",
    "新竹市_Hsinchu_City": "hsinchu_city",
    "宜蘭縣_Yilan_County": "yilan_county",
    "新竹縣_Hsinchu_County": "hsinchu_county",
    "中部地區_Central_region": "central_region",
    "臺中市_Taichung_City": "taichung_city",
    "臺中縣_Taichung_County": "taichung_county",
    "苗栗縣_Miaoli_County": "miaoli_county",
    "彰化縣_Changhua_County": "changhua_county",
    "南投縣_Nantou_County": "nantou_county",
    "雲林縣_Yunlin_County": "yunlin_county",
    "南部地區_Southern_region": "south_region",
    "臺南市_Tainan_City": "tainan_city",
    "臺南縣_Tainan_County": "tainan_county",
    "高雄市_Kaohsiung_City": "kaohsiung_city",
    "高雄縣_Kaohsiung_County": "kaohsiung_county",
    "嘉義市_Chiayi_City": "chiayi_city",
    "嘉義縣_Chiayi_County": "chiayi_county",
    "屏東縣_Pingtung_County": "pingtung_county",
    "澎湖縣_Penghu_County": "penghu_county",
    "東部地區_Eastern_region": "east_region",
    "臺東縣_Taitung_County": "taitung_county",
    "花蓮縣_Hualien_County": "hualien_county"
}

# ===== 讀取 XML =====
tree = ET.parse(xml_file)
root = tree.getroot()

json_data = []

for item in root.findall("縣市別失業率"):
    rec = {}

    for xml_field, eng_field in field_map.items():
        el = item.find(xml_field)
        if el is None:
            rec[eng_field] = None
            continue

        txt = el.text.strip() if el.text else ""

        if txt == "" or txt == "-":
            rec[eng_field] = None
        else:
            try:
                rec[eng_field] = float(txt)
            except:
                rec[eng_field] = txt

    json_data.append(rec)

# ===== 輸出 JSON =====
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"轉換完成！共 {len(json_data)} 筆資料")
print(f"JSON 存在: {json_file}")
