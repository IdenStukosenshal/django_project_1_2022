from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    #path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'), # name='post_list' это имя URL, которое будет использовано, чтобы идентифицировать его
    path('<int:year>/<int:month>/<int:day>/<slug:post123>/', views.post_detail, name='post_detail'), # reverse('blog:post_detail', ...
    path('<int:post_id>/share/', views.post_share, name='post_share') # получаем url из detail/html


]

# значение, определенное в шаблоне как <parameter>, возвраща-
# -ется в виде строки в ф-цию views.post_detail, преобразовываем в int первые 3
# slug - функция, преобр к виду: цифры, буквы, "-", "_"
