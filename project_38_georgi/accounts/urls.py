from django.urls import path

from project_38_georgi.accounts.views import index

urlpatterns = [
    path('', index, name='index'),
]
