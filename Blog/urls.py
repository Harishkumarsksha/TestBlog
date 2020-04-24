from django.conf.urls import url, include
from Blog import views
from django.urls import path

urlpatterns = [

    url(r'^$', views.post_list_view),
    path('tag/<str:tag_slug>/', views.post_list_view,
         name='post_list_by_tag_name'),
    path('<int:year>/<int:month>/<int:day>/<str:post>/',
         views.post_detail_view, name='post_detail'),
    path('<int:id>/share/', views.mail_send_view, name='sendmail'),
]
