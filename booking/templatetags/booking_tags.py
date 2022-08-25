"""Booking Template Tags"""
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def booking_static():
    """Template tag to return booking static files"""
    static = (
        '<script type="text/javascript" src="'
        'https://res.cloudinary.com/daxqnc8yw/raw/upload/'
        'v1661260312/static/js/jquery.datetimepicker.full.min.349b0ca1b372.js'
        '"></script>'
        '<script type="text/javascript" src="https://res.cloudinary.com/'
        'daxqnc8yw/raw/upload/v1661260313/static/js/datetimepicker.'
        '1da7b1691d0f.js"></script>'
        '<script type="text/javascript" src="https://res.cloudinary.com/'
        'daxqnc8yw/raw/upload/v1661260312/static/js/google_map.'
        'b070891af348.js"></script>'
    )

    return format_html(static)
