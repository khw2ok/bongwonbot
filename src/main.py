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
data = json.load(open('data.json'))

import os
import re
import requests

def checkDB(req):
    if req['userRequest']['user']['id'] not in data:
        data[req['userRequest']['user']['id']] = {
            'usage': 0,
            'config': {
                'grade': None,
                'class': None
            }
        }
        json.dump(data, open('data.json', 'w'), indent=4)

def addUsage(req):
    checkDB(req)
    data[req['userRequest']['user']['id']]['usage'] = data[req['userRequest']['user']['id']]['usage']+1
    json.dump(data, open('data.json', 'w'), indent=4)

@app.post('/api/welcome', description='', response_class=JSONResponse)
async def api_welcome(request:Request):
    req = await request.json()
    addUsage(req)
    if req['userRequest']['user']['id'] in data:
        res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'basicCard': {
                            'title': '안녕하세요',
                            'description': '저는 봉원중학교의 생활을 더욱 편리하게 만들어줄 \'봉원중학교 챗봇\'입니다.',
                            'thumbnails': {
                                'imageUrl': ''
                            }
                        }
                    }
                ]
            }
        }
    else:
        checkDB(req)
        res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'basicCard': {
                            'title': '안녕하세요',
                            'description': '저는 봉원중학교의 생활을 더욱 편리하게 만들어줄 \'봉원중학교 챗봇\'입니다.',
                            'thumbnails': {
                                'imageUrl': ''
                            }
                        }
                    },
                    {
                        'basicCard': {
                            'title': '이용이 처음이신가요?',
                            'description': '챗봇 도움말에 이용에 도움이 될 만한 정보를 알 수 있습니다.',
                            'thumbnails': {
                                'imageUrl': ''
                            },
                            'buttons': [
                                {
                                    'label': '확인하기',
                                    'action': 'webLink',
                                    'webLinkUrl': 'https://b1bot.kro.kr/docs'
                                }
                            ],
                        }
                    }
                ]
            }
        }
    return res

@app.post('/api/config', description='', response_class=JSONResponse)
async def api_config(request:Request):
    req = await request.json()
    checkDB(req)
    addUsage(req)
    params_bot_school_grade = req['action']['detailParams']['bot_school_grade']['value']
    params_bot_school_class = req['action']['detailParams']['bot_school_class']['value']
    res_school_grade = re.sub(r'[^0-9]', '', params_bot_school_grade)
    res_school_class = re.sub(r'[^0-9]', '', params_bot_school_class)
    data[req['userRequest']['user']['id']] = {
        'usage': 0,
        'config': {
            'grade': int(res_school_grade),
            'class': int(res_school_class)
        }
    }
    json.dump(data, open('data.json', 'w'), indent=4)
    res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'basicCard': {
                            'title': '설정이 완료 되었습니다.',
                            'description': f'{res_school_grade}학년 {res_school_class}반으로 설정이 완료되었습니다.',
                            'thumbnails': {
                                'imageUrl': ''
                            }
                        }
                    }
                ]
            }
        }
    return res

@app.post('/api/info', description='', response_class=JSONResponse)
async def api_info(request:Request):
    req = await request.json()
    checkDB(req)
    addUsage(req)
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'itemCard': {
                        'head': {
                            'title': req['userRequest']['user']['id'],
                        },
                        'itemList': [
                            {
                                'title': '챗봇 이용률',
                                'description': f'{data[req["userRequest"]["user"]["id"]]["usage"]}'
                            },
                            {
                                'title': '학급',
                                'description': f'{data[req["userRequest"]["user"]["id"]]["config"]["grade"]}학년 {data[req["userRequest"]["user"]["id"]]["config"]["class"]}반'
                            }
                        ],
                        'itemListAlignment' : 'right'
                    }
                }
            ],
            'quickReplies': [
                {
                    'label': '학급 설정하기',
                    'action': 'block',
                    'blockId': '635c946c7d0dc94f4d60f044'
                }
            ]
        }
    }
    return res

@app.post('/api/meal', description='Check the school meal.', response_class=JSONResponse)
async def api_meal(request:Request):
    req = await request.json()
    params_sys_plugin_date = req['action']['detailParams']['sys_plugin_date']['value']
    req_plugin_date = datetime.strptime(params_sys_plugin_date[33:43], '%Y-%m-%d')
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

@app.post('/api/timetable', description='', response_class=JSONResponse)
async def api_timetable(request:Request):
    req = await request.json()
    checkDB(req)
    res_school_grade = data[req['userRequest']['user']['id']]['config']['grade']
    res_school_class = data[req['userRequest']['user']['id']]['config']['class']
    if res_school_grade == None or res_school_class == None:
        res = {
            'version': '2.0',
            'template': {
                'outputs': [
                    {
                        'basicCard': {
                            'title': '오류',
                            'description': '현재 학급이 설정되어 있지 않습니다. 아래 버튼을 통해 학급 설정 이후 이용해 주시기 바랍니다.',
                            'thumbnails': {
                                'imageUrl': ''
                            },
                            'buttons': [
                                {
                                    'label': '학급 설정하기',
                                    'action': 'block',
                                    'blockId': '635c946c7d0dc94f4d60f044'
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
                                'title': f'{res_school_grade}학년 {res_school_class}반 월요일',
                                'description': f'{res_timetable_class[0][0]}\n{res_timetable_class[0][1]}\n{res_timetable_class[0][2]}\n{res_timetable_class[0][3]}\n{res_timetable_class[0][4]}\n{res_timetable_class[0][5]}\n{res_timetable_class[0][6]}\n{res_timetable_class[0][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{res_school_grade}학년 {res_school_class}반 화요일',
                                'description': f'{res_timetable_class[1][0]}\n{res_timetable_class[1][1]}\n{res_timetable_class[1][2]}\n{res_timetable_class[1][3]}\n{res_timetable_class[1][4]}\n{res_timetable_class[1][5]}\n{res_timetable_class[1][6]}\n{res_timetable_class[1][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{res_school_grade}학년 {res_school_class}반 수요일',
                                'description': f'{res_timetable_class[2][0]}\n{res_timetable_class[2][1]}\n{res_timetable_class[2][2]}\n{res_timetable_class[2][3]}\n{res_timetable_class[2][4]}\n{res_timetable_class[2][5]}\n{res_timetable_class[2][6]}\n{res_timetable_class[2][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{res_school_grade}학년 {res_school_class}반 목요일',
                                'description': f'{res_timetable_class[3][0]}\n{res_timetable_class[3][1]}\n{res_timetable_class[3][2]}\n{res_timetable_class[3][3]}\n{res_timetable_class[3][4]}\n{res_timetable_class[3][5]}\n{res_timetable_class[3][6]}\n{res_timetable_class[3][7]}'.strip('\nNone'),
                                'thumbnail': {
                                    'imageUrl': '',
                                }
                            },
                            {
                                'title': f'{res_school_grade}학년 {res_school_class}반 금요일',
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
                        'head': {
                            'title': req['userRequest']['user']['id'],
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