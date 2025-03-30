# WineRecommendation

## 📌 프로젝트 개요

- **URL**: http://winerecommendation.store/
- **프로젝트 이름**: [**WineRecommendation**](https://github.com/Seung-Bum/WineRecommendation)
- **설명**: 개인의 취향에 맞는 와인을 추천하고, 추천된 와인을 공유할 수 있는 웹 애플리케이션

## 🚀 주요 기능

- 사용자 데이터를 입력받아 적절한 와인을 추천
- 추천된 와인을 공유할 수 있는 기능 제공
- Flask 기반의 백엔드 구현 및 Nginx를 통한 Reverse Proxy 설정

## 🛠 기술 스택

- **Backend**: Flask, Python, Nginx
- **Database**: N/A
- **Infra**: Raspberry Pi

## 🏗 설치 방법

### 1️⃣ 환경 설정

- **필수 패키지 설치**

  ```bash
  pip install -r requirements.txt
  ```

- **필요한 라이브러리**

  ```python
  from flask import Flask, request, render_template, jsonify, session
  from flask_cors import CORS
  import os
  from cryptography.fernet import Fernet
  import json
  ```

### 2️⃣ 실행 방법

```bash
python3 app.py
```

## 🔧 환경 변수 설정

`.env` 파일을 생성하여 환경 설정을 지정합니다.

```env
FLASK_ENV=production
#FLASK_ENV=development
```

## 📡 API 엔드포인트

- **`GET /config`**

  - 현재 서버 운영 환경을 반환
  - 로컬 환경: `http://localhost:5000`
  - 운영 환경: `http://124.51.107.175:5001`

- **`POST /receiveData`**

  - 사용자 데이터를 받아서 취향 분석 후 추천 와인 정보 제공
  - 리다이렉트 응답 예시:

    ```json
    {
      "redirect": "/result?wineName=Chardonnay"
    }
    ```

- **`GET /result`**
  - 사용자의 데이터를 바탕으로 추천 와인 결과 제공

## 📦 배포 방법

### 1️⃣ Raspberry Pi에서 소스 코드 다운로드

```bash
git clone https://github.com/Seung-Bum/WineRecommendation.git
cd WineRecommendation
```

### 2️⃣ Nginx 설정

`/etc/nginx/sites-available/default` 또는 별도의 설정 파일을 수정하여 Nginx Reverse Proxy를 설정합니다. (필요에 따라 포트포워딩 설정 진행)

```nginx
server {
    listen 80;
    server_name winerecommendation.store www.winerecommendation.store;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

변경 사항을 적용하려면 다음 명령어 실행:

```bash
sudo systemctl restart nginx
```

### 3️⃣ Flask 서비스 실행 (백그라운드 실행)

```bash
python3 app.py
```
