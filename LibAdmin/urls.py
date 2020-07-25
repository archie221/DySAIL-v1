from django.urls import path
from . import views
from .views import passkeyView

urlpatterns = [
    path('', passkeyView.as_view(), name='lib-login'),
    path('search/', views.search, name='student-search'),
    path('info/<student_roll>', views.info_student, name='student-info'),
    path('logout/', views.logout, name='lib-logout'),
    path('occupied/<student_roll>', views.occupied_student, name='student-occupied'),
    path('idle/<student_roll>', views.idle_student, name='student-idle'),
    path('overnight/<student_roll>', views.idle_overnight, name='overnight-idle'),
    path('terminate/<student_roll>',views.terminate_student,name='student-terminate'),
    path('overidle/<student_roll>',views.overidle_student,name='student-overidle'),
]




