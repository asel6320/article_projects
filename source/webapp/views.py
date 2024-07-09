from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.forms import ArticleForm
from webapp.models import Article
from webapp.validate import article_validate


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'index.html', context={"articles": articles})

def create_article(request):
    if request.method == 'GET':
        form = ArticleForm()
        print(form)
        return render(request, 'create_article.html', {'form': form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=request.POST['title'],
                content=request.POST['content'],
                author=request.POST['author']
            )
            tags = form.cleaned_data['tags']
            print(tags)
            article.tags.set(tags)
            return redirect("article_detail", pk=article.pk)

        return render(
            request,
            'create_article.html',
            context={"form":form}
        )

def article_detail(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    #try:
    #    article = Article.objects.get(id=pk)
    #except Article.DoesNotExist:
    #    raise Http404
    return render(request, 'article_detail.html', context={"article": article})

def update_article(request, *args, pk, **kwargs):
    if request.method == "GET":
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(initial={
            "title": article.title,
            "author": article.author,
            "content": article.content,
        })
        return render(
            request, "update_article.html",
            context={"form": form}
        )
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, pk=pk)
            article.title = request.POST.get("title")
            article.content = request.POST.get("content")
            article.author = request.POST.get("author")
            article.save()
            return redirect("article_detail", pk=article.pk)
        else:
            return render(
                request,
                "update_article.html",
                {"form": form}
            )

def delete_article(request, *args, pk, **kwargs):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'delete_article.html')
    else:
        article = get_object_or_404(Article, pk=pk) #by this function you find the article
        article.delete()
        return redirect("articles")
