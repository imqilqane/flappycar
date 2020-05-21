from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('results/<str:search>/', views.SearchResult, name='results'),
    path('details/<str:ebay_link>/', views.DetailsView, name='details'),

]