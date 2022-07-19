import os
from itertools import count

import requests
from dotenv import load_dotenv

from cli_parser import parse_arguments
from cli_tables import make_table
from salaries_calculations import predict_rub_salary_sj, calculate_average


def fetch_all_salaries_sj(params: dict, headers: dict) -> dict:
    url = 'https://api.superjob.ru/2.0/vacancies'
    all_salaries = []
    for page in count():
        params.update(page=page)
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        decoded_page_response = page_response.json()
        vacancies = decoded_page_response['objects']
        for vacancy in vacancies:
            all_salaries.append(predict_rub_salary_sj(vacancy))
        if not decoded_page_response['more']:
            break
    return {
        'vacancies_found': decoded_page_response['total'],
        'vacancies_processed': len(all_salaries),
        'average_salary': calculate_average(all_salaries)
    }


def set_sj_parameters(language, town):
    params = {'town': town, 'keyword': f'{language} разработчик', 'count': 100}
    headers = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
    return params, headers


def main():
    load_dotenv()
    sj_vacancies = {}
    keywords, town = parse_arguments()
    for language in keywords:
        params, headers = set_sj_parameters(language, town)
        sj_vacancies.update(language=fetch_all_salaries_sj(params, headers))
    print(make_table(sj_vacancies, title='SuperJob Analytics'))


if __name__ == '__main__':
    main()
