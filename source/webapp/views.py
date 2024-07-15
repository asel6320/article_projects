from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView

from webapp.forms import ArticleForm
from webapp.models import Article

class ArticleListView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.order_by('-created_at')
        return render(request, 'index.html', context={"articles": articles})

# Create your views here.

class CreateArticleView(FormView):
    template_name = "create_article.html"
    form_class = ArticleForm

    def form_valid(self, form):
        article = form.save()
        return redirect("article_detail", pk=article.pk)

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


class UpdateArticleView(FormView):
    template_name = "update_article.html"
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs.get("pk"))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def form_valid(self, form):
        form.save()
        return redirect("article_detail", pk=self.article.pk)

def delete_article(request, *args, pk, **kwargs):
    if request.method == 'GET':
        article = get_object_or_404(Article, pk=pk)
        return render(request, 'delete_article.html')
    else:
        article = get_object_or_404(Article, pk=pk) #by this function you find the article
        article.delete()
        return redirect("articles")
