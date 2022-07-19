import argparse


def parse_arguments() -> tuple[tuple, str]:
    parser = argparse.ArgumentParser(
        description='Enter programming language or languages name to find all available'
                    ' vacancies in sj base related with it and average salary'
    )
    parser.add_argument(
        '-k',
        '--keywords',
        default='Python',
        help='Enter single or several programming languages separated with commas'
    )
    parser.add_argument('-city', '--city', default='Москва', help='Enter city name, to filter vacancies by area.')
    args = parser.parse_args()
    args.keywords = tuple(args.keywords.split(','))
    return args.keywords, args.city
