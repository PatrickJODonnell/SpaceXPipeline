# Import statements
import asyncio
import aiohttp
from pprint import pprint

async def fetchData():
    """
    Function that fetches data from the provided API URL
    """
    # Setting up API call variables
    base_url = 'https://api.spacexdata.com'
    route = '/v5/launches/query'
    query = {
        "query": {},
        "options": {
            "select":['date_utc', 'rocket', 'payloads', 'success'],
            "pagination": False, 
            "populate": ["payloads", "rocket"]
        }
    }
    # Calling SpaceX API
    async with aiohttp.ClientSession() as session:
        async with session.post(base_url + route, headers={"Conetent-Type": "application/json"}, json = query) as response:
            raw_response = await response.json()
            response = raw_response['docs']
            return(response)

if __name__ == "__main__":
    """
    Running if Python file is running natively 
    """
    # Calling the fetchData function
    response = asyncio.run(fetchData())
    pprint(response)