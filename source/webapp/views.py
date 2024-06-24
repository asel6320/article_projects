from django.http import HttpResponseRedirect
from django.shortcuts import render

from webapp.article_db import ArticleDb
from webapp.models import Article


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'index.html', context={"articles": articles})

def create_article(request):
    if request.method == 'GET':
        return render(request, 'create_article.html')
    else:
        Article.objects.create(
            title=request.POST.get("title"),
            content = request.POST.get("content"),
            author = request.POST.get("author")
        ) # v ideale vot zdes' doljna iiti proverka, chto priwli nujnye dannye i potom peredavat'

        return HttpResponseRedirect('/')

def article_detail(request, article_id):
    pass