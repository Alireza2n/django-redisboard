import django
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

if django.VERSION[:2] < (1, 7):
    admin.autodiscover()

urlpatterns = patterns("",
    url(r"^", include(admin.site.urls)),
)
