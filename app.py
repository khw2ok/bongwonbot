from comcigan import School
from bs4 import BeautifulSoup
from datetime import datetime
from flask import jsonify, Flask, request

import dotenv
import json
import os
import re
from pip import main
import requests

app = Flask(__name__)
dotenv.load_dotenv()
school = School("봉원중학교")

@app.route("/")
def index():
    return '''
        <html>
            <head>
                <title>BongwonBot</title>
                <meta http-equiv="refresh" content="0;url=https://bongwonbot.github.io"/>
            </head>
        </html>
    '''

@app.route("/test", methods=["POST"])
def test():
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "answer"
                    }
                }
            ]
        }
    }

    return jsonify(res)

@app.route("/food", methods=["POST"])
def food():
    req = request.get_json()

    bot_plugin_date : str = req["action"]["detailParams"]["bot_plugin_date"]["value"]
    bot_date : str = f"{bot_plugin_date[33]}{bot_plugin_date[34]}{bot_plugin_date[35]}{bot_plugin_date[36]}{bot_plugin_date[37]}{bot_plugin_date[38]}{bot_plugin_date[39]}{bot_plugin_date[40]}{bot_plugin_date[41]}{bot_plugin_date[42]}"

    url = requests.get("https://schoolmenukr.ml/api/middle/B100001561")
    file = url.text
    data = json.loads(file)
    #print(re.sub("-?\d+|\'|\?|\'|\.|", "", str(data)))

    date = datetime.strptime(str(bot_date), "%Y-%m-%d")
    days = ["월", "화", "수", "목", "금", "토", "일"]
    #days[datetime(int(datetime.now().year), int(datetime.now().month), 1).weekday()]
    now_month : int = datetime.now().month

    date_food = data["menu"][date.day-1]["lunch"]

    answer_title = f"{str(now_month)}월 {date.day}일 {days[datetime(date.year, datetime.now().month, date.day).weekday()]}요일"
    answer_desc : str = re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(date_food))
    answer_image = "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/spoon.png"
    print(date.month)
    print(now_month)
    if date.month != str(now_month):
        answer_image = "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/warning.png"
    if answer_desc == "":
        answer_image = "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/warning.png"
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
                            "imageUrl": answer_image,
                            "fixedRatio": True
                        }
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.route("/weather", methods=["POST"])
def weather():
    apikey : str = os.environ["APIKEY"]
    api = f"http://api.openweathermap.org/data/2.5/weather?appid={apikey}&lang=kr&q=Seoul,KR&"

    file = api.format(key=apikey)
    url = requests.get(file)
    data = json.loads(url.text)

    calc = lambda k: k - 273.15

    print(data)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "itemCard": {
                        "imageTitle": {
                            "title": "날씨",
                            "description": "현재 서울의 날씨"
                        },
                        "thumbnail": {
                            "imageUrl": "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/sun_behind_rain_cloud.png",
                            "fixedRatio": True
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

@app.route("/timetable", methods=["POST"])
def timetable():
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
                                "imageUrl": "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/sun_behind_rain_cloud.png",
                                "fixedRatio": True
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
                                    "imageUrl": "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/sun_behind_rain_cloud.png",
                                    "fixedRatio": True
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
                                    "imageUrl": "https://raw.githubusercontent.com/bongwonbot/bongwonbot/main/img/sun_behind_rain_cloud.png",
                                    "fixedRatio": True
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

    return jsonify(res)

@app.route("/virus", methods=["POST"])
def virus():
    url = "http://ncov.mohw.go.kr/"
    
    res = requests.get(url) #covid_virus
    soup = BeautifulSoup(res.text, "html.parser")

    infection = soup.find_all("div", {"class":"box"})[6].text #infection
    death = soup.find_all("div", {"class":"box"})[5].text #death
    infection_day = soup.select("div.occur_graph > table.ds_table > tbody > tr > td > span")[3].text #infection_day
    death_day = soup.select("div.occur_graph > table.ds_table > tbody > tr > td > span")[0].text #death_day
    vaccine1 = soup.find_all("li", {"class":"percent"})[0].text #vaccine1
    vaccine2 = soup.find_all("li", {"class":"percent"})[1].text #vaccine2
    vaccine3 = soup.find_all("li", {"class":"percent"})[2].text #vaccine3

    r_infection = str(re.sub(r"[^0-9]", "", infection).strip("[\']\'")) #infection
    r_death = str(re.sub(r"[^0-9]", "", death).strip("[\']\'")) #death
    r_infection_day = str(re.sub(r"[^0-9]", "", infection_day).strip("[\']\'")) #infection_day
    r_death_day = str(re.findall("-?\d+", death_day)).strip('[\'\']') #death_day

    return {
        "version": "2.0",
        "name": "virus",
        "data": {
            "infection": f"{r_infection}",
            "death": f"{r_death}",
            "infection_day": f"{r_infection_day}",
            "death_day": f"{r_death_day}"
        }
    }

@app.route("/info", methods=["POST"])
def info():
    url = "https://www.schoolinfo.go.kr/ei/ss/Pneiss_b01_s0.do?GS_CD=S010001561"
    
    res = requests.get(url, verify=False) #covid_virus
    soup = BeautifulSoup(res.text, "html.parser")

    students_num = soup.select("div.KeyInfo > div.wrap_box > div.box")[2].text #students_num
    teachers_num = soup.select("div.basicInfo > div.basic_data > span.md")[4].text.split()[2] #students_num

    r_students_num = str(re.sub(r'[^0-9]', "", students_num)) #students_num
    r_teachers_num = re.sub(r'[^0-9]', "", teachers_num) #students_num

    return {
        "version": "1.0",
        "name": "info",
        "data": {
            "students": f"{r_students_num}",
            "teachers": f"{r_teachers_num}"
        }
    }

if __name__ == "__main__":
    #run(selfcheck())
    app.run(debug=True)