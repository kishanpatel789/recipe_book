from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return []
    return dictionary.get(str(key)) or dictionary.get(int(key)) or []
