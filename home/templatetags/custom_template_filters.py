from django.template import Library
from time import strptime, strftime

register = Library()
"""2024-04-12T12:37:21.1421869Z"""


@register.filter
def change_timestamp(value):
    time_obj = strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    result = strftime('%H:%M:%S on %Y/%m/%d', time_obj)
    return result