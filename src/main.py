from comcigan import School
school = School("봉원중학교")

from datetime import datetime, timedelta
from flask import Flask, jsonify, request, session
app = Flask(__name__)
# app.config["SERVER_NAME"] = "b1bot.kro.kr"

import dotenv
dotenv.load_dotenv()

import json
data = json.load(open("src/data.json"))

import os
import random
import re
import requests

def checkDB(req):
    if req["userRequest"]["user"]["id"] not in data:
        data[req["userRequest"]["user"]["id"]] = {
            "name": "미설정",
            "grade": None,
            "class": None
        }
        json.dump(data, open("src/data.json", "w"), indent=4)
    if "name" not in data[req["userRequest"]["user"]["id"]]:
        data[req["userRequest"]["user"]["id"]]["name"] = "미설정"
        json.dump(data, open("src/data.json", "w"), indent=4)

@app.errorhandler(Exception)
def error(e):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "오류 발생",
                        "description": f"아래와 같은 오류가 발생했습니다.\n\"{e}\"",
                        "thumbnails": {
                            "imageUrl": ""
                        }
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.post("/api/welcome")
def api_welcome():
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "안녕하세요",
                                "description": "저는 봉원중학교의 생활을 더욱 편리하게 만들어줄 \"봉원중학교 챗봇\"입니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                }
                            },
                            {
                                "title": "이용 약관",
                                "description": "서비스 이용 시 이용약관에 동의한 걸로 간주됩니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "약관 확인하기",
                                        "webLinkUrl": "https://github.com/khw2ok/bongwonbot/blob/main/docs/privacy.md"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "도움말 확인하기",
                    "action": "block",
                    "blockId": "6137f4f6dae81c4da823012e"
                }
            ]
        }
    }
    return jsonify(res)

@app.post("/api/fallback")
def api_fallback():
    req = request.get_json()
    res_text = ["이해하지 못 했어요. 🤨", "이해하지 못 했어요. 😥", "모르는 내용이에요. 🤨", "모르는 내용이에요. 😥", "아직 답변해드릴 수 없는 내용이에요. 😥"]
    check_req = [
        ["급식", "긊", "그시", "끄ㅃ씪", "끕식", "급싴", "급시", "rmqtlr"],
        ["시간표", "시반", "간표", "표", "시간", "시깐표", "tlrksvy", "tlrks"],
        ["도움말", "도움", "도와", "움말", "또움", "동움", "ehdnaakf", "ehdna"]
    ]
    if req["userRequest"]["utterance"] in check_req[0]:
        res_text = ["혹시 \"급식\"을 찾으시나요?"]
    if req["userRequest"]["utterance"] in check_req[1]:
        res_text = ["혹시 \"시간표\"를 찾으시나요?"]
    if req["userRequest"]["utterance"] in check_req[2]:
        res_text = ["혹시 \"도움말\"를 찾으시나요?"]
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": random.choice(res_text)
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "도움말 확인하기",
                    "action": "block",
                    "blockId": "6137f4f6dae81c4da823012e"
                }
            ]
        }
    }
    if req["userRequest"]["utterance"] in check_req[0]:
        res["template"]["quickReplies"][0] = {
            "label": "급식 확인하기",
            "action": "block",
            "blockId": "612db350ecdd173dd6816b65"
        }
    if req["userRequest"]["utterance"] in check_req[1]:
        res["template"]["quickReplies"][0] = {
            "label": "시간표 확인하기",
            "action": "block",
            "blockId": "61efe491e3907f6a2b567319"
        }
    return jsonify(res)

