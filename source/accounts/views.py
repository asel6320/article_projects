
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import MyUserCreationForm, ProfileChangeForm, UserChangeForm
from accounts.models import Profile

# Create your views here.
User = get_user_model()

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_path = request.POST.get('next', "webapp:articles")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(next_path, "next_path")
            return redirect(next_path)
        else:
            context['has_error'] = True
    context["next_param"] = request.GET.get('next')
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('webapp:articles')

class RegistrationView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'registration.html'
    model = User

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:articles')
        return next_url

class ProfileView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user_obj'
    paginate_related_by = 3

    def get_context_data(self, **kwargs):
        articles = self.object.articles.order_by('-created_at')
        paginator = Paginator(articles, self.paginate_related_by)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['articles'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)

class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})