from django import template
from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

"""Для того чтобы зарегистрировать наши теги, каждый модуль с функциями тегов должен определять переменную
 register. Эта переменная является объектом класса template.Library и используется 
для регистрации пользовательских тегов и фильтров в системе. В файле мы определяем тег total_posts, 
реализованный в виде функции, и оборачиваем его в декоратор @register.simple_tag 
для регистрации нового тега. Django будет использовать название функции в качестве названия тега. 
Однако можно указать явно, как обращаться к тегу из шаблонов. Для этого достаточно передать в де-
коратор аргумент name –    @register.simple_tag(name='my_tag')."""


register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts} # Инклюзивные теги должны возвращать только словари контекста, который затем будет использован для формирования HTML-шаблона
#Чтобы задать любое другое количество статей, используйте такую запись: {% show_latest_posts число %}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')  # {{ variable|markdown }} # https://daringfireball.net/projects/markdown/basics
def markdown_format(text):
    return mark_safe(markdown.markdown(text)) # используем функцию mark_safe, чтобы пометить результат работы фильтра как HTML-код, который нужно учитывать при построении шаблона
