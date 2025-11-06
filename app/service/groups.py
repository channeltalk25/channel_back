from core.http import get_http_session
from app.service.managers import get_manager_name

async def get_groups() :

    url = "https://api.channel.io/open/v5/groups?limit=50"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        group_list = [
            {
                "groupId": group["id"],
                "name": group["title"],
                "managerIds" : group["managerIds"]
            }
            for group in result["groups"]
        ]
            
    return group_list