from django.urls import path
from . import views
app_name = 'accounts'
#app_name = namespace
urlpatterns =[
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('update/', views.user_update, name='update'),
    path('change/', views.change_password, name='change'),
    path('phone_login/', views.phone_login, name='phone_login'),
    path('verify/', views.verify, name='verify'),
]