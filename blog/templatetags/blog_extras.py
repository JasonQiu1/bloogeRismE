import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def bloogerify(value):
    return value;
    return re.sub(r'^My|\b[mM]y\b', 'Blooger\'s',
            re.sub(r'\bI\b', 'me', 
                re.sub(r'^I\b|(\. |>)I\b', r'\1Me', 
                    re.sub(r'\b[mM]e\b', 'Blooger', value)
                )
            )
    )
