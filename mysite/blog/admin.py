from django.contrib import admin
from .models import Post

@admin.register(Post)   # то же самое что admin.site.register(Post): регистрирует декорируемый класс
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ("author",)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


