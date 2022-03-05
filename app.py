from typing import Type
from bs4 import BeautifulSoup
from datetime import date, datetime
from flask import Flask, jsonify

import dotenv
import json
import os
import re
import requests

app = Flask(__name__)
dotenv.load_dotenv()

@app.route("/")
def home():
    return (
        '''
        <html>
            <head>
                <title>BongwonBot</title>
                <meta http-equiv="refresh" content="5;url=https://bongwonbot.github.io"/>
            </head>
            <body>
                <div>
                    Hello Podcast!
                </div>
            </body>
        </html>
        '''
    )

@app.route("/test", methods=["POST"])
def test():
    return {
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
                    "simpleText": {
                        "text": f"행운동 봉원중학교의 현재 날씨 {weather}.\n\n※현재 테스트 중인 기능이며 오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(서버의 네트워크 상황에 따라 데이터가 공백일: 수 있습니다.)\n\n사용한 날씨 및 대기질 정보 '네이버 날씨'"
                    }
                },
                {
                    "carousel": {
                        "type": "listCard",
                        "items": [
                            {
                                "header": {
                                    "title": "날씨"
                                },
                                "items": [
                                    {
                                        "title": "온도",
                                        "description": f"현재 {r_temperature}° (최고 {r_max_temperature}°, 최저 {r_min_temperature}°)",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "강수 확률",
                                        "description": f"오늘 오전: {round(int(r_precipitation_percentage1))}% 오후: {round(int(r_precipitation_percentage2))}%",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "습도 및 자외선 지수",
                                        "description": f"hm_v%, {ultraviolet_ray}",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "label": "더보기",
                                        "action": "webLink",
                                        "webLinkUrl" : "http://ncov.mohw.go.kr/"
                                    }
                                ]
                            },
                            {
                                "header": {
                                    "title": "대기질"
                                },
                                "items": [
                                    {
                                        "title": "미세먼지",
                                        "description": f"{microdust_grade} {microdust_value}㎍/㎥",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "초미세먼지",
                                        "description": f"{ultra_microdust_grade} {ultra_microdust_value}㎍/㎥",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "오존",
                                        "description": f"{ozone_grade} {ozone_value}ppm",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "label": "더보기",
                                        "action": "webLink",
                                        "webLinkUrl" : "https://weather.naver.com/air/09620575"
                                    }    
                                ]
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [
                {
                    "blockId": "61f0cf897953c638686710f3",
                    "action": "message",
                    "label": "오류 제보하기"
                }
            ]
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

    r_infection = str(re.sub(r'[^0-9]', '', infection).strip('[\'\']')) #infection
    r_death = str(re.sub(r'[^0-9]', '', death).strip('[\'\']')) #death
    r_infection_day = str(re.sub(r'[^0-9]', '', infection_day).strip('[\'\']')) #infection_day
    r_death_day = str(re.findall('-?\d+', death_day)).strip('[\'\']') #death_day

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {   
                    "simpleText": {
                        "text": f"[바이러스 현황]\n코로나 확진자: {str(format(int(r_infection), ','))}명 (+ {str(format(int(r_infection_day), ','))}명)\n코로나 사망자: {str(format(int(r_death), ','))}명 (+ {str(format(int(r_death_day), ','))}명)\n\n[백신 접종률]\n백신 접종 (1차): {vaccine1}\n백신 접종 (2차): {vaccine2}\n백신 접종 (3차): {vaccine3}\n\n※현재 테스트 중인 기능이며 오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(서버의 네트워크 상황에 따라 데이터가 공백일: 수 있습니다.)\n\n사용한 코로나 바이러스 정보 '정부 코로나바이러스감염증-19'"
                    }
                },
            ],
            "quickReplies": [
                {
                    "blockId": "61f0cf897953c638686710f3",
                    "action": "message",
                    "label": "오류 제보하기"
                }
            ]
        }
    }

@app.route("/food", methods=["POST"])
def food():
    url = requests.get("https://schoolmenukr.ml/api/middle/B100001561")
    
    file = url.text
    data = json.loads(file)
    #print(re.sub("-?\d+|\'|\?|\'|\.|", "", str(data)))

    days = ['월', '화', '수', '목', '금', '토', '일']
    #days[datetime(int(datetime.now().year), int(datetime.now().month), 1).weekday()]

    answer1 = "1일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 1).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][0]["lunch"]))+"\n2일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 2).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][1]["lunch"]))+"\n3일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 3).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][2]["lunch"]))+"\n4일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 4).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][3]["lunch"]))+"\n5일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 5).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][4]["lunch"]))+"\n6일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 6).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][5]["lunch"]))+"\n7일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 7).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][6]["lunch"]))
    answer2 = "8일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 8).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][7]["lunch"]))+"\n9일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 9).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][8]["lunch"]))+"\n10일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 10).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][9]["lunch"]))+"\n11일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 11).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][10]["lunch"]))+"\n12일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 12).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][11]["lunch"]))+"\n13일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 13).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][12]["lunch"]))+"\n14일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 14).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][13]["lunch"]))
    answer3 = "15일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 15).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][14]["lunch"]))+"\n16일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 16).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][15]["lunch"]))+"\n17일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 17).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][16]["lunch"]))+"\n18일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 18).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][17]["lunch"]))+"\n19일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 19).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][18]["lunch"]))+"\n20일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 20).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][19]["lunch"]))+"\n21일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 21).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][20]["lunch"]))
    answer4 = "22일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 22).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][21]["lunch"]))+"\n23일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 23).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][22]["lunch"]))+"\n24일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 24).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][23]["lunch"]))+"\n25일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 25).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][24]["lunch"]))+"\n26일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 26).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][25]["lunch"]))+"\n27일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 27).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][26]["lunch"]))+"\n28일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 28).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][27]["lunch"]))

    try:
        answer5 = "29일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 29).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][28]["lunch"]))+"\n30일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 30).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][29]["lunch"]))+"\n31일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 31).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][30]["lunch"]))
    except TypeError:
        try:
            answer5 = "29일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 29).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][28]["lunch"]))+"\n30일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 30).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][29]["lunch"]))
        except TypeError:
            try:
                answer5 = "29일 ("+days[datetime(int(datetime.now().year), int(datetime.now().month), 29).weekday()]+"): "+re.sub("-?\d+|\'|\.|\'|\#|\'|\[|\'|\]", "", str(data["menu"][28]["lunch"]))
            except TypeError:
                answer5 = "None"
    
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {   
                    "simpleText": {
                        "text": f"{datetime.now().month}월 {datetime.now().day}일 {days[datetime(int(datetime.now().year), int(datetime.now().month), int(datetime.now().day)).weekday()]}요일\n\n오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(급식이 없는 날은 데이터가 None 또는 공백일 수도 있습니다.)\n\n사용한 학교 급식 정보 '5d-jh/school-menu-api (NEIS 급식)'"
                    }
                },
                {
                    "simpleText": {
                        "text": str(answer1)
                    }
                },
                {   
                    "simpleText": {
                        "text": str(answer2)
                    }
                },
                {   
                    "simpleText": {
                        "text": str(answer3)
                    }
                },
                {   
                    "simpleText": {
                        "text": str(answer4)
                    }
                },
                {   
                    "simpleText": {
                        "text": str(answer5)
                    }
                },
            ],
            "quickReplies": [
                {
                    "blockId": "61f0cf897953c638686710f3",
                    "action": "message",
                    "label": "오류 제보하기"
                }
            ]
        }
    }

if __name__ == "__main__":
    app.run(debug=True)