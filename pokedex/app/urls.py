from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name="index"),
    path('pokemon/<int:id>', views.pokemonDetails, name="pokemon-details")
]