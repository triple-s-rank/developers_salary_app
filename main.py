import requests


def predict_rub_salary(vacancy):
    salary = vacancy['salary']
    if not salary or not salary['currency'] == 'RUR':
        return None
    if salary['from'] and salary['to']:
        return salary['from'] + salary['to'] / 2
    elif salary['from']:
        return salary['from'] * 1.2
    else:
        return salary['to'] * 0.8


params = {'area': 1, 'text': 'Python разработчик'}
response = requests.get(url='https://api.hh.ru/vacancies', params=params)




