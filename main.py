from comcigan import School
from datetime import datetime
from flask import jsonify, Flask, redirect, request, url_for

import dotenv
import json
import os
import random
import re
import requests

app = Flask(__name__)
dotenv.load_dotenv()
school = School("봉원중학교")

@app.route("/")
def index():
    return "Hello World"

@app.errorhandler(404)
def e404(e):
    return e

@app.route("/api/")
def api():
    return redirect(url_for("index"))

@app.route("/api/test", methods=["POST"])
def api_test():
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕하세요!"
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route("/api/meal", methods=["POST"])
def api_meal():
    req = request.get_json()

    bot_plugin_date = req["action"]["detailParams"]["bot_plugin_date"]["value"]
    bot_date = bot_plugin_date[33:43]

    date = datetime.strptime(bot_date, "%Y-%m-%d")
    days = ["월", "화", "수", "목", "금", "토", "일"]

    res = requests.get(f"https://schoolmenukr.ml/api/middle/B100001561?month={date.month}&allergy=hidden").text
    data = json.loads(res)

    date_food = data["menu"][date.day-1]["lunch"]

    answer_title = f"{date.month}월 {date.day}일 {days[datetime(date.year, date.month, date.day).weekday()-1]}요일"
    answer_desc = re.sub("#|\'|\[|\'|\]", "", str(date_food))

    if answer_desc == "" or answer_desc == None:
        answer_desc = "급식 정보가 없습니다."

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": answer_title,
                        "description": answer_desc,
                        "thumbnail": {
                            "imageUrl": "",
                        }
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.route("/api/weather", methods=["POST"])
def api_weather():
    apikey : str = os.environ["WEATHER_APIKEY"]
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={apikey}&lang=kr&q=Seoul,KR&".format(key=apikey))
    data = json.loads(res.text)

    calc = lambda k: k - 273.15

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "itemCard": {
                        "imageTitle": {
                            "title": "날씨",
                            "description": "현재 서울 봉원중학교의 날씨"
                        },
                        "thumbnail": {
                            "imageUrl": ""
                        },
                        "itemList": [
                            {
                                "title": "날씨",
                                "description": data['weather'][0]['description']
                            },
                            {
                                "title": "기온",
                                "description": f"{round(calc(data['main']['temp']))}° ({round(calc(data['main']['temp_min']))}° & {round(calc(data['main']['temp_max']))}°)"
                            },
                            {
                                "title": "습도",
                                "description": data['main']['humidity']
                            },
                            {
                                "title": "풍속&퐁항",
                                "description": f"{data['wind']['speed']}m/sec & {data['wind']['deg']}°"
                            }
                        ],
                        "itemListAlignment" : "right",
                        "buttons": [
                            {
                                "label": "더보기",
                                "action": "webLink",
                                "webLinkUrl": "https://openweathermap.org/city/1835848"
                            }
                        ],
                        "buttonLayout" : "vertical"
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route("/api/timetable", methods=["POST"])
def api_timetable():
    req = request.get_json()

    bot_school_grade = req["action"]["detailParams"]["bot_school_grade"]["value"]
    bot_school_class = req["action"]["detailParams"]["bot_school_class"]["value"]
    bot_date_week = req["action"]["detailParams"]["bot_date_week"]["value"]

    req_school_grade : int = re.sub(r'[^0-9]', "", bot_school_grade)
    req_school_class : int = re.sub(r'[^0-9]', "", bot_school_class)

    if bot_date_week == "월요일":
        req_date_week = 1
    elif bot_date_week == "화요일":
        req_date_week = 2
    elif bot_date_week == "수요일":
        req_date_week = 3
    elif bot_date_week == "목요일":
        req_date_week = 4
    elif bot_date_week == "금요일":
        req_date_week = 5
    elif bot_date_week == "토요일":
        req_date_week = 6
    elif bot_date_week == "일요일":
        req_date_week = 7

    answer = school[int(req_school_grade)][int(req_school_class)][int(req_date_week) - 1]

    try:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "itemCard": {
                            "imageTitle": {
                                "title": f"{req_school_grade}학년 {req_school_class}반",
                                "description": f"봉원중학교의 시간표"
                            },
                            "head": {
                                "title": f"{bot_date_week} 시간표"
                            },
                            "thumbnail": {
                                "imageUrl": ""
                            },
                            "itemList": [
                                {
                                    "title": "1교시",
                                    "description": f"{answer[0][0]} ({answer[0][2]})"
                                },
                                {
                                    "title": "2교시",
                                    "description": f"{answer[1][0]} ({answer[1][2]})"
                                },
                                {
                                    "title": "3교시",
                                    "description": f"{answer[2][0]} ({answer[2][2]})"
                                },
                                {
                                    "title": "4교시",
                                    "description": f"{answer[3][0]} ({answer[3][2]})"
                                },
                                {
                                    "title": "5교시",
                                    "description": f"{answer[4][0]} ({answer[4][2]})"
                                },
                                {
                                    "title": "6교시",
                                    "description": f"{answer[5][0]} ({answer[5][2]})"
                                },
                                {
                                    "title": "7교시",
                                    "description": f"{answer[6][0]} ({answer[6][2]})"
                                }
                            ],
                            "itemListAlignment" : "left",
                            "buttonLayout" : "vertical"
                        }
                    }
                ]
            }
        }
    except IndexError:
        try:
            res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "itemCard": {
                                "imageTitle": {
                                    "title": f"{req_school_grade}학년 {req_school_class}반",
                                    "description": f"봉원중학교의 시간표"
                                },
                                "head": {
                                    "title": f"{bot_date_week} 시간표"
                                },
                                "thumbnail": {
                                    "imageUrl": ""
                                },
                                "itemList": [
                                    {
                                        "title": "1교시",
                                        "description": f"{answer[0][0]} ({answer[0][2]})"
                                    },
                                    {
                                        "title": "2교시",
                                        "description": f"{answer[1][0]} ({answer[1][2]})"
                                    },
                                    {
                                        "title": "3교시",
                                        "description": f"{answer[2][0]} ({answer[2][2]})"
                                    },
                                    {
                                        "title": "4교시",
                                        "description": f"{answer[3][0]} ({answer[3][2]})"
                                    },
                                    {
                                        "title": "5교시",
                                        "description": f"{answer[4][0]} ({answer[4][2]})"
                                    },
                                    {
                                        "title": "6교시",
                                        "description": f"{answer[5][0]} ({answer[5][2]})"
                                    }
                                ],
                                "itemListAlignment" : "left",
                                "buttonLayout" : "vertical"
                            }
                        }
                    ]
                }
            }
        except IndexError:
            try:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "itemCard": {
                                    "imageTitle": {
                                        "title": f"{req_school_grade}학년 {req_school_class}반",
                                        "description": f"봉원중학교의 시간표"
                                    },
                                    "head": {
                                        "title": f"{bot_date_week} 시간표"
                                    },
                                    "thumbnail": {
                                        "imageUrl": ""
                                    },
                                    "itemList": [
                                        {
                                            "title": "1교시",
                                            "description": f"{answer[0][0]} ({answer[0][2]})"
                                        },
                                        {
                                            "title": "2교시",
                                            "description": f"{answer[1][0]} ({answer[1][2]})"
                                        },
                                        {
                                            "title": "3교시",
                                            "description": f"{answer[2][0]} ({answer[2][2]})"
                                        },
                                        {
                                            "title": "4교시",
                                            "description": f"{answer[3][0]} ({answer[3][2]})"
                                        },
                                        {
                                            "title": "5교시",
                                            "description": f"{answer[4][0]} ({answer[4][2]})"
                                        }
                                    ],
                                    "itemListAlignment" : "left",
                                    "buttonLayout" : "vertical"
                                }
                            }
                        ]
                    }
                }
            except:
                res = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {
                                "itemCard": {
                                    "imageTitle": {
                                        "title": f"{req_school_grade}학년 {req_school_class}반",
                                        "description": f"봉원중학교의 시간표"
                                    },
                                    "head": {
                                        "title": f"{bot_date_week} 시간표"
                                    },
                                    "thumbnail": {
                                        "imageUrl": ""
                                    },
                                    "itemList": [
                                        {
                                            "title": "오류",
                                            "description": f"{req_school_grade}학년 {req_school_class}반 {bot_date_week} 시간표를 찾을 수 없습니다."
                                        }
                                    ],
                                    "itemListAlignment" : "left",
                                    "buttonLayout" : "vertical"
                                }
                            }
                        ]
                    }
                }

    return jsonify(res)

