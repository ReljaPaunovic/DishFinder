from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^recipe/(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe'),
	url(r'^search/(?P<search_param>.+)/$', views.search_result, name='search result'),
]