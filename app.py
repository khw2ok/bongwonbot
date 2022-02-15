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
    
    res1 = requests.get(url1) #res-weather
    soup1 = BeautifulSoup(res1.text, "html.parser")

    res2 = requests.get(url2) #res-microdust
    soup2 = BeautifulSoup(res2.text, "html.parser")

    #weather data from naver weather
    wt = soup1.find_all("span", {"class":"weather"})[0].text #weather
    tp_d = soup1.find_all("div", {"class":"weather_now"})[0].text #temperature_div
    mxtp_d = soup1.find_all("span", {"class":"highest"})[0].text #max-temperature_div
    mntp_d = soup1.find_all("span", {"class":"lowest"})[0].text #min-temperature_div
    pp_v1_d = soup1.find_all("span", {"class":"rainfall"})[0].text #precipitation_percentage_value1_div
    pp_v2_d = soup1.find_all("span", {"class":"rainfall"})[1].text #precipitation_percentage_value2_div
    ur_v = soup1.find_all("strong", {"class":"level_dsc"})[0].text #ultraviolet-ray_value
    #ctp_v = soup1.find_all("div", {"class":"current-weather-extra"})[0].text #ctemperature_value
    #hm_v = soup1.find_all("span", {"id":"wob_hm"})[3].text #humidity_value
    #air data from naver weather
    md_v = soup2.find_all("span", {"class":"value _cnPm10Value"})[0].text #microdust_value
    md_g = soup2.find_all("span", {"class":"grade _cnPm10Grade"})[0].text #microdust_grade
    smd_v = soup2.find_all("span", {"class":"value _cnPm25Value"})[0].text #smicrodust_value
    smd_g = soup2.find_all("span", {"class":"grade _cnPm25Grade"})[0].text #smicrodust_grade
    oz_v = soup2.find_all("strong", {"class":"level"})[0].texts #ozone_value
    oz_g = soup2.find_all("strong", {"class":"level_dsc"})[0].texts #ozone_grade

    tp_v = str(re.findall('-?\d+', tp_d)[0]).strip('[\'\']') #temperature_value
    #ytp_cv = str(re.findall('-?\d+', tp_d)[1]).strip('[\'\']') #yesterday_temperature_compared_value
    mxtp_v = str(re.findall('-?\d+', mxtp_d)[0]).strip('[\'\']') #max-temperature_value
    mntp_v = str(re.findall('-?\d+', mntp_d)[0]).strip('[\'\']') #min-temperature_value
    pp_v1 = str(re.findall('-?\d+', pp_v1_d)[0]).strip('[\'\']') #precipitation_percentage_value1
    pp_v2 = str(re.findall('-?\d+', pp_v2_d)[0]).strip('[\'\']') #precipitation_percentage_value2

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {   
                    "simpleText": {
                        "text": f"행운동 봉원중학교의 현재 날씨 {wt}.\n\n※현재 테스트 중인 기능이며 오류 발생 시 아래 바로가기를 통해 제보해주시길 바랍니다.\n(서버의 네트워크 상황에 따라 데이터가 공백일 수 있습니다.)\n\n사용한 날씨 및 대기질 정보 '네이버 날씨'"
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
                                        "description": f"현재 {tp_v}° (최고 {mxtp_v}°, 최저 {mntp_v}°)",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "강수 확률",
                                        "description": f"오늘 {round((int(pp_v1)+int(pp_v2))/2)}%",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "습도 및 자외선 지수",
                                        "description": f"hm_v%, {ur_v}",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    }
                                ],
                                "buttons": [
                                    {
                                        "label": "더보기",
                                        "action": "webLink",
                                        "webLinkUrl" : "https://weather.naver.com/today/09620575"
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
                                        "description": f"{md_g} {md_v}㎍/㎥",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "초미세먼지",
                                        "description": f"{smd_g} {smd_v}㎍/㎥",
                                        "imageUrl": "https://i.ibb.co/Swwxz7F/64x64.png"
                                    },
                                    {
                                        "title": "오존",
                                        "description": f"{oz_g} {oz_v}ppm",
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

if __name__ == "__main__":
    app.run(debug=True)