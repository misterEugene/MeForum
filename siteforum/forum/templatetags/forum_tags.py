from django import template
from forum.models import *
from forum.views import menu

register = template.Library()

@register.simple_tag()
def get_categories():
    return Categories.objects.all()

@register.simple_tag()
def get_header_menu():
    return menu