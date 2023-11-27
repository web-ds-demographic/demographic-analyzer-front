import requests
# примерные запросы к бекенду (который его еще нет)

# получение списка регионов
def get_regions():
    response = requests.get('http://127.0.0.1:5000/api/demography/GetRegions')
    regions = response.json()
    return regions

# получение информации о периоде данных для выбранного источника и региона
def get_sources_info(region, source):
    response = requests.get(f'http://127.0.0.1:5000/api/demography/GetSources?region={region}&source={source}')
    info = response.json()
    return info

# отправки запроса на предсказание демографии
def get_prediction(region, source, start, end):
    data = {
        "region": region,
        "source": source,
        "inputDataPeriod": {
            "start": start,
            "end": end
        }
    }
    response = requests.post('http://127.0.0.1:5000/api/demography/Predict', json=data)
    result = response.json()
    return result
