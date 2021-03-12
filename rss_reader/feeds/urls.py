from django.urls import path # noqa

from . import views


app_name = "feeds"
urlpatterns = [
    path('', views.IndexView.as_view(), name='home')
]
