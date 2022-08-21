"""Booking Template Tags"""
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def booking_static():
    """Template tag to return booking static files"""
    static = (
        '<script type="text/javascript" src="'\
            '/static/js/jquery.datetimepicker.full.min.js"></script>'
        '<script type="text/javascript" src="/static/js/datetimepicker.js"></script>'
        '<script type="text/javascript" src="/static/js/google_map.js"></script>'
    )

    return format_html(static)
