from core.http import get_http_session

async def send_bot_message_to_user_chat(bot_name: str, payload: dict) :

    url_base = "https://api.channel.io/open/v5/user-chats/690a37d9b0954ff47241/messages?botName="

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")

    url = url_base
    url += bot_name

    async with http_session.post(url, json=payload) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(response)

        result = await response.json()
        
    return result