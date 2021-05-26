from django.views.generic.edit import FormView, DeleteView, CreateView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Link
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db.models import F

class LinkCreateView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('sign-in')
    template_name = 'shortlink/create-link.html'
    model = Link
    fields = ['link_to']
    title = 'create-link'


    def form_valid(self, form):
        form.instance.user = self.request.user
        link = form.save()
        link.save()
        context = self.get_context_data(form=form)
        context['new_link'] = link.link_from
        return self.render_to_response(context)
            

class LinksView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign-in')
    success_url = reverse_lazy('link-list')
    template_name = 'shortlink/links.html'
    title = 'links'
    paginate_by = 5

    def get_queryset(self):
        queryset = Link.objects.filter(user = self.request.user).order_by('-create_date')
        return queryset

class DeleteRedirectView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign-in')
    model = Link
    success_url = reverse_lazy('links')
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        self.object = get_object_or_404(Link, link_from=kwargs['link'])
        if request.user != self.object.user:
            raise PermissionDenied 
        self.object.delete()
        return HttpResponseRedirect(self.success_url)

class RedirectToView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        link = get_object_or_404(Link, link_from=kwargs['link'])
        link.counter = F("counter") + 1
        link.save(update_fields=["counter"])
        return link.link_to

class HomeView(TemplateView):
    template_name = 'shortlink/home.html'
    title = 'home'



class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('sign-in')
    template_name = 'shortlink/profile.html'
    title = 'profile'


class SignUpView(FormView):
    template_name = 'shortlink/sign-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('links')
    title = 'sign-up'
    
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.profile.birth_date = form.cleaned_data.get('birth_date')
        user.profile.gender = form.cleaned_data.get('gender')
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class SignInView(auth_views.LoginView):
    template_name = 'shortlink/sign-in.html'
    success_url = reverse_lazy('profile')
    title = 'sign-in'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or self.success_url

class SignOutView(auth_views.LogoutView):
    next_page = '/'
    