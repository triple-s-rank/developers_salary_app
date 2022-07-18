import argparse
import os
from itertools import count

import requests
from dotenv import load_dotenv

from cli_tables import make_table
from salaries_calculations import predict_rub_salary_sj, calculate_average


def fetch_all_salaries_sj(params: dict, headers: dict) -> dict:
    url = 'https://api.superjob.ru/2.0/vacancies'
    all_salaries = []
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_response_serialized = page_response.json()
        vacancies = page_response_serialized['objects']
        for vacancy in vacancies:
            all_salaries.append(predict_rub_salary_sj(vacancy))
        if not page_response_serialized['more']:
            break
    return {
        'vacancies_found': page_response_serialized['total'],
        'vacancies_processed': len(all_salaries),
        'average_salary': calculate_average(all_salaries)
    }


def main():
    load_dotenv()
    sj_vacancies = {}
    parser = argparse.ArgumentParser(
        description='Enter programming languag  e or languages name to find all available'
                    ' vacancies in sj base related with it and average salary'
    )
    parser.add_argument('keywords', help='Enter single or several programming languages separated with commas')
    parser.add_argument('-city', '--city', help='Enter city name, to filter vacancies by area.')
    args = parser.parse_args()
    args.keywords = tuple(args.keywords.split(','))
    for language in args.keywords:
        params = {'town': args.city, 'keyword': f'{language} разработчик', 'count': 100}
        headers = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
        sj_vacancies[language] = fetch_all_salaries_sj(params, headers)
    return make_table(sj_vacancies, title='SuperJob Analytics')


if __name__ == '__main__':
    print(main())
