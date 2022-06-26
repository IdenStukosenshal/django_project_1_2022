from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    """changefreq и priority показывают частоту обновления
страниц статей и степень их совпадения с тематикой сайта (максимальное значение 1)"""

    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj): # Метод lastmod принимает каждый объект из результата вызова items() и возвращает время последней модификации статьи
        return obj.updated
