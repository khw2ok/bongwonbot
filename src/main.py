from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
app = FastAPI(
    title='bongwonbot',
    description='Chatbot, <b>@bongwonbot</b> for bongwon middle school.',
    version='3.2',
    docs_url='/',
    terms_of_service='https://b1bot.kro.kr',
    contact={'email': 'official@b1bot.kro.kr'},
    license_info={'name': 'MIT License', 'url': 'https://opensource.org/licenses/MIT'}
)

from comcigan import School
school = School('봉원중학교')

from datetime import datetime

import dotenv
dotenv.load_dotenv()

import json
import os
import re
import requests

class botParams():
    sys_plugin_date: str
    bot_school_grade: int
    bot_school_class: int
    sys_text: str

@app.post('/api/test', description='Check the user id.', response_class=JSONResponse)
async def api_test(request:Request):
    req = await request.json()
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': req['userRequest']['user']['id']
                    }
                }
            ]
        }
    }
    return res

@app.post('/api/meal', description='Check the school meal.', response_class=JSONResponse)
async def api_meal(request:Request):
    req = await request.json()
    botParams.sys_plugin_date = req['action']['detailParams']['sys_plugin_date']['value']
    req_plugin_date = datetime.strptime(botParams.sys_plugin_date[33:43], '%Y-%m-%d')
    res_days = ['월', '화', '수', '목', '금', '토', '일']
    res_api = requests.get(f'https://schoolmenukr.ml/api/middle/B100001561?year={req_plugin_date.year}&month={req_plugin_date.month}&date={req_plugin_date.day}&allergy=hidden').text
    res_api_data = json.loads(res_api)
    res_meal = re.sub("#|\'|\[|\'|\]", '', str(res_api_data['menu'][0]['lunch']))
    if res_meal == '' or res_meal == None:
        res_meal = '급식 정보가 없습니다.'
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'basicCard': {
                        'title': f'{req_plugin_date.year}년 {req_plugin_date.month}월 {req_plugin_date.day}일 {res_days[datetime(req_plugin_date.year, req_plugin_date.month, req_plugin_date.day).weekday()]}요일',
                        'description': f'{res_meal}',
                        'thumbnail': {
                            'imageUrl': '',
                        }
                    }
                }
            ]
        }
    }
    return res

@app.post('/api/timetable', description='Check the school weather.', response_class=JSONResponse)
async def api_timetable(request:Request):
    req = await request.json()
    botParams.bot_school_grade = req['action']['detailParams']['bot_school_grade']['value']
    botParams.bot_school_class = req['action']['detailParams']['bot_school_class']['value']
    req_school_grade = re.sub(r'[^0-9]', '', botParams.bot_school_grade)
    req_school_class = re.sub(r'[^0-9]', '', botParams.bot_school_class)
    res_timetable = school[int(req_school_grade)][int(req_school_class)]
    res_timetable_class = [[], [], [], [], []]
    for i in range(8):
        for j in range(5):
            try:
                res_timetable_class[j].append(f'{i+1}교시 - {res_timetable[j][i][1]} ({res_timetable[j][i][2]})')
            except IndexError:
                res_timetable_class[j].append(None)
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'carousel': {
                        'type': 'basicCard',
                        'items': [
                            {
                                'title': f'{req_school_grade}학년 {req_school_class}반 월요일 시간표',
                                'description': f'{res_timetable_class[0][0]}\n{res_timetable_class[0][1]}\n{res_timetable_class[0][2]}\n{res_timetable_class[0][3]}\n{res_timetable_class[0][4]}\n{res_timetable_class[0][5]}\n{res_timetable_class[0][6]}\n{res_timetable_class[0][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{req_school_grade}학년 {req_school_class}반 화요일 시간표',
                                'description': f'{res_timetable_class[1][0]}\n{res_timetable_class[1][1]}\n{res_timetable_class[1][2]}\n{res_timetable_class[1][3]}\n{res_timetable_class[1][4]}\n{res_timetable_class[1][5]}\n{res_timetable_class[1][6]}\n{res_timetable_class[1][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{req_school_grade}학년 {req_school_class}반 수요일 시간표',
                                'description': f'{res_timetable_class[2][0]}\n{res_timetable_class[2][1]}\n{res_timetable_class[2][2]}\n{res_timetable_class[2][3]}\n{res_timetable_class[2][4]}\n{res_timetable_class[2][5]}\n{res_timetable_class[2][6]}\n{res_timetable_class[2][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{req_school_grade}학년 {req_school_class}반 목요일 시간표',
                                'description': f'{res_timetable_class[3][0]}\n{res_timetable_class[3][1]}\n{res_timetable_class[3][2]}\n{res_timetable_class[3][3]}\n{res_timetable_class[3][4]}\n{res_timetable_class[3][5]}\n{res_timetable_class[3][6]}\n{res_timetable_class[3][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{req_school_grade}학년 {req_school_class}반 금요일 시간표',
                                'description': f'{res_timetable_class[4][0]}\n{res_timetable_class[4][1]}\n{res_timetable_class[4][2]}\n{res_timetable_class[4][3]}\n{res_timetable_class[4][4]}\n{res_timetable_class[4][5]}\n{res_timetable_class[4][6]}\n{res_timetable_class[4][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
    return res

@app.post('/api/weather', description='Check the school timetable.', response_class=JSONResponse)
async def api_weather():
    res_api = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={os.environ["WEATHER_APIKEY"]}&lang=kr&q=Seoul,KR'.format(key=os.environ['WEATHER_APIKEY'])).text
    res_api_data = json.loads(res_api)
    res_calc = lambda k: k - 273.15
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'itemCard': {
                        'imageTitle': {
                            'title': '날씨',
                            'description': '현재 서울 봉원중학교의 날씨'
                        },
                        'thumbnail': {
                            'imageUrl': ''
                        },
                        'itemList': [
                            {
                                'title': '날씨',
                                'description': res_api_data['weather'][0]['description']
                            },
                            {
                                'title': '기온',
                                'description': f'{round(res_calc(res_api_data["main"]["temp"]))}° ({round(res_calc(res_api_data["main"]["temp_min"]))}° & {round(res_calc(res_api_data["main"]["temp_max"]))}°)'
                            },
                            {
                                'title': '습도',
                                'description': res_api_data['main']['humidity']
                            },
                            {
                                'title': '풍속&퐁항',
                                'description': f'{res_api_data["wind"]["speed"]}m/sec & {res_api_data["wind"]["deg"]}°'
                            }
                        ],
                        'itemListAlignment' : 'right',
                        'buttons': [
                            {
                                'label': '더보기',
                                'action': 'webLink',
                                'webLinkUrl': 'https://openweathermap.org/city/1835848'
                            }
                        ],
                        'buttonLayout' : 'vertical'
                    }
                }
            ]
        }
    }
    return res