@app.route("/api/plan")
def api_plan():
    # req = request.get_json()

    # bot_plugin_date : str = req["action"]["detailParams"]["bot_plugin_date"]["value"]

    # date = datetime.strptime(str(bot_date), "%Y-%m-%d")

    api_key : str = os.environ["NEIS_APIKEY"]
    if datetime.now().month < 10:
        url = f"https://open.neis.go.kr/hub/SchoolSchedule?KEY={api_key}&Type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7132140&AA_FROM_YMD={datetime.now().year}0{datetime.now().month}01&AA_TO_YMD={datetime.now().year}0{datetime.now().month}32"
    else:
        url = f"https://open.neis.go.kr/hub/SchoolSchedule?KEY={api_key}&Type=json&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7132140&AA_FROM_YMD={datetime.now().year}{datetime.now().month}01&AA_TO_YM={datetime.now().year}{datetime.now().month}32"

    res = requests.get(url).text
    data = json.loads(res)
    #print(re.sub("-?\d+|\'|\?|\'|\.|", "", str(data)))

    print(data["SchoolSchedule"][0]["head"][0]["list_total_count"])
    print(data["SchoolSchedule"][1]["row"][-1])

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "answer_title",
                        "description": "answer_desc",
                        "thumbnail": {
                            "imageUrl": "answer_image",
                            "fixedRatio": True
                        }
                    }
                }
            ]
        }
    }
    return jsonify(data["SchoolSchedule"][1]["row"][-1])

