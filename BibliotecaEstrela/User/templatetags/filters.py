from django import template

register = template.Library()

@register.filter
def virgula(value):
    try:
        valor = float(value)
        return f'{valor:.2f}'.replace('.', ',')
    except:
        return value