from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('',                          views.invitation_view,       name='invitation'),
    path('dashboard/',                views.dashboard_view,        name='dashboard'),

    # API RSVP
    path('rsvp/',                     views.rsvp_view,             name='rsvp'),

    # API Invitations
    path('invitations/<int:invitation_id>/delete/', views.delete_invitation_view, name='delete_invitation'),

    # API Dons
    path('dons/add/',                 views.add_don_view,          name='add_don'),
    path('dons/<int:don_id>/delete/', views.delete_don_view,       name='delete_don'),
]