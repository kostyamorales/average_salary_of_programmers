import requests
from utils import print_table, get_language_statistic_hh, get_language_statistic_sj
from os import getenv
from dotenv import load_dotenv


def get_statistic_hh(languages):
    statistic = {}
    for language in languages:
        params = {
            'area': 1,
            'text': f'программист {language}',
            'period': 30,
            'per_page': 100,
        }
        url = 'https://api.hh.ru/vacancies'
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies_found = response.json()['found']
        pages = response.json()['pages']
        params['only_with_salary'] = True
        language_statistic = get_language_statistic_hh(vacancies_found, pages, params)
        statistic[language] = language_statistic
    return statistic


def get_statistic_sj(languages, api_key):
    statistic = {}
    for language in languages:
        headers = {
            'X-Api-App-Id': api_key
        }
        params = {
            'keyword': f'программист {language}',
            'town': 4,
            'catalogues': 48,
            'count': 100
        }
        url = 'https://api.superjob.ru/2.33/vacancies/'
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies_found = response.json()['total']
        pages = vacancies_found // 100
        language_statistic = get_language_statistic_sj(vacancies_found, pages, params, headers)
        statistic[language] = language_statistic
    return statistic


if __name__ == '__main__':
    load_dotenv()
    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Shell',
        'Objective-C',
        'Scala',
        'Swift',
        'TypeScript'
    ]
    sj_api_key = getenv('SJ_API_KEY')
    hh_statistic = get_statistic_hh(programming_languages)
    sj_statistic = get_statistic_sj(programming_languages, sj_api_key)
    print_table(hh_statistic, 'HeadHunter')
    print_table(sj_statistic, 'SuperJob')
