from itertools import count

import requests

from salaries_calculations import calculate_average, predict_rub_salary_hh
from cli_tables import make_table
from cli_parser import parse_arguments


def fetch_cities_id():
    response = requests.get(url='https://api.hh.ru/areas', params={'per_page': 100})
    response.raise_for_status()
    cities_and_regions = {}
    for region in response.json()[0]['areas']:
        cities_and_regions[region['name']] = region['id']
        for town in region['areas']:
            cities_and_regions[town['name']] = town['id']
    return cities_and_regions


def fetch_all_salaries_hh(params: dict) -> dict:
    url = 'https://api.hh.ru/vacancies/'
    all_salaries = []
    maximum_allowed_pages_to_fetch = 19
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        decoded_page_response = page_response.json()
        page_vacancies = decoded_page_response['items']
        for vacancy in page_vacancies:
            all_salaries.append(predict_rub_salary_hh(vacancy))
        if page >= maximum_allowed_pages_to_fetch:
            break
    return {
            'vacancies_found': decoded_page_response['found'],
            'vacancies_processed': len(all_salaries),
            'average_salary': calculate_average(all_salaries)
            }


def set_hh_parameters(language, city):
    cities_id = fetch_cities_id()
    params = {'keyword': f'{language} разработчик', 'per_page': 100}
    try:
        params['area'] = cities_id[city]
    except KeyError:
        raise KeyError('Такого города нет в базе данных HeadHunter')
    return params


def main():
    hh_vacancies = {}
    keywords, city = parse_arguments()
    for language in keywords:
        hh_vacancies[language] = fetch_all_salaries_hh(set_hh_parameters(language, city))
    print(make_table(hh_vacancies, title='HeadHunter Analytics'))


if __name__ == '__main__':
    main()
