from django.urls import path
from . import views
from .views import search_results


urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', search_results, name='search_results'),
]
