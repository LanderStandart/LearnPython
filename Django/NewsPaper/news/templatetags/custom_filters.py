from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    value = value.replace('Ковид','*Болезнь о которой не стоит говорить*')
    value = value.replace('Навальный','*Имя которое нестоит называть')
    value = value.replace('кризис','*временные трудности*')
    
    return str(value)