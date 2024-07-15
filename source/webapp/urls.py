from django.urls import path
from django.views.generic import RedirectView

from webapp.views import delete_article, ArticleListView, CreateArticleView, ArticleDetailView, UpdateArticleView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('', RedirectView.as_view(pattern_name="articles")), #you can change redirect to the main page
    path('create/', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', UpdateArticleView.as_view(), name='update_article'),
    path('article/<int:pk>/delete/', delete_article, name='delete_article')
]