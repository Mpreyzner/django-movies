from django.conf.urls import include, url

try:
    from django.conf.urls import patterns
except ImportError:
    pass
from . import views

urlpatterns = [
    url(r'^movies/$', views.MovieAPIListView.as_view()),
    url(r'^comments/$', views.CommentAPIListView.as_view()),
    url(r'^top/$', views.TopAPIListView.as_view()),

]
