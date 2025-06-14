from django.urls import re_path, path
from . import views

app_name = 'core'

urlpatterns = [
    # Con re_path catturi /, /home, /home/
    re_path(r'^$|^home$|^home/$', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('realtime-data/', views.get_realtime_data, name='realtime_data'),
]
