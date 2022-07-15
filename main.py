from statistics import mean

import requests


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary or not salary['currency'] == 'RUR':
        return None
    if salary['from'] and salary['to']:
        return int(salary['from'] + salary['to'] / 2)
    elif salary['from']:
        return int(salary['from'] * 1.2)
    else:
        return int(salary['to'] * 0.8)


params = {'area': 1, 'text': 'Python разработчик'}
url = 'https://api.hh.ru/vacancies'


def main():
    vacancies_dict = {}
    for language in ('Python', 'Java', 'Javascript'):
        response = requests.get(url=url, params={'area': 1, 'text': f'{language} разработчик'})
        all_salaries = []
        vacancies_processed = 0
        for vacancy in response.json()['items']:
            all_salaries.append(predict_rub_salary(vacancy))
            vacancies_processed += 1
        all_salaries = [salary for salary in all_salaries if salary]

        vacancies_dict[f'{language}'] = {
            'vacancies_found': response.json()['found'],
            'vacancies_processed': vacancies_processed,
            'average_salary': int(mean(all_salaries))
        }
    return vacancies_dict


if __name__ == '__main__':
    print(main())