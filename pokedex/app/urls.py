from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name="index"),
    path('pokemon/<int:id>', views.pokemonDetails, name="pokemon-details"),


    # Path compte utilisateur
    path('register', views.RegisterView, name="register"),
    path('login', views.LoginView, name="login"),
    path('logout', views.LogoutView, name="logout"),
    path('dashboard', views.dashboardView, name="dashboard")
]