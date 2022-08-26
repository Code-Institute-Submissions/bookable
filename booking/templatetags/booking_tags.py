"""Booking Template Tags"""
from django import template
from django.templatetags.static import static
from django.utils.html import format_html

register = template.Library()

DATE_TIME_PICKER_FULL = static('js/jquery.datetimepicker.full.min.js')
DATE_TIME_PICKER = static('js/datetimepicker.js')
GOOGLE_MAP = static('js/google_map.js')


@register.simple_tag
def booking_static():
    """Template tag to return booking static files"""
    static_files = (
        '<script src="'
        f'{DATE_TIME_PICKER_FULL}'
        '"></script>'
        '<script src="'
        f'{DATE_TIME_PICKER}'
        '"></script>'
        '<script src="'
        f'{GOOGLE_MAP}'
        '"></script>'
    )

    return format_html(static_files)