@app.post("/api/help")
def api_help():
    req = request.get_json()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "아래와 같은 기능들을 이용할 수 있어요."
                    }
                },
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "도움말 문서 확인",
                                "description": "도움말 문서를 확인합니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "문서 확인하기",
                                        "webLinkUrl": "https://github.com/khw2ok/bongwonbot/blob/main/docs/howto.md"
                                    }
                                ]
                            },
                            {
                                "title": "약관 확인",
                                "description": "이용 약관을 확인합니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "약관 확인하기",
                                        "webLinkUrl": "https://github.com/khw2ok/bongwonbot/blob/main/docs/policy.md"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "급식 확인",
                                "description": "해당 날짜의 급식을 알려줍니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "급식 확인하기",
                                        "blockId": "612db350ecdd173dd6816b65"
                                    }
                                ]
                            },
                            {
                                "title": "시간표 확인",
                                "description": "해당 학급의 이번 주 시간표를 알려줍니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "시간표 확인하기",
                                        "blockId": "61efe491e3907f6a2b567319"
                                    }
                                ]
                            },
                            {
                                "title": "내 정보",
                                "description": "이용자의 정보를 알려줍니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": "내 정보 확인하기",
                                        "blockId": "635d100ea3aa951a6a31cedb"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.post("/api/config")
def api_config():
    req = request.get_json()
    checkDB(req)
    params_sys_text = req["action"]["params"]["sys_text"]
    params_bot_school_grade = req["action"]["detailParams"]["bot_school_grade"]["value"]
    params_bot_school_class = req["action"]["detailParams"]["bot_school_class"]["value"]
    res_school_grade = re.sub(r"[^0-9]", "", params_bot_school_grade)
    res_school_class = re.sub(r"[^0-9]", "", params_bot_school_class)
    data[req["userRequest"]["user"]["id"]] = {
        "name": params_sys_text,
        "grade": int(res_school_grade),
        "class": int(res_school_class)
    }
    json.dump(data, open("src/data.json", "w"), indent=4)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "설정이 완료 되었습니다.",
                            "description": f"안녕하세요, {params_sys_text}님!\n{res_school_grade}학년 {res_school_class}반으로 설정이 완료되었습니다.",
                            "thumbnails": {
                                "imageUrl": ""
                            }
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label": "내 정보 확인하기",
                        "action": "block",
                        "blockId": "635d100ea3aa951a6a31cedb"
                    }
                ]
            }
        }
    return jsonify(res)

@app.post("/api/info")
def api_info():
    req = request.get_json()
    checkDB(req)
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "itemCard": {
                        "head": {
                            "title": "내 정보",
                        },
                        "itemList": [
                            {
                                "title": "이름",
                                "description": data[req["userRequest"]["user"]["id"]]["name"]
                            },
                            {
                                "title": "학급",
                                "description": f'{data[req["userRequest"]["user"]["id"]]["grade"]}학년 {data[req["userRequest"]["user"]["id"]]["class"]}반'
                            },
                            {
                                "title": "아이디",
                                "description": req["userRequest"]["user"]["id"]
                            }
                        ],
                        "itemListAlignment" : "right"
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "내 정보 변경하기",
                    "action": "block",
                    "blockId": "635c946c7d0dc94f4d60f044"
                }
            ]
        }
    }
    return jsonify(res)

