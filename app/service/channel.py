from core.http import get_http_session

async def get_channel():

    url = "https://api.channel.io/open/v5/channel"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()

    return result