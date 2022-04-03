# bongwonbot
봉원중학교 비공식 챗봇 <small>bongwon middle school unofficial chatbot</small>

![Python-v3.10.4-blue](https://img.shields.io/badge/Python-v3.10.4-blue)
![license-MIT-green](https://img.shields.io/badge/license-MIT-green)
![last-commit](https://img.shields.io/github/last-commit/bongwonbot/bongwonbot)

## 정보
@bongwonbot 은 봉원중학교의 비공식 카카오톡 챗봇입니다.

### 1세대
봉원중학교 챗봇 1세대<small>(구)</small>는 *4월 20일 2021년*에 시작되어, 학교 관련 문제로 인하여 *8월 2021년* 종료했습니다.

> **서버** - [Goorm IDE](https://ide.goorm.io/) <small>(24/7 서비스 미지원)</small>  
> **비용** - 무료  
> **이용자** -  14명

### 2세대
봉원중학교 챗봇 2세대는 곧 *4월 20일 2022년* 챗봇 1주년에 릴리즈 될 예정입니다.

> **서버** - [Heroku](https://heroku.com/)  
> **비용** - 약 5000원  
> **이용자** -  없음

#### 팟캐스트
팟캐스트, 봉원중학교 챗봇은 *2021년* 1세대 서비스 종료 후 *2022년* 2세대 서비스 이전 테스트 겸으로 제작된 임시 챗봇입니다.

## 기능들
|기능|설명|업데이트|발화|
|:---:|:---|:---|:---|
|테스트|봇 서버 테스트||`테스트`, `test` ...|
|급식|학교 급식 확인|`prev3.0[food/3]`|`급식`, `급식 알려줘` ...|
|기상|기상 정보 확인|`v2.4`|`기상`, `날씨`, `기상 알려줘` ...|
|시간표|학교 시간표 확인|||
|바이러스|코로나 확진, 정보 확인|`v2.31`|`바이러스`, `코로나`, `바이러스 정보` ...|
|정보|학교 정보 확인|`v2.4`|`학교`, `학교 정보` ...|

## 릴리즈
챗봇 1주년에 릴리즈 될 예정입니다.

### 패치노트
<details><summary><b>prev3.0</b></summary>

> *(예정)* **prev3.0** - 4월 2일 ~ ~~4월 20일~~ - 2022년 <small>*(Preview Update)*</small>
> - - [x] 깃허브 레포 변경; <small>`/app` to `/bongwonbot`</small>
> - - [x] 전체적인 챗봇 구성 변경
>   - - [ ] json template 리턴 -> json data 리턴으로 대부분 변경
>   - - [ ] 일부 발화 리턴 simpleText -> Card 형식 변경
> - - [ ] 봉원중학교 챗봇 개발 알림톡 제작 *(예정)*
> - - [ ] 스킬 추가 및 수정
>   - - [x] 급식 정보
>       - ~~이번 달 -> 이번 주 / 다음 주 / 저번 주로 변경~~
>       - ~~나이스 급식 api 사용 *(예정)*~~
>   - - [x] 날씨 정보<small>(*구 기상 정보* 에서 분리)</small>
>       - [x] 네이버 날씨 크롤링 -> ~~AccuWeather~~ OpenWeatherMap API
>   - - [ ] 대기 정보<small>(*구 기상 정보* 에서 분리)</small>
>       - - [ ] 네이버 날씨 크롤링 -> API *(예정)*
>   - - [ ] 코로나 정보<small>(*구 바이러스 정보*)</small>
>   - - [ ] 시간표 정보
>       - - [ ] [컴시간.py](#참고된-내용) 이용; <small>이번주 월 / 화 / 수 / 목 / 금 / 토 정보 확인 가능</small>
>   - - [ ] 자가진단 확인 *(예정)*
>       - - [ ] [자가진단.py](#참고된-내용) 이용 *(예정)*
>   - - [ ] 이외 스킬 추가
</details>

## 파일 구조
```shell
bongwonbot
├── .venv
├── img
│   ├── thermometer.png
│   └── white.png
├── src
│   ├── templates
│        └── index.html
│   ├── .env
│   └── app.py
├── .gitignore
├── Aptfile
├── LICENSE
├── ngrok
├── Procfile
├── readme.md
├── requirements.txt
└── runtime.txt
```

## 개발 환경
> **언어** - Python 3.10.4  
> **패키지** - Flask 2.0.3 [포함 24개](requirements.txt)  
> **서버** - [Heroku](https://heroku.com/)   
> **OS** - [Debian 11 testing](https://www.debian.org/)

## 참고된 내용
- [응답 타입별 JSON 포맷](https://i.kakao.com/docs/skill-response-format)
- 챗봇
  - [단대 라이프](https://github.com/kitae0522/DKSH-KAKAO-i)
  - [선우봇](https://github.com/swparkaust/sunwoobot)
- 패키지 및 깃허브
  - [Flask](https://github.com/pallets/flask)
  - [컴시간.py](https://github.com/Team-IF/comcigan-py)
  - ~~[자가진단.py](https://github.com/decave27/hcspy)~~
  - [학교 급식 api](https://github.com/5d-jh/school-menu-api)
