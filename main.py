import argparse

import os

from dotenv import load_dotenv

from get_hh_areas_ids import serialize_and_save_data, fetch_cities_id
from get_hh_statistics import fetch_all_salaries_hh
from get_sj_statistics import fetch_all_salaries_sj
from cli_tables import make_table


def main():
    load_dotenv()
    hh_vacancies_dict = {}
    sj_vacancies_dict = {}
    hh_cities_id = serialize_and_save_data(fetch_cities_id)
    parser = argparse.ArgumentParser(
        description='Enter programming language or languages name to get number of available'
                    ' vacancies in HeadHunter and SuperJob databases related with it and average salary'
    )
    parser.add_argument('keywords', help='Enter single or several programming languages separated with commas')
    parser.add_argument('-city', '--city', help='Enter city name, to filter vacancies by area.')
    args = parser.parse_args()
    args.keywords = tuple(args.keywords.split(','))
    for language in args.keywords:
        params = {'area': hh_cities_id[args.city], 'text': f'{language} разработчик', 'per_page': 100}
        url = 'https://api.hh.ru/vacancies'
        hh_vacancies_dict[language] = fetch_all_salaries_hh(url, params)
        params = {'town': args.city, 'keyword': f'{language} разработчик', 'count': 100}
        headers = {'X-Api-App-Id': os.getenv('SJ_API_KEY')}
        url = 'https://api.superjob.ru/2.0/vacancies'
        sj_vacancies_dict[language] = fetch_all_salaries_sj(url, params, headers)
    make_table(hh_vacancies_dict, title='HeadHunter Analytics')
    make_table(sj_vacancies_dict, title='SuperJob Analytics')


if __name__ == '__main__':
    main()

