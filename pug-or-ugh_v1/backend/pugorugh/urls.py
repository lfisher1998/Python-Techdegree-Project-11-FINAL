from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView

from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^api/user/preferences/$', 
        views.CreateUpdateViewUserPref.as_view(), name='user-pref'), 
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<status>[\w\-]+)/$',
        views.UpdateStatus.as_view(), name='UpdateStatus'),
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<status>[\w\-]+)/next/$',
        views.NextDogView.as_view(), name='NextDog'),
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/$',
        views.UpdateUndecided.as_view(), name='UpdateUndecided'),   
    url(r'^api/dogs/$', 
        views.ListDogsView.as_view(), name='ListDogs'),
    url(r'api/dogs/(?P<status>[\w\-]+)/$',
        views.ListDogsStatusView.as_view(), name='ListDogsStatus'),   
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),    
    
])