@app.route("/api/quotes", methods=["POST"])
def api_quotes():
    list = [
        '"피할수 없으면 즐겨라." - 로버트 엘리엇',
        '"행복의 문이 하나 닫히면 다른 문이 열린다. 그러나 우리는 종종 닫힌 문을 멍하니 바라보다가 우리를 향해 열린 문을 보지 못하게 된다." - 헬렌 켈러',
        '"나 자신에 대한 자신감을 잃으면온 세상이 나의 적이 된다." - 랄프 왈도 에머슨',
        '"항상 맑으면 사막이 된다. 비가 내리고 바람이 불어야만 비옥한 땅이 된다." - 스페인 속담',
        '"인생은 곱셈이다. 어떤 기회가 와도 내가 제로면 아무런 의미가 없다." - 나카무라 미츠루',
        '"실패란 넘어지는 것이 아니라, 넘어진 자리에 머무는 것이다." - 아네스 안 「프린세스 라 브라바」 中',
        '"사람들은 가치보다 가격에 더 주목한다. 하지만 가격은 당신이 지불하는것이고, 가치는 당신이 얻는것이다." - 워렌 버핏',
        '"거짓말이 달아준 날개로 당신은 얼마든지 멀리 갈 수 있습니다. 그렇지만 다시 돌아오는 길은 어디에도 없어요." - 파울로 코엘료 「마법의 순간」 中',
        '"언제나 인생은 99.9%의 일상과 0.1%의 낯선 순간이었다. 이제 더 이상 기대되는 일이 없다고 슬퍼하기엔 99.9%의 일상이 너무도 소중했다." - 이미예 「달러구트 꿈 백화점 2」 中',
        '"때로는 살아있는 것 조차도 용기가 될 때가 있다." - 세네카',
        '"당신은 아주 짧은 시간에 태도를 바꿀 수 있습니다. 그 짧은 시간에 태도를 바꾸면, 당신은 하루 전체를 바꿀 수 있습니다." - 스펜서 존슨',
        '"사막이 아름다운 것은, 어디엔가 샘을 숨기고 있기 때문이야." - 앙투안 드 생텍쥐페리  「어린왕자」 中',
        '"어른들은 누구나 처음에는 어린이였다. 그러나 그것을 기억하는 어른은 별로 없다." - 앙투안 드 생텍쥐페리  「어린왕자」 中',
        '"바다는 비에 젖지 않는다." - 어니스트 헤밍웨이 「노인과 바다」 中',
        '"새는 알에서 나오기 위해 투쟁한다. 알은 세계이다. 태어나려는 자는 하나의 세계를 깨뜨려야 한다. 새는 신에게로 날아간다. 그 신의 이름은 아프락사스다." - 헤르만 헤세 「데미안」 中',
        '"진짜 문제는 사람들의 마음이다. 그것은 절대로 물리학이나 윤리학의 문제가 아니다." - 아인슈타인',
        '"해야 할 것을 하라. 모든 것은 타인의 행복을 위해서, 동시에 특히 나의 행복을 위해서이다." - 톨스토이',
        '"당신이 인생의 주인공이기 때문이다. 그 사실을 잊지마라. 지금까지 당신이 만들어온 의식적 그리고 무의식적 선택으로 인해 지금의 당신이 있는것이다." - 바바라 홀',
        '"겨울이 오면 봄이 멀지 않으리." - 셸리'
    ]

    res = {
        "version": "1.0",
        "name": "quotes",
        "data": {
            "quote": random.choice(list)
        }
    }

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)