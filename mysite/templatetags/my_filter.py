import markdown
from django.utils.safestring import mark_safe
# 특수문자 같은 것이 해석이 안 될때가 있는데 그런 것들을 mark_safe로 안전하게 저장해준다.

from django import template

register = template.Library()

# (val1-val2)의 결과를 반환
@register.filter
def minus(val1, val2):
    return val1 - val2

# 쿼리 스트링 추가
# query_string 사용자 정의 필터
# 내용을 가져다가 쿼리를 만들어서 작성하자(이게 기본 작성내용, 다른 프로젝트에도 똑같이 사용 가능)
@register.simple_tag(takes_context=True)
def query_string(context, **kwargs):
    query_dict = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return query_dict.urlencode()

# 마크다운 변환
@register.filter
def markdown_to_html(value):
    extensions = [
        'nl2br',
        'fenced_code',
    ]
    return mark_safe(markdown.markdown(value, extensions=extensions))