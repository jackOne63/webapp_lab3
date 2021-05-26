from .models import Link
from django.contrib.auth.models import User, Group
from rest_framework import serializers

class LinkSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = Link
        fields = ['url', 'create_date', 'link_to', 'link_from', 'user', 'counter']
        extra_kwargs = {'link_from': {'required': False, 'read_only' : True},
                        'create_date' :{'read_only' : True}, 'counter':{'read_only' : True}
        }

    def to_representation(self, instance):
        """Add to link from url of site"""
        ret = super().to_representation(instance)
        ret['link_from'] = "{0}://{1}/{2}/".format(self.context['request'].scheme, \
            self.context['request'].get_host(), ret['link_from'])
        return ret

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']