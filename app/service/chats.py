from aiohttp import ClientSession
from core.http import get_http_session
import asyncio

async def get_user_chatIds(http_session : ClientSession, since: str) -> list[str]:
    """
        열려있는 유저 채팅방들의 chatId 목록 반환
    """

    url = "https://api.channel.io/open/v5/user-chats?state=opened&sortOrder=desc&limit=200"
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(f"[get_user_chatIds] HTTP {response.status}: {text}")
            return []

        result = await response.json()

        # since 기준 이후(createdAt > since)만 남기기
        filtered_messages = [
            chat_info for chat_info in result["messages"]
            if chat_info.get("createdAt") and int(chat_info["createdAt"]) > int(since)
        ]

        # chatId만 추출
        chatId_list = [chat_info["chatId"] for chat_info in filtered_messages]

    return chatId_list

async def get_user_chat_messages(http_session: ClientSession, chatId : str) :
    """
        특정 chatId의 메시지 목록을 반환
    """

    url = f"https://api.channel.io/open/v5/user-chats/{chatId}/messages?sortOrder=asc&limit=30"
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(f"[get_user_chat_messages:{chatId}] HTTP {response.status}: {text}")
            return []

        result = await response.json()
        message_list = [
            {
                "id" : message["id"],
                "type" : message["personType"],
                "text" : message["plainText"],
                "createdAt" : message["createdAt"]
            }
            for message in result["messages"]
            if message.get("plainText") and message["personType"] in ("bot", "manager")
        ]
        
    return message_list

async def get_all_user_chat_messages(since: str) :
    """
        해당 채널의 모든 유저 대화내역 조회
    """
    
    http_session: ClientSession = await get_http_session()

    if http_session is None:
        raise Exception("http session null")

    
    chatIds = await get_user_chatIds(http_session, since)

    # 모든 메시지 요청을 병렬 실행
    tasks = [
        get_user_chat_messages(http_session, chatId)
        for chatId in chatIds
    ]

    results = await asyncio.gather(*tasks)

    # chatId와 결과를 매핑
    chat_history = [
        {"chatId": cid, "messages": msgs}
        for cid, msgs in zip(chatIds, results)
    ]

    return chat_history