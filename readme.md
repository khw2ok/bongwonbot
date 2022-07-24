# Bongwon MidSchool ChatBot
봉원중학교 카카오톡 챗봇

![Python-v3.7.4-blue](https://img.shields.io/badge/Python-v3.7.4-blue)
![license-MIT-green](https://img.shields.io/badge/license-MIT-green)
![last-commit](https://img.shields.io/github/last-commit/khw2ok/bongwonbot)

## Run Application
```bash
./start.sh
```

## Environments
```
WEATHER_APIKEY
NEIS_APIKEY
```

### Server Environments
- OS        : Ubuntu 18.04 LTS
- RAM       : 1024 MB
- IDE       : Goorm IDE

### Develop Environments
- OS        : Debian bookworm/sid
- IDE       : VSCode
- Python    : 3.7.4
- PIP       : 22.2
  - FastAPI : 0.79.0
  - Uvicorn : 0.18.2

## Features
[기능들](docs/features.md)

## Version
[업데이트](docs/version.md)

## Directory
```bash
.venv/
docs/
    features.md
    version.md
src/
    __pycache__/
    data/
        html/
            index.html
        json/
    main.py
tmp/
    backup1.txt
    backup2.txt
.env
.gitignore
LICENSE
ngrok
readme.md
requirements.txt
start.sh
```

## Devlopers
- @khw2ok