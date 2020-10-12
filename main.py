import requests
from utils import create_table, get_statistics
from os import getenv
from dotenv import load_dotenv


def get_statistics_hh(languages):
    statistics = {}
    place = 'hh'
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
        language_statistics = get_statistics(place, vacancies_found, url, pages, params)
        statistics[language] = language_statistics
    return statistics


def get_statistics_sj(languages):
    statistics = {}
    place = 'sj'
    for language in languages:
        headers = {
            'X-Api-App-Id': getenv('SJ_API_KEY')
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
        language_statistics = get_statistics(place, vacancies_found, url, pages, params, headers)
        statistics[language] = language_statistics
    return statistics


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

    hh_statistics = get_statistics_hh(programming_languages)
    sj_statistics = get_statistics_sj(programming_languages)
    create_table(hh_statistics, 'HeadHunter')
    create_table(sj_statistics, 'SuperJob')