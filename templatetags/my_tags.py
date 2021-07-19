from django import template

register = template.Library()


@register.filter
def text2html(v1: str):
    return v1.replace("\n", "<br>").replace(" ", "&nbsp;").replace("\t", "&nbsp" * 4)


@register.filter
def contain(v1: str, v2: str):
    if v2 in v1:
        return True

@register.filter
def url(v1: str):
    if v1 == "":
        return "javascript:void(0)"

@register.filter
def get_dict(v1: dict, v2: str):
    return v1[v2]

@register.filter
def opposite(v1: bool):
    return not bool