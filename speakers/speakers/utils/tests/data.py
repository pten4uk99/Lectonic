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
    'equipment': 'Руки, ноги, доска, полет.'
}

LECTURE = {
    'name': 'Лекция супер хорошая лекция',
    'time_start': '15:30',
    'time_end': '16:00',
    'date': datetime.date.today() + datetime.timedelta(days=2),
    'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
    'hall_address': 'Москва, ул. Не московская, д. Домашний',
    'type': 'offline',
    'equipment': 'Руки, ноги, доска, полет.',
    'cost': '1000',
    'description': 'Отличное описание блин'
}
