from . import views
from django.urls import path


urlpatterns = [
    # Path Principal (view)
    path('', views.index, name="index"),
    path('pokemon/<int:id>', views.pokemonDetails, name="pokemon-details"),
    path('team', views.pokemonTeamView, name="team"),


    # Path team utilisateur (action)
    path('updateTeamTitle', views.updateTeamTitle, name="updateTeamTitle"),
    path('addPokemon', views.addPokemonInCurrentTeam, name="addPokemon"),
    path('removePokemon', views.removePokemonInCurrentTeam, name="removePokemon"),
    path('createTeam', views.createTeam, name="createTeam"),
    path('removeTeam', views.removeTeam, name="removeTeam"),


    # Path compte utilisateur (view)
    path('register', views.RegisterView, name="register"),
    path('login', views.LoginView, name="login"),
    path('logout', views.LogoutView, name="logout"),
    path('dashboard', views.dashboardView, name="dashboard")
]