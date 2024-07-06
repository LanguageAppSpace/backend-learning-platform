import markdown as md

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    html_content = md.markdown(value, extensions=["markdown.extensions.fenced_code"])
    return mark_safe(html_content)
