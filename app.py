from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

import dotenv
import os
import re
import requests

app = Flask(__name__)
dotenv.load_dotenv()

@app.route("/")
def home():
    return ("Hello Podcast!")

@app.route("/test", methods=['POST'])
def test():
    req_json = request.get_json()
    skill_test = req_json["action"]["detailParams"]["skill_test"]["value"]

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

@app.route("/weather", methods=['POST'])
def weather():
    req_json = request.get_json()
    skill_weather = req_json["action"]["detailParams"]["skill_weather"]["value"]
    
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
                        "text": f"행운동 봉원중학교의 현재 날씨 {weather}.\n\n※현재 테스트 중인 기능이며 오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(서버의 네트워크 상황에 따라 데이터가 공백일 수 있습니다.)\n\n사용한 날씨 및 대기질 정보 '네이버 날씨'"
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

@app.route("/virus", methods=['POST'])
def virus():
    req_json = request.get_json()
    skill_virus = req_json["action"]["detailParams"]["skill_virus"]["value"]
    
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
                        "text": f"[바이러스 현황]\n코로나 확진자: {str(format(int(r_infection), ','))}명 (+ {str(format(int(r_infection_day), ','))}명)\n코로나 사망자: {str(format(int(r_death), ','))}명 (+ {str(format(int(r_death_day), ','))}명)\n\n[백신 접종률]\n백신 접종 (1차): {vaccine1}\n백신 접종 (2차): {vaccine2}\n백신 접종 (3차): {vaccine3}\n\n※현재 테스트 중인 기능이며 오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(서버의 네트워크 상황에 따라 데이터가 공백일 수 있습니다.)\n\n사용한 코로나 바이러스 정보 '정부 코로나바이러스감염증-19'"
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