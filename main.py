from itertools import count
from statistics import mean
from typing import Union, Dict

from terminaltables import SingleTable

import requests


def make_table(vacancies_dict: dict, title: str):
    data = list()
    data.append([
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'])
    for language, vacancy_info in vacancies_dict.items():
        data.append([
            language,
            vacancy_info['vacancies_found'],
            vacancy_info['vacancies_processed'],
            vacancy_info['average_salary']])

    print(SingleTable(data, title).table)


def predict_rub_salary(salary_min: Union[int, float], salary_max: Union[int, float]) -> int:
    if not salary_min and salary_max:
        return None
    if salary_min and salary_max:
        return int(salary_min + salary_max / 2)
    elif salary_min:
        return int(salary_min * 1.2)
    else:
        return int(salary_max * 0.8)


def predict_rub_salary_sj(vacancy: requests.Response) -> int:
    if not vacancy['payment_from'] and not vacancy['payment_to'] or vacancy['currency'] != 'rub':
        return None
    return predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])


def predict_rub_salary_hh(vacancy: requests.Response) -> int:
    if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
        return None
    return predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])


def calculate_average(salaries: list) -> int:
    salaries_without_none = [salary for salary in salaries if salary]
    average_expected_salary = mean(salaries_without_none)
    return int(average_expected_salary)


def fetch_all_salaries_hh(url: str, params: dict) -> dict:
    all_salaries = []
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        page_vacancies = page_response.json()['items']
        for vacancy in page_vacancies:
            all_salaries.append(predict_rub_salary_hh(vacancy))
        if page >= 3:
            break
    return {
            'vacancies_found': page_response.json()['found'],
            'vacancies_processed': len(all_salaries),
            'average_salary': calculate_average(all_salaries)
            }


def fetch_all_salaries_sj(url: str, params: dict, headers: dict) -> dict:
    all_salaries = []
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        vacancies = page_response.json()
        for vacancy in vacancies['objects']:
            all_salaries.append(predict_rub_salary_sj(vacancy))
        if not vacancies['more']:
            break
    return {
        'vacancies_found': vacancies['total'],
        'vacancies_processed': len(all_salaries),
        'average_salary': calculate_average(all_salaries)
    }


def main():
    hh_vacancies_dict = {}
    sj_vacancies_dict = {}
    for language in ('Flutter', 'Rust', 'Dart'):
        params = {'area': 1, 'text': f'{language} разработчик', 'per_page': 100}
        url = 'https://api.hh.ru/vacancies'
        hh_vacancies_dict[language] = fetch_all_salaries_hh(url, params)
        params = {'town': 4, 'keyword': f'{language} разработчик', 'count': 100}
        headers = {
            'X-Api-App-Id':
                'v3.r.136805035.9d02bec60443e5736d70f80f04969b0d37a4e525.dc10c3e63a6116e6840aec166bf23e304a1e678d'
        }
        url = 'https://api.superjob.ru/2.0/vacancies'
        sj_vacancies_dict[language] = fetch_all_salaries_sj(url, params, headers)
    make_table(hh_vacancies_dict, title='HeadHunter Analytics')
    make_table(sj_vacancies_dict, title='SuperJob Analytics')


if __name__ == '__main__':
    main()

