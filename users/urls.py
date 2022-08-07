from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profiles/', views.profiles, name="profiles"),
    path('account/', views.adminAccount, name="account"),
    path('edit-account/', views.editAdminAccount, name="edit-account"),
]
