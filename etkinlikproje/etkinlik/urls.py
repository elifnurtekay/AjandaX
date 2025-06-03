from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('update/<int:event_id>/', views.event_update, name='event_update'),
    path('delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('listele/', views.event_listele, name='event_listele'),
    path('istatistik/', views.event_istatistik, name='event_istatistik'),
]
