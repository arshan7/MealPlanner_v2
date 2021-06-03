from django import template

register = template.Library()


@register.simple_tag
def get_object_variable(c_object, variable):
    return getattr(c_object, variable)


@register.simple_tag
def get_dict_values(c_dict, key):
    if key in c_dict:
        return c_dict[key]
    else:
        return ""


@register.filter(name='index')
def array_item(c_list, index):
    if index < len(c_list):
        return c_list[index]
    return ""
