from django.urls import path
from . import views

urlpatterns = [
    # Root path directs to the login page
    path('', views.admin_login, name='login'),

    # Logout path
    path('logout/', views.logout, name='logout'),

    # Signup path
    path('signup/', views.admin_signup, name='signup'),

    # Password reset path
    path('passwordreset/', views.password_reset, name='password_reset'),

    # Dashboard path
    path('dashboard/', views.dashboard, name='dashboard'),

    # Register patient path
    path('register/', views.register_patient, name='registerpatient'),

    # Check returning patient path
    path('checkpatient/', views.check_returning_patient, name='checkpatient'),
    path('about/', views.about, name='About'),

    # Book appointment path
    path('bookappointment/', views.book_appointment, name='bookappointment'),
]
