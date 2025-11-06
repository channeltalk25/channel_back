from typing import Optional
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "Content-Type": "application/json",
    "accept" : "application/json",
    "x-access-key": os.getenv("ACCESS_KEY", ""),
    "x-access-secret": os.getenv("ACCESS_SECRET", "")
}

print("ACCESS_KEY:", os.getenv("ACCESS_KEY"))
print("ACCESS_SECRET:", os.getenv("ACCESS_SECRET"))

session: Optional[aiohttp.ClientSession] = None

async def get_http_session():
    global session
    if session is None:
        print("HTTP Connection Pool이 초기화되지 않았습니다")
        raise ConnectionError("HTTP Connection Pool이 초기화되지 않았습니다")
    elif session.closed:
        print("HTTP Connection Pool이 closed 상태입니다")
        raise ConnectionError("HTTP Connection Pool이 closed 상태입니다")
    
    return session

async def init_http_session():
    global session
    try:
        # ClientSession의 커넥션풀 설정
        connection_pool = aiohttp.TCPConnector(limit=20)

        session = aiohttp.ClientSession(
            connector=connection_pool,
            headers=headers
        )

        if session:
            print("HTTP Session (HTTP Connection Pool) 초기화 성공")
        else:
            print("HTTP Session (HTTP Connection Pool) 초기화 실패")
    except Exception as e:
        print("INIT HTTP SESSION 실패", str(e))
        raise

async def close_http_session():
    global session
    
    if session and not session.closed:
        try:
            await session.close()
        except Exception as e:
            print("HTTP Sessions 반환 실패", str(e))
    else:
        print("HTTP Sessions 반환 실패")