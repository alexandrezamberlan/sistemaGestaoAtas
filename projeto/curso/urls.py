from django.conf.urls import url

from .views import CursoListView, CursoCreateView
from .views import CursoUpdateView, CursoDeleteView


urlpatterns = [
	url(r'list/$', CursoListView.as_view(), name='curso_list'),
	url(r'cad/$', CursoCreateView.as_view(), name='curso_create'),
	url(r'(?P<pk>\d+)/$', CursoUpdateView.as_view(), name='curso_update'),
	url(r'(?P<pk>\d+)/delete/$', CursoDeleteView.as_view(), name='curso_delete'), 
]
