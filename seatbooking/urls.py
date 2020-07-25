from django.urls import path
from . import views

urlpatterns = [
    path('booking/', views.booking, name='book-details'),
    path('book/multipleseat', views.multipleseat, name='book-multiple'),
    path('book/multipleseat/club_ids', views.club, name='club-ids'),
    path('book/',views.book, name='book-seat'),
    path('book/cancel/',views.cancel, name='cancel-seat'),
    path('view/', views.seatview, name='view-seats'),
    path('yes/<username>', views.yes_request, name='yes_clubrequest'),
    path('no/<username>', views.no_request, name='no_clubrequest'),
    path('end_club/', views.end_club, name='end-club'),
    path('hide/', views.hide, name='hide-identity'),
]