from django.urls import path,include
from . import views
from .views import chatView,chatboxView

urlpatterns = [
    path('', views.home, name='student-home'),
    path('gadgets/',views.gadgets, name='gadgets'),
    path('gadgets/update/',views.updateGadget, name='update_gadgets' ),
    path('chat/', chatView.as_view(), name='chat'),
    path('chat/<receiver_username>/', chatboxView.as_view(), name='chatbox'),
    path('notification/',views.notifications,name='notices'),
    path('notification/delete',views.notifications_delete,name='delete_notices'),
    #for seatbooking app
    path('seats/',include('seatbooking.urls'))
]