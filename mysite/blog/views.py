from django.shortcuts import render, get_object_or_404, redirect
from.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm1, CommentForm, SearchForm, CreatePostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def post_list(request, tag_slug=None):
    object_list = Post.published.all() # запрашиваем все "published" посты из базы данных

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) #инициализир обж класса Paginator, указав кол-во постов на каждой странице
    page = request.GET.get('page') #Извлекаем из запроса GET параметр page, указывающий текущую стр
    try:
        posts = paginator.page(page) #получаем список обж на нужной стр с помощью метода page класса Paginator, после объект передаётся в list.html, в конце передаётся в pagination.html
    except PageNotAnInteger:  # Если страница не целое число
        posts = paginator.page(1)
    except EmptyPage:  # если номер страницы больше общего кол-ва страниц, возвращаем последнюю
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  {'page': page, 'posts': posts, 'tag': tag})  # Передаём номер страницы и объект в шаблон

    #posts = Post.published.all()
    #return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post123): #slug (unique_for_date='publish'), поэтому у каждого поста уникальный slug, если они созданы в один день
    post = get_object_or_404(Post, slug=post123, status='published', publish__year=year,
                             publish__month=month, publish__day=day)  # Функция возвращает объект по указанным параметрам или 404


    '''Список активных комментариев для статьи'''
    comments = post.comments.filter(active=True) #менеджер определён в модели, related_name
    new_comment = None
    if request.method == 'POST':  # если коммент отправлен
        comment_form = CommentForm(data=request.POST) #заполняем форму данными из запроса
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) # создаём но не сохраняем в бд
            new_comment.post = post # привязываем комм к статье
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True) #  получает все ID тегов текущей статьи. Метод QuerySet’а values_list() возвращает кортежи со значениями заданного поля. Мы указали flat=True, чтобы получить «плоский» список вида [1, 2, 3, ...]
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #  получает все статьи, содержащие хоть один тег из полученных ранее, исключая текущую статью
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] #  использует функцию агрегации Count для формирования вычисляемого поля same_tags, которое  содержит определенное количество совпадающих тегов
    # сортирует список опубликованных статей в убывающем порядке по количеству совпадающих тегов для
    # отображения первыми максимально похожих статей и делает срез результата для отображения только четырех статей
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment, 'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


"""Контекст
 Если шаблон имеет вид  <p>Hello {% first_name %}.</p>
И если вы передаете переменную first_name в контексте:
render(request,'users/register.html', {'form': form, 'first_name': 'John'})
Шаблон будет отображать Hello John.
То, что вы предоставляете в контексте, доступно в шаблоне
"""


class PostListView(ListView):
    """Аналог post_list"""
    queryset = Post.published.all()  #если использовать model=Post, будет менеджер по умолчанию (objects)
    context_object_name = "posts"  # если не использовать, по умолчанию переменная контекста будет object_list
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id): # Получение статьи по id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST': #Форма была отправлена на сохранение, отправляется методом POST, если GET - пустая форма
        form = EmailPostForm1(request.POST)
        if form.is_valid():
            cd = form.cleaned_data #словарь с полями формы и их значениями, если валидац не пройдена то в cleaned_data попадут только корректные поля
            post_url = request.build_absolute_uri(post.get_absolute_url()) #абсолютная ссылка на статью
            subject = f'{cd["name"]} ({cd["email"]}) recommends you reading" {post.title}"'
            message = f'Read"{post.title}" at {post_url}\n\n{cd["name"]}\'s comments: {cd["comments"]}'
            send_mail(subject, message, '', [cd["to"], ]) # https://django.fun/docs/django/ru/4.0/topics/email/
            sent = True # Требуются параметры subject, message, from_email и recipient_list, from_email: Строка. Если None, Django будет использовать значение параметра DEFAULT_FROM_EMAIL
    else:
        form = EmailPostForm1()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

# GET запрос используется чтобы получить данные, а POST чтобы отправить.

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET) # Поисковый запрос будет отправляться методом GET, чтобы результирующий URL содержал в себе фразу поиска в параметре query
    if form.is_valid():
        query = form.cleaned_data['query']
        #results = Post.objects.annotate(search=SearchVector('title', 'body'), ).filter(search=query)

        #search_vector = SearchVector('title', 'body')
        #search_query = SearchQuery(query)
        # results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        #results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        results = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter().order_by('-similarity')  # https://gis.stackexchange.com/questions/195207/how-to-instal-pg-trgm-on-windows
        #results = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.3).order_by('-similarity')
    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results}) # filter(similarity__gt=0.3) не работает    https://qna.habr.com/q/514293










def create_post(request):
    new_post = None
    if request.method == 'POST':
        post_form = CreatePostForm(data=request.POST)
        if post_form.is_valid():
            new_post = post_form.save()
            return redirect('blog:post_list')

    else:
        post_form = CreatePostForm()
    return render(request, 'blog/post/createpost.html', {'post_form': post_form, })

