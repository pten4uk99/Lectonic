from .base import FilterField

__all__ = [
    'CUSTOMER_LECTURE_FILTER_FIELDS',
    'LECTURER_LECTURE_FILTER_FIELDS',
    'POTENTIAL_LECTURER_LECTURE_FILTER_FIELDS',
    'POTENTIAL_CUSTOMER_LECTURE_FILTER_FIELDS',
    'LECTURER_FILTER_FIELDS',
    'CUSTOMER_FILTER_FIELDS',
]


POTENTIAL_LECTURER_LECTURE_FILTER_FIELDS = [
        FilterField('city', 'customer__person__city_id'),
        FilterField('domain', 'lecture_domains__domain_id'),
    ]

POTENTIAL_CUSTOMER_LECTURE_FILTER_FIELDS = [
        FilterField('city', 'lecturer__person__city_id'),
        FilterField('domain', 'lecture_domains__domain_id'),
    ]

LECTURER_LECTURE_FILTER_FIELDS = [
        FilterField('city', 'lecturer__person__city_id'),
        FilterField('domain', 'lecture_domains__domain_id'),
    ]


CUSTOMER_LECTURE_FILTER_FIELDS = [
        FilterField('city', 'customer__person__city_id'),
        FilterField('domain', 'lecture_domains__domain_id'),
    ]

LECTURER_FILTER_FIELDS = [
        FilterField('city', 'person__city_id'),
        FilterField('domain', 'lecturer_domains__domain_id'),
    ]

CUSTOMER_FILTER_FIELDS = [
        FilterField('city', 'person__city_id'),
        FilterField('domain', 'customer_domains__domain_id'),
    ]
