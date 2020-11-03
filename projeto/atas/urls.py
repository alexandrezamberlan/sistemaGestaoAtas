from django.conf.urls import url

from .views import AtaListView, AtaCreateView, AtaDetailView
from .views import AtaUpdateView, AtaDeleteView


urlpatterns = [
	url(r'list/$', AtaListView.as_view(), name='ata_list'),
	url(r'cad/$', AtaCreateView.as_view(), name='ata_create'),
	url(r'(?P<pk>\d+)/$', AtaUpdateView.as_view(), name='ata_update'),
	url(r'(?P<pk>\d+)/detalhes/$', AtaDetailView.as_view(), name='ata_detail'),
	url(r'(?P<pk>\d+)/delete/$', AtaDeleteView.as_view(), name='ata_delete'), 
]
