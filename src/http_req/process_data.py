def find_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None  # Return None if the value is not found

# локальная обработка имен
# def get_country_names_by_iso2(iso2_codes):
#     countries = wb.get_countries(incomelevel='', lendingtype='', displayformat='json')
#     result = {}
#     for iso2_code in iso2_codes:
#         iso2_code_lower = iso2_code.lower()
#         country_info = countries[countries['iso2Code'].str.lower() == iso2_code_lower].iloc[0]
#         country_name = country_info['name'] if not country_info.empty else f"Country with code '{iso2_code}' not found."
#         result[iso2_code] = country_name
#     return result

def extract_years(minmax_date):
    start_date_str = minmax_date['start']
    end_date_str = minmax_date['end']

    start_year = int(start_date_str.split('-')[0])
    end_year = int(end_date_str.split('-')[0])

    return start_year, end_year