import json
import requests


def fetch_cities_id():
    response = requests.get(url='https://api.hh.ru/areas', params={'per_page': 100})
    cities_and_regions = {}
    for region in response.json()[0]['areas']:
        cities_and_regions[region['name']] = region['id']
        for town in region['areas']:
            cities_and_regions[town['name']] = town['id']
    return cities_and_regions


def serialize_and_save_data(data: dict):
    try:
        with open('city_id_hh.json', 'r') as f:
            data = {}
            data = json.load(f)
    except FileNotFoundError:
        with open('city_id_hh.json', 'w') as fp:
            json.dump(data, fp)
    except json.decoder.JSONDecodeError:
        with open('city_id_hh.json', 'a') as fp:
            json.dump(data, fp)
    return data
