from django.urls import path
from . import views

urlpatterns = [
    path('', views.invitation_page, name='invitation'),
    path('rsvp/', views.rsvp_submit, name='rsvp_submit'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
