from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

from django.utils.text import slugify
''''''

class PublishedManager(models.Manager):
    """"""
    def get_queryset(self):  #Queryset коллекция объектов, полученных из базы данных
        return super().get_queryset().filter(status='published')  # метод get_queryset() менеджера возвращает Queryset, переопределили и добавили фильтр


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # Один ко многим
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # менеджер по умолчанию
    published = PublishedManager()  # новый менеджер

    tags = TaggableManager()

    def get_absolute_url(self):
        """Возвращает ссылку на пост
        reverse() дает возможность получать URL, указав имя
        шаблона и параметры"""
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    class Meta:
        ordering = ('-publish',)  # по убыванию даты "-"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)  # попробовать добавить в прошлый проект генерацию слага

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #один ко многим,
    name = models.CharField(max_length=80) # Атрибут related_name позволяет получить доступ к комментариям конкретной статьи. Теперь мы сможем обращаться к статье из комментария, используя запись comment.post, и к комментариям статьи при помощи post.comments.all()
    email = models.EmailField()
    body = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) # Для возможности скрыть некоторые сообщения

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post} .'




