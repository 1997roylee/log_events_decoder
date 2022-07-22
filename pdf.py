import glob
import json
import re
# import requests

def load_json(file):
    with open(file, 'rb') as f:
        return json.loads(f.read())


def remove_space(value):
    return value.replace(" ", "").replace("\n", "")


def extract_basic_info(data):
    basic_info = data.get("basic")
    result = {}
    for value in basic_info:
        if "性別" in value[0]:
            result["gender"] = remove_space(value[1])
        elif "年齡" in value[0]:
            result["age"] = remove_space(value[1])
        elif "國籍" in value[0]:
            result["nation"] = remove_space(value[1])
        elif "住址" in value[0]:
            result["address"] = remove_space(value[1])
        elif "陽性日期" in value[0]:
            result["tested_at"] = remove_space(value[1])
    return result


def extract_date(date):
    if re.search("\d月.*日", date):
        return re.search("\d月.*日", date).group(0)
    else:
        return None


PERIOD = ["早上", "中午", "晚上", "下午", "早上"]


def extract_timing(timing):
    return timing
    # if timing in PERIOD:
    #     index = PERIOD.index(timing)
    #     return PERIOD[index]
    # elif re.search("\d*:\d*", timing):
    #     return timing
    # else:
    #     return None


def extract_routes(data):
    tables = data.get("routes")
    result = []
    for routes in tables:
        for route in routes:
            date = extract_date(remove_space(route[0]))
            timing = extract_timing(remove_space(route[1]))
            content = remove_space(route[2])
            result.append({
                "date": date,
                "period": timing,
                "content": content
            })

    return result


def load_and_extract_json(file_name):
    if not "618" in file_name:
        return None

    case_id = file_name.replace(".json", "").split("/")[-1]
    
    if case_id == "":
        return None
    
    data = load_json(file_name)
    basic_info = extract_basic_info(data)
    return {
        "gender": basic_info.get('gender'),
        "address": basic_info.get('address'),
        "tested_at": basic_info.get('tested_at'),
        "country": basic_info.get("nation"),
        "case_id": case_id,
        "age": basic_info.get("age"),
        "routes": extract_routes(data)
    }
     

payloads = []
json_file_list = glob.glob("content 2/output/*.json")
for json_file in json_file_list:
    payloads.append(load_and_extract_json(json_file))