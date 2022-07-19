from dotenv import load_dotenv

from cli_parser import parse_arguments
from hh_statistics import fetch_all_salaries_hh, set_hh_parameters
from sj_statistics import fetch_all_salaries_sj, set_sj_parameters
from cli_tables import make_table


def main():
    load_dotenv()
    hh_vacancies = {}
    sj_vacancies = {}
    keywords, city = parse_arguments()
    for language in keywords:
        hh_vacancies[language] = fetch_all_salaries_hh(set_hh_parameters(language, city))
        params, headers = set_sj_parameters(language, city)
        sj_vacancies[language] = fetch_all_salaries_sj(params, headers)
    print(make_table(hh_vacancies, title='HeadHunter'), make_table(sj_vacancies, title='SuperJob'), sep='\n')


if __name__ == '__main__':
    main()

