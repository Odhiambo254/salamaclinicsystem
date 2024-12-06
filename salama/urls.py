from django.urls import path
from . import views

urlpatterns = [


    # Root path directs to the login page
    path('', views.admin_login, name='login'),
    path('home', views.home, name='home'),

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
    # path('departments/', views.departments, name='departments'),

    # Book appointment path
    path('bookappointment/', views.book_appointment, name='bookappointment'),
    # path('pending', views.appointment_pending, name='pending'),
    path('bill', views.view_bills, name='bill'),
    path('paybills/<int:bill_id>/', views.pay_bill, name='pay_bill'),

    path('createbill/', views.create_bill, name='create_bill'),

]
