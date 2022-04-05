import datetime

SIGNUP = {'email': 'admin@admin.ru', 'password': '12345678'}

PROFILE = {
    'first_name': 'Пётр-Петр',
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
    'name': 'Лекция супер хорошая лекция',
    'datetime': [str(datetime.datetime.now() + datetime.timedelta(days=2)) + ',' +
                 str(datetime.datetime.now() + datetime.timedelta(days=2, hours=1))],
    'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
    'hall_address': 'Москва, ул. Не московская, д. Домашний',
    'type': 'offline',
    'equipment': 'Руки, ноги, доска, полет.',
    'cost': '1000',
    'description': 'Отличное описание блин'
}

LECTURE_AS_CUSTOMER = LECTURE.copy()
LECTURE_AS_CUSTOMER['listeners'] = 200
