from urllib.parse import urlencode

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView, ListView

from webapp.forms import ArticleForm, SearchForm
from webapp.models import Article

class ArticleListView(ListView):
    #queryset = Article.objects.filter(title__contains='Article')
    model = Article
    template_name = "articles/index.html"
    ordering = ['-created_at']
    context_object_name = 'articles'
    paginate_by = 3

# Create your views here.
    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                Q(title__contains=self.search_value) | Q(author__contains=self.search_value)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context

class CreateArticleView(FormView):
    template_name = "articles/create_article.html"
    form_class = ArticleForm

    def form_valid(self, form):
        article = form.save()
        return redirect("article_detail", pk=article.pk)

class ArticleDetailView(TemplateView):
    template_name = "articles/article_detail.html"

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["article"] = self.article
        return context


class UpdateArticleView(FormView):
    template_name = "articles/update_article.html"
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
        return render(request, 'articles/delete_article.html')
    else:
        article = get_object_or_404(Article, pk=pk) #by this function you find the article
        article.delete()
        return redirect("articles")
