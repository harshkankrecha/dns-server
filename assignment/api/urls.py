
"""
In app's urls.py, we write all the urls path which renders each of the APIs in the views.py
"""


from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('get/<str:name>/', views.get_data, name='getdata'),
    path('post/', views.post_data, name='postdata'),
    path('update/<str:name>/', views.update_data, name='updatedata'),
]

