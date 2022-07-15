from itertools import count
from statistics import mean

import requests


def predict_rub_salary(vacancy: requests.models.Response) -> int:
    salary = vacancy['salary']
    if not salary or not salary['currency'] == 'RUR':
        return None
    if salary['from'] and salary['to']:
        return int(salary['from'] + salary['to'] / 2)
    elif salary['from']:
        return int(salary['from'] * 1.2)
    else:
        return int(salary['to'] * 0.8)


def calculate_average(salaries: list) -> int:
    salaries_without_none = [salary for salary in salaries if salary]
    average_expected_salary = mean(salaries_without_none)
    return int(average_expected_salary)


def fetch_all_salaries(url: str, params: dict) -> dict:
    all_salaries = []
    for page in count():
        params['page'] = page
        page_response = requests.get(url=url, params=params)
        page_response.raise_for_status()
        page_vacancies = page_response.json()['items']
        for vacancy in page_vacancies:
            all_salaries.append(predict_rub_salary(vacancy))
        if page >= 19:
            break
    return {
            'vacancies_found': page_response.json()['found'],
            'vacancies_processed': len(all_salaries),
            'average_salary': calculate_average(all_salaries)
            }


def main():
    vacancies_dict = {}
    for language in ('Python', 'Rust', 'Dart'):
        params = {'area': 1, 'text': f'{language} разработчик', 'per_page': 100}
        url = 'https://api.hh.ru/vacancies'
        vacancies_dict[language] = fetch_all_salaries(url, params)
    return vacancies_dict


if __name__ == '__main__':
    print(main())

