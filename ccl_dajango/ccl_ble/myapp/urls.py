from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'main'

router = routers.DefaultRouter()
router.register(r'userstatus', views.UserStausViewSet)
router.register(r'checklog', views.CheckLogViewSet)

urlpatterns = [

    url(r'^',include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('signup/', views.signup, name='user_signup'),
    # path('login/', views.signin, name='user_login'),
    # path('logout/', views.signout, name='user_logout'),




]