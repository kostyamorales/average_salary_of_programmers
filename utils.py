from terminaltables import AsciiTable
import requests


def predict_rub_salary(salary_from, salary_to):
    if salary_from == 0:
        salary_from = None
    if salary_to == 0:
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


def create_table(statistics, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in statistics:
        table_data.append(
            [language, statistics[language]['vacancies_found'], statistics[language]['vacancies_processed'],
             statistics[language]['average_salary']])
    table = AsciiTable(table_data, title)
    print(table.table)


def get_statistics(place, vacancies_found, url, pages, params, headers=None):
    language_statistics = {}
    vacancies_processed = 0
    page = 0
    salary_sum = 0
    if vacancies_found == 0:
        language_statistics = {
            'vacancies_found': 0,
            'vacancies_processed': 0,
            'average_salary': 0
        }

    if place == 'sj':
        pages += 1  # в SuperJob, чтобы верно работала функция должно быть page <= pages, а в hh page < pages
    while page < pages:
        params['page'] = page
        page_response = requests.get(url, headers=headers, params=params)
        page_response.raise_for_status()
        if place == 'sj':
            answer = page_response.json()['objects']
        else:
            answer = page_response.json()['items']
        page += 1
        for vacancy in answer:
            if place == 'sj':
                salary_from = vacancy['payment_from']
                salary_to = vacancy['payment_to']
                if salary_from == 0 and salary_to == 0:
                    continue
            else:
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
