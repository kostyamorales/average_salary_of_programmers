from terminaltables import AsciiTable
import requests


def predict_rub_salary(salary_from, salary_to):
    if not salary_from:
        salary_from = None
    if not salary_to:
        salary_to = None
    if salary_from and salary_to:
        average_salary = (salary_from + salary_to) / 2
        return average_salary
    elif salary_from and not salary_to:
        average_salary = salary_from * 1.2
        return average_salary
    elif not salary_from and salary_to:
        average_salary = salary_to * 0.8
        return average_salary


def print_table(statistics, title):
    rows_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in statistics:
        rows_table.append(
            [language, statistics[language]['vacancies_found'], statistics[language]['vacancies_processed'],
             statistics[language]['average_salary']])
    table = AsciiTable(rows_table, title)
    print(table.table)


def get_language_statistic_hh(vacancies_found, pages, params):
    language_statistics = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    vacancies_processed = 0
    page = 0
    salary_sum = 0
    while page < pages:
        url = 'https://api.hh.ru/vacancies'
        params['page'] = page
        page_response = requests.get(url, params=params)
        page_response.raise_for_status()
        answer = page_response.json()['items']
        page += 1
        for vacancy in answer:
            salary = vacancy['salary']
            if salary['currency'] != 'RUR':
                continue
            salary_from = salary['from']
            salary_to = salary['to']
            average_salary_vacancy = predict_rub_salary(salary_from, salary_to)
            salary_sum += average_salary_vacancy
            vacancies_processed += 1
            average_salary = 0
            if vacancies_processed > 0:
                average_salary = int(salary_sum // vacancies_processed)
            language_statistics = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': average_salary
            }
    return language_statistics


def get_language_statistic_sj(vacancies_found, pages, params, headers):
    language_statistics = {
        'vacancies_found': vacancies_found,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    vacancies_processed = 0
    page = 0
    salary_sum = 0
    while page <= pages:
        url = 'https://api.superjob.ru/2.33/vacancies/'
        params['page'] = page
        page_response = requests.get(url, headers=headers, params=params)
        page_response.raise_for_status()
        answer = page_response.json()['objects']
        page += 1
        for vacancy in answer:
            salary_from = vacancy['payment_from']
            salary_to = vacancy['payment_to']
            if not salary_from and not salary_to:
                continue
            average_salary_vacancy = predict_rub_salary(salary_from, salary_to)
            salary_sum += average_salary_vacancy
            vacancies_processed += 1
            average_salary = 0
            if vacancies_processed > 0:
                average_salary = int(salary_sum // vacancies_processed)
            language_statistics = {
                'vacancies_found': vacancies_found,
                'vacancies_processed': vacancies_processed,
                'average_salary': average_salary
            }
    return language_statistics
