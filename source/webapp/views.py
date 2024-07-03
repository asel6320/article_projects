from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Article


# Create your views here.
def index(request):
    articles = Article.objects.order_by('-created_at')
    return render(request, 'index.html', context={"articles": articles})

def create_article(request):
    if request.method == 'GET':
        return render(request, 'create_article.html')
    else:
        article = Article.objects.create(
            title=request.POST.get("title"),
            content = request.POST.get("content"),
            author = request.POST.get("author")
        ) # v ideale vot zdes' doljna iiti proverka, chto priwli nujnye dannye i potom peredavat'
        #return HttpResponseRedirect(reverse("article_detail", kwargs={"pk": article.pk}))
        return redirect("article_detail", pk=article.pk)

def article_detail(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    #try:
    #    article = Article.objects.get(id=pk)
    #except Article.DoesNotExist:
    #    raise Http404
    return render(request, 'article_detail.html', context={"article": article})

def update_article(request, *args, pk, **kwargs):
    if request.method == 'GET':
        return render(
            request, "update_article.html",
            context={"article": get_object_or_404(Article, pk=pk)}
        )
    else:
        article = get_object_or_404(Article, pk=pk)
        article.title = request.POST.get("title")
        article.content = request.POST.get("content")
        article.author = request.POST.get("author")
        article.save()
        #by doing this function you will save all the cnages made to your article to the database
        return redirect("article_detail", pk= article.pk)

def delete_article(request, *args, pk, **kwargs):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'delete_article.html')
    else:
        article = get_object_or_404(Article, pk=pk) #by this function you find the article
        article.delete()
        return redirect("articles")
