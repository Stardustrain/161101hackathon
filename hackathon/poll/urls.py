from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^poll_list/$',views.poll_list,name='poll_list'),
    url(r'^poll_edit/$',views.poll_edit,name='poll_edit'),
    url(r'^poll_detail/(?P<poll_id>\d+)/$',views.poll_detail,name='poll_detail'),
    url(r'^poll_result/(?P<poll_id>\d+)/$',views.poll_result,name='poll_result'),

]