from django.urls import path
# from django.contrib.auth.views import login
from users import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('send_code/', views.send_code, name='send_code'),
]
