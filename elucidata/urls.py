from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ques1$', views.ques1, name='ques1'),
    url(r'^ques2$', views.ques2, name='ques2'),
    url(r'^ques3$', views.ques3, name='ques3'),
    url(r'^ques4$', views.ques4, name='ques4'),
]