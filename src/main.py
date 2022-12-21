from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
app = FastAPI(
    title="bongwonbot",
    description="Chatbot, <b>@bongwonbot</b> for bongwon middle school.",
    version="221221",
    docs_url="/",
    terms_of_service="http://b1bot.kro.kr",
    contact={"email": "official@b1bot.kro.kr"},
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"}
)

from comcigan import School
school = School("봉원중학교")

from datetime import datetime

import dotenv
dotenv.load_dotenv()

import json
data = json.load(open("data.json"))

import os
import re
import requests

def checkDB(req):
    if req["userRequest"]["user"]["id"] not in data:
        data[req["userRequest"]["user"]["id"]] = {
            "config": {
                "grade": None,
                "class": None
            }
        }
        json.dump(data, open("data.json", "w"), indent=4)

@app.post("/api/welcome", description="Welcoming message.", response_class=JSONResponse)
async def api_welcome(request:Request):
    req = await request.json()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "안녕하세요",
                        "description": "저는 봉원중학교의 생활을 더욱 편리하게 만들어줄 \"봉원중학교 챗봇\"입니다.",
                        "thumbnails": {
                            "imageUrl": ""
                        }
                    }
                }
            ]
        }
    }
    return res

@app.post("/api/config", description="Change user config.", response_class=JSONResponse)
async def api_config(request:Request):
    req = await request.json()
    checkDB(req)
    params_bot_school_grade = req["action"]["detailParams"]["bot_school_grade"]["value"]
    params_bot_school_class = req["action"]["detailParams"]["bot_school_class"]["value"]
    res_school_grade = re.sub(r"[^0-9]", "", params_bot_school_grade)
    res_school_class = re.sub(r"[^0-9]", "", params_bot_school_class)
    data[req["userRequest"]["user"]["id"]] = {
        "usage": 0,
        "config": {
            "grade": int(res_school_grade),
            "class": int(res_school_class)
        }
    }
    json.dump(data, open("data.json", "w"), indent=4)
    res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": "설정이 완료 되었습니다.",
                            "description": f"{res_school_grade}학년 {res_school_class}반으로 설정이 완료되었습니다.",
                            "thumbnails": {
                                "imageUrl": ""
                            }
                        }
                    }
                ]
            }
        }
    return res

