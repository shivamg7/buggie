from django import template

register = template.Library()

@register.filter(name='hash')
def hash(h, key):
    return h[key]

@register.filter(name='mul')
def mul(key):
    return key*20
