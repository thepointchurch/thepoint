import re

from django import template

register = template.Library()


def multiple_replace(text, adict):
    matcher = re.compile("|".join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return matcher.sub(one_xlat, text if isinstance(text, str) else str(text))


@register.filter
def smartquote(value):
    return multiple_replace(value, {"'": "’", ' "': " “", '" ': "” "})
