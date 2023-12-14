import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/"

async def get_regions(): 
    url = BASE_URL + "regions/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def get_sources():
    url = BASE_URL + "sources/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching sources. Status code: {response.status_code}")
            return None

async def get_source_names():
    sources = await get_sources()
    if sources:
        return [source.get('source_name') for source in sources]
    else:
        return []

async def get_regions_by_source(source_name):
    regions = await get_regions()
    
    if regions:
        filtered_regions = [region for region in regions if source_name in region.get('sources', [])]
        result_dict = {region['code']: region['name'] for region in filtered_regions}
        return result_dict
    else:
        print("Error fetching regions.")
        return {}

async def get_minmax_date(region_code, source_name):
    url = BASE_URL + f"source/{region_code}/{source_name}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # Заменяем ключи 'min' и 'max'
            data['start'] = data.pop('min', None)
            data['end'] = data.pop('max', None)
            return data
        else:
            print(f"Error fetching data. Status code: {response.status_code}")
            return None

async def post_demography_prediction(data):
    url = BASE_URL + "prediction/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return response.status_code, response.json()
    
    