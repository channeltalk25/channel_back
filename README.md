# ChannelTalk Backend

2025 ChannelTalk Hackathon Backend + AI Repository

# 환경변수 설정

`env.example`을 참고하여 `.env` 파일을 생성합니다.

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

# 설치 및 실행방법

Server will be hosted on localhost:port=3100

### 1. 사전 요구사항

```bash
- Python 3.11 이상
- pip
```

### 2. 프로젝트 클론

```bash
git clone <repository-url>
```

### 3. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

### 5. 서버 실행

```bash
python main.py
```