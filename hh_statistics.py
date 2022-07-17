from itertools import count
import argparse

import requests


from salaries_calculations import calculate_average, predict_rub_salary_hh
from hh_areas_ids import fetch_cities_id, serialize_and_save_ids
from cli_tables import make_table


def fetch_all_salaries_hh(url: str, params: dict) -> dict:
    all_salaries = []
    MAXIMUM_ALLOWED_PAGES_TO_FETCH = 19
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        page_response_serialized = page_response.json()
        page_vacancies = page_response_serialized['items']
        for vacancy in page_vacancies:
            all_salaries.append(predict_rub_salary_hh(vacancy))
        if page >= MAXIMUM_ALLOWED_PAGES_TO_FETCH:
            break
    return {
            'vacancies_found': page_response_serialized['found'],
            'vacancies_processed': len(all_salaries),
            'average_salary': calculate_average(all_salaries)
            }


def main():
    hh_vacancies = {}
    cities_id = fetch_cities_id()
    cities_id = serialize_and_save_ids(cities_id)
    parser = argparse.ArgumentParser(
        description='Enter programming language or languages name to find all available'
                    ' vacancies in hh base related with it and average salary'
    )
    parser.add_argument('keywords', help='Enter single or several programming languages separated with commas')
    parser.add_argument('-city', '--city', help='Enter city name, to filter vacancies by area.')
    args = parser.parse_args()
    args.keywords = tuple(args.keywords.split(','))
    for language in args.keywords:
        url = 'https://api.hh.ru/vacancies/'
        params = {'text': f'{language} разработчик', 'per_page': 100}
        if args.city: params['area'] = cities_id[args.city]
        hh_vacancies[language] = fetch_all_salaries_hh(url, params)
    return make_table(hh_vacancies, title='HeadHunter Analytics')


if __name__ == '__main__':
    print(main())
