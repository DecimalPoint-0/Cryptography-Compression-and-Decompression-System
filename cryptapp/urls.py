from unicodedata import name
from . import views
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('home', login_required(views.Index.as_view(), login_url='login'), name="index"),
    path('', views.loginPage, name="login"),
    path('register', views.UsersForm.as_view(), name="register"),
    path('home/about', views.about, name="about"),
    path('logout', views.log_out, name="logout"),
    re_path(r'^download/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}, name="details")
]


