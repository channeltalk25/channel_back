from core.http import get_http_session
from app.service.managers import get_manager_name
from app.service.threads import get_message_threads

# OPEN API /groups/{groupId}/messages? 사용

async def get_group_messages(groupId : str) :

    url = f"https://api.channel.io/open/v5/groups/{groupId}/messages?sortOrder=asc&limit=100"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        message_list = [
            {
                "messageId" : chat["id"],
                "personId" : await get_manager_name(chat["personId"]),
                "text" : chat["plainText"]
            }
            for chat in result["messages"]
            if chat.get("plainText")
        ]

    return message_list

async def get_group_messages_and_threads(groupId : str) :

    url = f"https://api.channel.io/open/v5/groups/{groupId}/messages?sortOrder=desc&limit=100"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        message_list = [
            {
                "messageId" : chat["id"],
                "personId" : await get_manager_name(chat["personId"]),
                "text" : chat["plainText"],
                "threads" : await get_message_threads(groupId, chat["id"])
            }
            for chat in result["messages"]
            if chat.get("plainText")
        ]

    return message_list


# json spec -> openai
# 유형별 반환 시키기
# 카테고리 -> 매핑해서 반환