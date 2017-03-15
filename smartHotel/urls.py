from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    #TODO : da rimuovere post debug
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('bacheca.urls')),
)
