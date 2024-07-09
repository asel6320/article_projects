from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
from webapp.models import Article

class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by('-created_at')
        return render(request, 'index.html', context={"articles": articles})

# Create your views here.

class CreateArticleView(View):
    def dispatch(self, request, *args, **kwargs):
        print(request.POST)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create_article.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print("post")
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=request.POST['title'],
                content=request.POST['content'],
                author=request.POST['author']
            )
            tags = form.cleaned_data['tags']
            article.tags.set(tags)
            return redirect("article_detail", pk=article.pk)

        return render(
            request,
            'create_article.html',
            context={"form":form}
        )

class ArticleDetailView(TemplateView):
    #template_name = "article_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["article"] = self.article
        return context

    def get_template_names(self):
        #in here you can check something with if and else
        if self.article.tags.exists():
            return ["article_detail.html"]
        else:
            return ["test_detail.html"] #according to different if and else checkings, you can return different html files


def update_article(request, *args, pk, **kwargs):
    if request.method == "GET":
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(initial={
            "title": article.title,
            "author": article.author,
            "content": article.content,
            "tags": article.tags.all(),
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
            tags = form.cleaned_data['tags']
            article.tags.set(tags)
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
