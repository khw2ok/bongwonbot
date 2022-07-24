from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
app = FastAPI(
    title='bongwonbot',
    description='Chatbot, <b>@bongwonbot</b> made by python.',
    version='dev3.2',
    docs_url='/',
    terms_of_service='https://bongwon.kro.kr/terms',
    contact={'email': 'idkimwook@gmail.com'},
    license_info={'name': 'MIT License', 'url': 'https://opensource.org/licenses/MIT'}
)

from comcigan import School
school = School('봉원중학교')

from datetime import datetime
from hanspell import spell_checker

import dotenv
dotenv.load_dotenv()

import json
import os
import random
import re
import requests

class botParams():
    sys_plugin_date: str
    bot_school_grade: int
    bot_school_class: int
    bot_date_week: str
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
    res_api = requests.get(f'https://schoolmenukr.ml/api/middle/B100001561?year={req_plugin_date.year}&month={req_plugin_date.month}&allergy=hidden').text
    res_api_data = json.loads(res_api)
    res_meal = re.sub("#|\'|\[|\'|\]", '', str(res_api_data['menu'][req_plugin_date.day-1]['lunch']))
    if res_meal == '' or res_meal == None:
        res_meal = '급식 정보가 없습니다.'
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'basicCard': {
                        'title': f'{req_plugin_date.year}년 {req_plugin_date.month}월 {req_plugin_date.day}일 {res_days[datetime(req_plugin_date.year, req_plugin_date.month, req_plugin_date.day).weekday()-1]}요일',
                        'description': res_meal,
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
    botParams.bot_date_week = req['action']['detailParams']['bot_date_week']['value']
    req_school_grade = re.sub(r'[^0-9]', '', botParams.bot_school_grade)
    req_school_class = re.sub(r'[^0-9]', '', botParams.bot_school_class)
    req_date_week = {
        '월요일': 0,
        '화요일': 1,
        '수요일': 2,
        '목요일': 3,
        '금요일': 4,
        '토요일': 5,
        '일요일': 6
    }
    res_date_week = req_date_week[botParams.bot_date_week]
    res_timetable = school[int(req_school_grade)][int(req_school_class)][int(res_date_week)]
    res_timetable_class = []
    for i in range(9):
        try:
            res_timetable_class.append({
                    'title': f'{i+1}교시',
                    'description': f'{res_timetable[i][1]} ({res_timetable[i][2]})'
                })
        except IndexError:
            res_timetable_class.append({'contents': 'items not found.'})
    print(res_timetable_class)
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'itemCard': {
                        'head': {
                            'title': f'{req_school_grade}학년 {req_school_class}반 {botParams.bot_date_week} 시간표'
                        },
                        'itemList': [
                            res_timetable_class[0],
                            res_timetable_class[1],
                            res_timetable_class[2],
                            res_timetable_class[3],
                            res_timetable_class[4],
                            res_timetable_class[5],
                            res_timetable_class[6],
                        ],
                        'itemListAlignment': 'left',
                        'buttonLayout': 'vertical'
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

@app.post('/api/spellcheck', description='Correct the spelling.', response_class=JSONResponse)
async def api_spellcheck(request:Request):
    req = await request.json()
    botParams.sys_text = req["action"]["detailParams"]["sys_text"]["value"]
    res = {
        'version': '2.0',
        'template': {
            'outputs': [
                {
                    'simpleText': {
                        'text': f'{spell_checker.check(botParams.sys_text).original} => {spell_checker.check(botParams.sys_text).checked}'
                    }
                }
            ]
        }
    }
    return res

@app.post('/api/quotes', description='Get quotes.', response_class=JSONResponse)
async def api_quotes():
    res_quotes = [
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
        'version': '1.0',
        'name': 'quotes',
        'data': {
            'quote': random.choice(res_quotes)
        }
    }
    return res