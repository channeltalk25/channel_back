from core.http import get_http_session

async def get_managers() :

    url = "https://api.channel.io/open/v5/managers?limit=100"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        id_name_list = [
            {
                "id" : manager["id"],
                "name" : manager["name"]
            }
            for manager in result["managers"]
        ]

    return id_name_list

async def get_manager_name(managerId : str) :

    url = f"https://api.channel.io/open/v5/managers/{managerId}"

    http_session = await get_http_session()

    if http_session is None :
        raise Exception("http session null")
    
    async with http_session.get(url) as response:
        # 정상 답변이 오지 않았다면
        if response.status != 200:
            text = await response.text()
            print(text)

        result = await response.json()
        
    manager = result.get("manager", {})
    
    return manager.get("name") or None