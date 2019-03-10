from django.conf.urls import url
from shazam import views
app_name = "shazam"

urlpatterns = [
    url(r'^$', views.index, name='index'),
]