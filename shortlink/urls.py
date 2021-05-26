from django.urls import path
from django.urls.conf import include
from . import views
from . import api_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
#router.register(r'users', api_views.UserViewSet)
router.register(r'groups', api_views.GroupViewSet)
router.register(r'links', api_views.LinkViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/api-token-auth/', obtain_auth_token),
    path('', views.HomeView.as_view(), name='main'),
    path('account/', views.ProfileView.as_view(), name='profile'),
    path('account/sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('account/sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('account/sign-out/', views.SignOutView.as_view(), name='sign-out'),
    path('account/links/', views.LinksView.as_view(), name='links'),
    path('account/links/create', views.LinkCreateView.as_view(), name='create-link'),
    path('<str:link>/', views.RedirectToView.as_view(), name='redirect'),
    path('<str:link>/delete/', views.DeleteRedirectView.as_view(), name='redirect-delete')
]