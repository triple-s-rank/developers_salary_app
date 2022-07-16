from terminaltables import SingleTable


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