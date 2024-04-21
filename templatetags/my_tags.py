from django import template
from django.utils.safestring import mark_safe
 
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]