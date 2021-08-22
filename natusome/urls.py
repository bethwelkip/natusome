from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static  # added

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send/$', views.send_message, name='send_message'),
    url(r'^receive/$', views.receive_message, name='receive_message'),
]
