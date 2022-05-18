from datetime import timezone, timedelta, datetime

import pytz

SIGNUP = {'email': 'admin@admin.ru', 'password': '12345678'}
SIGNUP2 = {'email': 'admin2@admin.ru', 'password': '12345678'}

PROFILE = {
    'first_name': 'Пётр-Петр',
    'bgc_number': '1',
    'last_name': 'Петр',
    'middle_name': 'Петрович',
    'birth_date': '2020-01-18',
    'description': 'Описанюшка',
}

LECTURER = {
    'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
    'performances_links': [
        'https://dev.lectonic.ru/city/?name=Москова',
        'http://dev.lectonic.com/com/com'
    ],
    'publication_links': [
        'https://dev.lectonic.ru/city/?name=Москова',
        'http://dev.lectonic.com/com/com'
    ],
    'education': 'У меня нереально высокое образование, я прям не могу',
    'hall_address': 'Москва, ул. Не московская, д. Домашний',
    'equipment': 'Руки, ноги, доска, полет.'
}

CUSTOMER = {
    'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
    'hall_address': 'Москва, ул. Не московская, д. Домашний',
    'equipment': 'Руки, ноги, доска, полет.',
    'company_name': 'Парвим',
    'company_description': 'kdmcsld',
    'company_site': 'dlcksmdl'
}

LECTURE = {
    'svg': 1,
    'name': 'Лекция супер хорошая лекция',
    'datetime': [
        (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M') +
        ',' +
        (datetime.now() + timedelta(days=2, hours=1)).strftime('%Y-%m-%dT%H:%M')],
    'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
    'hall_address': 'Москва, ул. Не московская, д. Домашний',
    'type': 'offline',
    'equipment': 'Руки, ноги, доска, полет.',
    'cost': '1000',
    'description': 'Отличное описание блин'
}
LECTURE_AS_CUSTOMER = LECTURE.copy()
LECTURE_AS_CUSTOMER['listeners'] = 200
