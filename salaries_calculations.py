from statistics import mean
from typing import Union

import requests


def calculate_average(salaries: list) -> int:
    salaries_without_none = [salary for salary in salaries if salary]
    average_expected_salary = mean(salaries_without_none)
    return int(average_expected_salary)


def predict_rub_salary(salary_min: Union[int, float], salary_max: Union[int, float]) -> int:
    if not salary_min and salary_max:
        return None
    if salary_min and salary_max:
        return int(salary_min + salary_max / 2)
    elif salary_min:
        return int(salary_min * 1.2)
    else:
        return int(salary_max * 0.8)


def predict_rub_salary_hh(vacancy: requests.Response) -> int:
    if not vacancy['salary'] or vacancy['salary']['currency'] != 'RUR':
        return None
    return predict_rub_salary(vacancy['salary']['from'], vacancy['salary']['to'])


def predict_rub_salary_sj(vacancy: requests.Response) -> int:
    if not vacancy['payment_from'] and not vacancy['payment_to'] or vacancy['currency'] != 'rub':
        return None
    return predict_rub_salary(vacancy['payment_from'], vacancy['payment_to'])