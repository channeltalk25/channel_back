from core.http import get_http_session
from app.service.managers import get_manager_name

# OPEN API /groups/{groupId}/threads/{messageId}/messages 사용

# 하나의 메시지에 답글로 달린 threads들을 조회
async def get_message_threads(groupId: str, messageId: str) :

    url = f"https://api.channel.io/open/v5/groups/{groupId}/threads/{messageId}/messages?sortOrder=asc"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        threads_list = [
            {
                "personId" : thread["personId"],
                "name" : await get_manager_name(thread["personId"]),
                "text" : thread["plainText"]
            }
            for thread in result["messages"]
            if thread.get("plainText")
        ]

    return threads_list