from django.shortcuts import render, get_object_or_404
from.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    object_list = Post.published.all() # запрашиваем все "published" посты из базы данных
    paginator = Paginator(object_list, 3) #инициализир обж класса Paginator, указав кол-во постов на каждой странице
    page = request.GET.get('page') #Извлекаем из запроса GET параметр page, указывающий текущую стр
    try:
        posts = paginator.page(page) #получаем список обж на нужной стр с помощью метода page класса Paginator
    except PageNotAnInteger:
        #Если страница не целое число
        posts = paginator.page(1)
    except EmptyPage:
        #если номер страницы больше общего кол-ва страниц, возвращаем последнюю
        posts = paginator.page(paginator.num_pages)

    #posts = Post.published.all()
    #return render(request, 'blog/post/list.html', {'posts': posts})

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts}) #Передаём номер страницы и объекты в шаблон

def post_detail(request, year, month, day, post123):
    post = get_object_or_404(Post, slug=post123, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Функция возвращает объект по указанным параметрам или 404
    #slug (unique_for_date='publish'), поэтому у каждого поста уникальный slug, если они созданы в один день
    return render(request, 'blog/post/detail.html', {'post': post})


"""Контекст
 Если шаблон имеет вид  <p>Hello {% first_name %}.</p>
И если вы передаете переменную first_name в контексте:
render(request,'users/register.html', {'form': form, 'first_name': 'John'})
Шаблон будет отображать Hello John.
То, что вы предоставляете в контексте, доступно в шаблоне
"""




