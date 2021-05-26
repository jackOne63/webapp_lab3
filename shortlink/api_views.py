from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, LinkSerializer
from .models import Link  
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from util.tasks import mailGroup

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(methods=['POST'], detail=True,
    url_name='mail_send', url_path='mail-send')
    def mailSend(self, request, pk=None):
        if 'subject' not in request.data:
            return Response({"Missing subject"}, status=status.HTTP_400_BAD_REQUEST)
        if 'text' not in request.data:
            return Response({"Missing text"}, status=status.HTTP_400_BAD_REQUEST)
        if Group.objects.filter(id=pk).count() == 0:
            return Response({"Invalid group"}, status=status.HTTP_404_NOT_FOUND)
        mail_text = request.data['text']
        subject = request.data['subject']
        mailGroup.delay(pk,subject, mail_text)
        return Response({'In executing %s:%s' % (pk, mail_text)})


class LinkViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    API endpoint that allows links to be viewed or edited.
    """
    queryset = Link.objects.all().order_by('-create_date')
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user = self.request.user)