@app.post("/api/meal")
def api_meal():
    req = request.get_json()
    params_sys_plugin_date = json.loads(req["action"]["params"]["sys_plugin_date"])["value"]
    res_days = ["월", "화", "수", "목", "금", "토", "일"]
    req_plugin_date = datetime.strptime(params_sys_plugin_date, "%Y-%m-%d")
    data = json.loads(requests.get(f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={os.environ['NEIS_APIKEY']}&Type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7132140&MLSV_YMD={req_plugin_date.strftime('%Y%m%d')}").text)
    try:
        data_set = (data["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"]).replace("<br/>", "\n")
        data_reg = re.sub("[#]|[a-zA-Z0-9_]|[ ]|[.]", "", data_set).replace("()", "") 
        res_meal = f"{data_reg}\n{data['mealServiceDietInfo'][1]['row'][0]['CAL_INFO']}"
    except KeyError:
        res_meal = "급식 정보가 없습니다."
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"{req_plugin_date.year}년 {req_plugin_date.month}월 {req_plugin_date.day}일 {res_days[datetime(req_plugin_date.year, req_plugin_date.month, req_plugin_date.day).weekday()]}요일",
                        "description": f"{res_meal}",
                        "thumbnail": {
                            "imageUrl": "",
                        }
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.post("/api/timetable")
def api_timetable():
    req = request.get_json()
    checkDB(req)
    def normalRes(v, w):
        try:
            res_timetable = school[v][w]
            res_timetable_class = [[], [], [], [], []]
            for i in range(8):
                for j in range(5):
                    try:
                        res_timetable_class[j].append(f"{i+1}교시 - {res_timetable[j][i][1]} ({res_timetable[j][i][2]})")
                    except IndexError:
                        res_timetable_class[j].append(None)
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "carousel": {
                                "type": "basicCard",
                                "items": [
                                    {
                                        "title": f"{v}학년 {w}반 월요일",
                                        "description": f"{res_timetable_class[0][0]}\n{res_timetable_class[0][1]}\n{res_timetable_class[0][2]}\n{res_timetable_class[0][3]}\n{res_timetable_class[0][4]}\n{res_timetable_class[0][5]}\n{res_timetable_class[0][6]}\n{res_timetable_class[0][7]}".strip("\nNone"),
                                        "thumbnail": {
                                            "imageUrl": "",
                                        }
                                    },
                                    {
                                        "title": f"{v}학년 {w}반 화요일",
                                        "description": f"{res_timetable_class[1][0]}\n{res_timetable_class[1][1]}\n{res_timetable_class[1][2]}\n{res_timetable_class[1][3]}\n{res_timetable_class[1][4]}\n{res_timetable_class[1][5]}\n{res_timetable_class[1][6]}\n{res_timetable_class[1][7]}".strip("\nNone"),
                                        "thumbnail": {
                                            "imageUrl": "",
                                        }
                                    },
                                    {
                                        "title": f"{v}학년 {w}반 수요일",
                                        "description": f"{res_timetable_class[2][0]}\n{res_timetable_class[2][1]}\n{res_timetable_class[2][2]}\n{res_timetable_class[2][3]}\n{res_timetable_class[2][4]}\n{res_timetable_class[2][5]}\n{res_timetable_class[2][6]}\n{res_timetable_class[2][7]}".strip("\nNone"),
                                        "thumbnail": {
                                            "imageUrl": "",
                                        }
                                    },
                                    {
                                        "title": f"{v}학년 {w}반 목요일",
                                        "description": f"{res_timetable_class[3][0]}\n{res_timetable_class[3][1]}\n{res_timetable_class[3][2]}\n{res_timetable_class[3][3]}\n{res_timetable_class[3][4]}\n{res_timetable_class[3][5]}\n{res_timetable_class[3][6]}\n{res_timetable_class[3][7]}".strip("\nNone"),
                                        "thumbnail": {
                                            "imageUrl": "",
                                        }
                                    },
                                    {
                                        "title": f"{v}학년 {w}반 금요일",
                                        "description": f"{res_timetable_class[4][0]}\n{res_timetable_class[4][1]}\n{res_timetable_class[4][2]}\n{res_timetable_class[4][3]}\n{res_timetable_class[4][4]}\n{res_timetable_class[4][5]}\n{res_timetable_class[4][6]}\n{res_timetable_class[4][7]}".strip("\nNone"),
                                        "thumbnail": {
                                            "imageUrl": "",
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "학급 설정하기",
                            "action": "block",
                            "blockId": "635c946c7d0dc94f4d60f044"
                        }
                    ]
                }
            }
            return res
        except IndexError:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": f"{v}학년 {w}반",
                                "description": "시간표 정보가 없습니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                }
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "학급 설정하기",
                            "action": "block",
                            "blockId": "635c946c7d0dc94f4d60f044"
                        }
                    ]
                }
            }
            return res
    if "bot_school_grade" in req["action"]["params"] and "bot_school_class" in req["action"]["params"]:
        res_school_grade = int(req["action"]["params"]["bot_school_grade"][0])
        res_school_class = int(req["action"]["params"]["bot_school_class"][0])
        return jsonify(normalRes(res_school_grade, res_school_class))
    else:
        res_school_grade = data[req["userRequest"]["user"]["id"]]["grade"]
        res_school_class = data[req["userRequest"]["user"]["id"]]["class"]
        if res_school_grade == None or res_school_class == None:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "basicCard": {
                                "title": "오류",
                                "description": "현재 학급이 설정되어 있지 않습니다. 아래 버튼을 통해 학급 설정 이후 이용해 주시기 바랍니다.",
                                "thumbnails": {
                                    "imageUrl": ""
                                },
                                "buttons": [
                                    {
                                        "label": "학급 설정하기",
                                        "action": "block",
                                        "blockId": "635c946c7d0dc94f4d60f044"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
            return jsonify(res)
        return jsonify(normalRes(res_school_grade, res_school_class))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)