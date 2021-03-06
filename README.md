# Average salary of programmers

## Получаем статистику по средней зарплате программистов.

Проект использует ресурсы HeadHunter и SuperJob, чтобы узнать общее количество вакансий и посмотреть среднюю зарплату по языкам программирования: JavaScript, Java, Python, Ruby, PHP, C++, C#, C, Go, Shell, Objective-C, Scala, Swift, TypeScript.

## Подготовка к работе
1. Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
2. Для работы программы нужно получить ключ к API SuperJob. [Зарегистрируйте приложение](https://api.superjob.ru/register/) и получите его `secret key`.
Создайте файл `.env` в головном каталоге. Внутри файла напишите 
```
SJ_API_KEY=secret_key
```
где вместо `secret_key` укажите ключ вашего аккаунта.

## Запуск программы

Из головного каталога запустите программу следующей командой
```
python main.py
```
Результаты выведутся на экран в виде таблицы.

## Цель проекта

 Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/)
