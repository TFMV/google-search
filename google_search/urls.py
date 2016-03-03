"""google_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from app.ajax import GoogleSearchView

urlpatterns = [
    url(r'^$', 'app.views.home'),
    url(r'^signin/$', 'app.views.signin'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/search/$', GoogleSearchView.as_view()),
]