@app.post("/api/info", description="Get user info.", response_class=JSONResponse)
async def api_info(request:Request):
    req = await request.json()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "itemCard": {
                        "head": {
                            "title": req["userRequest"]["user"]["id"],
                        },
                        "itemList": [
                            {
                                "title": "학급",
                                "description": f'{data[req["userRequest"]["user"]["id"]]["config"]["grade"]}학년 {data[req["userRequest"]["user"]["id"]]["config"]["class"]}반'
                            }
                        ],
                        "itemListAlignment" : "right"
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

@app.post("/api/meal", description="Check the school meal.", response_class=JSONResponse)
async def api_meal(request:Request):
    req = await request.json()
    params_sys_plugin_date = req["action"]["detailParams"]["sys_plugin_date"]["value"]
    req_plugin_date = datetime.strptime(params_sys_plugin_date[33:43], "%Y-%m-%d")
    res_days = ["월", "화", "수", "목", "금", "토", "일"]
    res_api = requests.get(f"https://schoolmenukr.ml/api/middle/B100001561?year={req_plugin_date.year}&month={req_plugin_date.month}&date={req_plugin_date.day}&allergy=hidden").text
    res_api_data = json.loads(res_api)
    res_meal = re.sub("#|\"|\[|\"|\]", "", str(res_api_data["menu"][0]["lunch"]))
    if res_meal == "" or res_meal == None:
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
    return res

@app.post("/api/timetable", description="Check the class's timetable", response_class=JSONResponse)
async def api_timetable(request:Request):
    req = await request.json()
    checkDB(req)
    if "bot_school_grade" in req["action"]["detailParams"] and "bot_school_class" in req["action"]["detailParams"]:
        res_school_grade = int(re.findall("\d+", req["action"]["detailParams"]["bot_school_grade"]["value"])[0])
        res_school_class = int(re.findall("\d+", req["action"]["detailParams"]["bot_school_class"]["value"])[0])
        res_timetable = school[res_school_grade][res_school_class]
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
                                    "title": f"{res_school_grade}학년 {res_school_class}반 월요일",
                                    "description": f"{res_timetable_class[0][0]}\n{res_timetable_class[0][1]}\n{res_timetable_class[0][2]}\n{res_timetable_class[0][3]}\n{res_timetable_class[0][4]}\n{res_timetable_class[0][5]}\n{res_timetable_class[0][6]}\n{res_timetable_class[0][7]}".strip("\nNone"),
                                    "thumbnail": {
                                        "imageUrl": "",
                                    }
                                },
                                {
                                    "title": f"{res_school_grade}학년 {res_school_class}반 화요일",
                                    "description": f"{res_timetable_class[1][0]}\n{res_timetable_class[1][1]}\n{res_timetable_class[1][2]}\n{res_timetable_class[1][3]}\n{res_timetable_class[1][4]}\n{res_timetable_class[1][5]}\n{res_timetable_class[1][6]}\n{res_timetable_class[1][7]}".strip("\nNone"),
                                    "thumbnail": {
                                        "imageUrl": "",
                                    }
                                },
                                {
                                    "title": f"{res_school_grade}학년 {res_school_class}반 수요일",
                                    "description": f"{res_timetable_class[2][0]}\n{res_timetable_class[2][1]}\n{res_timetable_class[2][2]}\n{res_timetable_class[2][3]}\n{res_timetable_class[2][4]}\n{res_timetable_class[2][5]}\n{res_timetable_class[2][6]}\n{res_timetable_class[2][7]}".strip("\nNone"),
                                    "thumbnail": {
                                        "imageUrl": "",
                                    }
                                },
                                {
                                    "title": f"{res_school_grade}학년 {res_school_class}반 목요일",
                                    "description": f"{res_timetable_class[3][0]}\n{res_timetable_class[3][1]}\n{res_timetable_class[3][2]}\n{res_timetable_class[3][3]}\n{res_timetable_class[3][4]}\n{res_timetable_class[3][5]}\n{res_timetable_class[3][6]}\n{res_timetable_class[3][7]}".strip("\nNone"),
                                    "thumbnail": {
                                        "imageUrl": "",
                                    }
                                },
                                {
                                    "title": f"{res_school_grade}학년 {res_school_class}반 금요일",
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
    res_school_grade = data[req["userRequest"]["user"]["id"]]["config"]["grade"]
    res_school_class = data[req["userRequest"]["user"]["id"]]["config"]["class"]
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
        return res
    res_timetable = school[res_school_grade][res_school_class]
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
                                "title": f"{res_school_grade}학년 {res_school_class}반 월요일",
                                "description": f"{res_timetable_class[0][0]}\n{res_timetable_class[0][1]}\n{res_timetable_class[0][2]}\n{res_timetable_class[0][3]}\n{res_timetable_class[0][4]}\n{res_timetable_class[0][5]}\n{res_timetable_class[0][6]}\n{res_timetable_class[0][7]}".strip("\nNone"),
                                "thumbnail": {
                                    "imageUrl": "",
                                }
                            },
                            {
                                "title": f"{res_school_grade}학년 {res_school_class}반 화요일",
                                "description": f"{res_timetable_class[1][0]}\n{res_timetable_class[1][1]}\n{res_timetable_class[1][2]}\n{res_timetable_class[1][3]}\n{res_timetable_class[1][4]}\n{res_timetable_class[1][5]}\n{res_timetable_class[1][6]}\n{res_timetable_class[1][7]}".strip("\nNone"),
                                "thumbnail": {
                                    "imageUrl": "",
                                }
                            },
                            {
                                "title": f"{res_school_grade}학년 {res_school_class}반 수요일",
                                "description": f"{res_timetable_class[2][0]}\n{res_timetable_class[2][1]}\n{res_timetable_class[2][2]}\n{res_timetable_class[2][3]}\n{res_timetable_class[2][4]}\n{res_timetable_class[2][5]}\n{res_timetable_class[2][6]}\n{res_timetable_class[2][7]}".strip("\nNone"),
                                "thumbnail": {
                                    "imageUrl": "",
                                }
                            },
                            {
                                "title": f"{res_school_grade}학년 {res_school_class}반 목요일",
                                "description": f"{res_timetable_class[3][0]}\n{res_timetable_class[3][1]}\n{res_timetable_class[3][2]}\n{res_timetable_class[3][3]}\n{res_timetable_class[3][4]}\n{res_timetable_class[3][5]}\n{res_timetable_class[3][6]}\n{res_timetable_class[3][7]}".strip("\nNone"),
                                "thumbnail": {
                                    "imageUrl": "",
                                }
                            },
                            {
                                "title": f"{res_school_grade}학년 {res_school_class}반 금요일",
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
