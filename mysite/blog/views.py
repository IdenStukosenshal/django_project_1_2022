from django.shortcuts import render, get_object_or_404
from.models import Post

def post_list(request):
    posts = Post.published.all() # запрашиваем все "published" посты из базы данных
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


"""Контекст
 Если шаблон имеет вид  <p>Hello {% first_name %}.</p>
И если вы передаете переменную first_name в контексте:
render(request,'users/register.html', {'form': form, 'first_name': 'John'})
Шаблон будет отображать Hello John.
То, что вы предоставляете в контексте, доступно в шаблоне
"""




