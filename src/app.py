from comcigan import School
from bs4 import BeautifulSoup
from datetime import datetime
from flask import jsonify, Flask, render_template, request

import dotenv
import json
import os
import re
import requests

app = Flask(__name__)
school = School("봉원중학교")
dotenv.load_dotenv()

@app.route("/")
def index():
    return render_template("index.html")

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
    print(bot_plugin_date)

    url = requests.get("https://schoolmenukr.ml/api/middle/B100001561")
    file = url.text
    data = json.loads(file)
    #print(re.sub("-?\d+|\'|\?|\'|\.|", "", str(data)))

    try:
        date = datetime.strptime(bot_plugin_date, "%Y-%m-%d")
    except:
        date = datetime.now()
    days = ["월", "화", "수", "목", "금", "토", "일"]
    #days[datetime(int(datetime.now().year), int(datetime.now().month), 1).weekday()]
    print(date)

    now_year : int = datetime.now().year
    now_month : int = datetime.now().month
    now_day : int = datetime.now().day

    print(date.day)

    date_food = data["menu"][date.day-1]["lunch"]

    answer_desc : str = re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(date_food))

    if answer_desc == "":
        answer_desc = "급식 정보가 없습니다."

    print(date_food)
    print(answer_desc)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"{date.month}월 {date.day}일 {days[datetime(now_year, now_month, now_day).weekday()]}요일",
                        "description": answer_desc,
                        "thumbnail": {
                            "imageUrl": "../spoon"
                        }
                    }
                }
            ]
        }
    }
    return jsonify(res)

@app.route("/weather", methods=["POST"])
def weather():
    url1 = "https://weather.naver.com/today/09620575"
    url2 = "https://weather.naver.com/air/09620575"
    
    res1 = requests.get(url1) #weather
    soup1 = BeautifulSoup(res1.text, "html.parser")

    res2 = requests.get(url2) #air
    soup2 = BeautifulSoup(res2.text, "html.parser")

    #weather data from naver weather
    weather = soup1.find_all("span", {"class":"weather"})[0].text #weather
    temperature = soup1.find_all("div", {"class":"weather_now"})[0].text #temperature
    max_temperature = soup1.find_all("span", {"class":"highest"})[0].text #max_temperature
    min_temperature = soup1.find_all("span", {"class":"lowest"})[0].text #min_temperature
    precipitation_percentage1 = soup1.find_all("span", {"class":"rainfall"})[0].text #precipitation_percentage1
    precipitation_percentage2 = soup1.find_all("span", {"class":"rainfall"})[1].text #precipitation_percentage2
    ultraviolet_ray = soup1.find_all("strong", {"class":"level_dsc"})[0].text #ultraviolet_ray

    #air data from naver weather
    microdust_grade = soup2.find_all("span", {"class":"grade _cnPm10Grade"})[0].text #microdust_grade
    microdust_value = soup2.find_all("span", {"class":"value _cnPm10Value"})[0].text #microdust_value
    ultra_microdust_grade = soup2.find_all("span", {"class":"grade _cnPm25Grade"})[0].text #ultra_microdust_grade
    ultra_microdust_value = soup2.find_all("span", {"class":"value _cnPm25Value"})[0].text #ultra_microdust_value
    ozone_grade = soup2.find_all("strong", {"class":"level_dsc"})[0].texts #ozone_grade
    ozone_value = soup2.find_all("strong", {"class":"level"})[0].texts #ozone_value

    r_temperature = str(re.findall('-?\d+', temperature)[0]).strip('[\'\']') #temperature
    r_max_temperature = str(re.findall('-?\d+', max_temperature)[0]).strip('[\'\']') #max_temperature
    r_min_temperature = str(re.findall('-?\d+', min_temperature)[0]).strip('[\'\']') #min_temperature
    r_precipitation_percentage1 = str(re.findall('-?\d+', precipitation_percentage1)[0]).strip('[\'\']') #precipitation_percentage1
    r_precipitation_percentage2 = str(re.findall('-?\d+', precipitation_percentage2)[0]).strip('[\'\']') #precipitation_percentage2

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "commerceCard": {
                        "description": f"행운동 봉원중학교의 현재 날씨 {weather}.\n\n온도: {r_temperature}° ({r_max_temperature}° / {r_min_temperature}°)\n강수량: 오전 - {round(int(r_precipitation_percentage1))}% 오후 - {round(int(r_precipitation_percentage2))}%\n자외선: {ultraviolet_ray}\n\n미세먼지: {microdust_grade} {microdust_value}㎍/㎥\n초미세먼지: {ultra_microdust_grade} {ultra_microdust_value}㎍/㎥\n\n사용한 날씨 및 대기질 정보 '네이버 날씨'",
                        "price": 0,
                        "currency": "won",
                        "thumbnails": [
                            {
                                "imageUrl": "../img/thermometer.png"
                            }
                        ],
                        "profile": {
                        "imageUrl": "../img/white.png",
                        "nickname": f"{datetime.now().month}월 {datetime.now().day}일"
                        },
                        "buttons": [
                            {
                                "label": "더보기",
                                "action": "webLink",
                                "webLinkUrl": url1
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [
                {
                    "blockId": "61f0cf897953c638686710f3",
                    "action": "message",
                    "label": "문의하기"
                }
            ]
        }
    }

@app.route("/timetable", methods=["POST"])
def timetable():
    req = request.get_json()

    grade = req["action"]["detailParams"]["bot.school.grade"]["value"]
    _class = req["action"]["detailParams"]["bot.school.class"]["value"]
    date = req["action"]["detailParams"]["bot.date.week"]["value"]

    r_grade = str(re.sub(r'[^0-9]', '', grade).strip("[\']\'"))
    r_class = str(re.sub(r'[^0-9]', '', _class).strip("[\']\'"))
    r_date = str(re.sub(r'[^0-9]', '', date).strip("[\']\'"))

    try:
        _timetable = school[r_grade][r_class][r_date]
    except:
        _timetable = "에러가 발생했습니다."

    return {
        "version": "2.0",
        "name": "timetable",
        "data": {
            "timetable": f"{str(_timetable)}",
            "date": f"{r_date}",
            "days": "",
            "grade": f"{grade}",
            "class": f"{_class}"
        }
    }

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