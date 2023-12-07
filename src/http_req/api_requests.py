import requests

BASE_URL = "http://localhost:8000/api/"

def get_regions(): 
    url = BASE_URL + "regions/"
    response = requests.get(url)
    return response.json()# [{'code': 'c9', 'name': 'c9', 'sources': ['worldbank']}, {'code': 'xp', 'name': 'xp', 'sources': ['worldbank']}, ...

def get_sources():
    url = BASE_URL + "sources/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching sources. Status code: {response.status_code}")
        return None

def get_source_names():
    sources = get_sources()
    
    if sources:
        return [source.get('source_name') for source in sources]
    else:
        return []

def get_regions_by_source(source_name):
    sources = get_sources()
    
    if sources:
        for source in sources:
            if source.get('source_name') == source_name:
                return source.get('regions', [])
        print(f"Source '{source_name}' not found.")
        return []
    else:
        return []

def get_minmax_date(region_code, source_name):
    url = BASE_URL + f"source/{region_code}/{source_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Заменяем ключи 'min' и 'max'
        data['start'] = data.pop('min', None)
        data['end'] = data.pop('max', None)
        return data
    else:
        print(f"Error fetching data. Status code: {response.status_code}")
        return None
 
# data = {    # dict тип
#     "region": "xp",          
#     "source": "worldbank",
#     "predict_years_count": 5,
#     "inputDataPeriod": {"start": "1960-01-01", "end": "2022-01-01"},
# }

# sources = get_sources()
def post_demography_prediction(data):
    url = BASE_URL + "prediction/"
    response = requests.post(url, json=data)
    return response.status_code, response.json()
# В ответ получаем
# [{'index': 0.0, 'Year': 1960, 'N(t)': 2107416130, 'B(t)': 73099320.0, 'D(t)': 41347730.0, 'NM(t)': 440770.0, 'DNM': 41788500.0, 'IntB': 73099320, 'IntDNM': 41788500, 'rBt': 0.0, 'rDNMt': 0.0, 'Qt': 0}, {'index': 1.0, 'Year': 1961, 'N(t)': 2135115636, 'B(t)': 71930086.0, 'D(t)': 33906093.0, 'NM(t)': 593111.0, 'DNM': 34499204.0, 'IntB': 145029406, 
# 'IntDNM': 76287704, 'rBt': 49.5968976112, 'rDNMt': 45.2224961443, 'Qt': 0}, {'index': 2.0, 'Year': 1962, 'N(t)': 2175939784, 'B(t)': 85824052.0, 'D(t)': 31377775.0, 'NM(t)': 
# 663100.0, 'DNM': 32040875.0, 'IntB': 230853458, 'IntDNM': 108328579, 'rBt': 37.1768535518, 'rDNMt': 29.57749035, 'Qt': 1}, {'index': 3.0, 'Year': 1963, 'N(t)': 2228877289, 'B(t)': 91616401.0, 'D(t)': 31682869.0, 'NM(t)': 755086.0, 'DNM': 32437955.0, 'IntB': 322469859, 'IntDNM': 140766534, 'rBt': 28.4108416471, 'rDNMt': 23.0437974696, 'Qt': 2}, {'index': 4.0, 'Year': 1964, 'N(t)': 2282093614, 'B(t)': 90072447.0, 'D(t)': 32945049.0, 
# 'NM(t)': 718826.0, 'DNM': 33663875.0, 'IntB': 412542306, 'IntDNM': 174430409, 'rBt': 21.833505483, 'rDNMt': 19.2993155224, 'Qt': 2},....
# ...................
