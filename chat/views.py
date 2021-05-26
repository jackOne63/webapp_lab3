from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from channels.layers import get_channel_layer
from shortlink.models import Link
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from asgiref.sync import async_to_sync
from .models import ConnectedUsers

class ChatView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('sign-in')
    template_name = 'shortlink/chat.html'
    title = 'chat'

class ChatUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('sign-in')
    template_name = 'shortlink/chat-users.html'
    title = 'chat-users'   
    paginate_by = 5

    def get_queryset(self):
        queryset = ConnectedUsers.objects.all().order_by('-connected')
        return queryset

    def test_func(self):
        return self.request.user.is_staff 
    

def webhook(request, link):
    object = get_object_or_404(Link, link_from=link)
    if request.user != object.user:
        raise PermissionDenied 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_user", {
            'type' : "chat_link",
            "link_from": object.link_from,
            "link_to": object.link_to,
            "counter": object.counter,
            "name": request.user.username,
        })
    return HttpResponse("Send in chat")