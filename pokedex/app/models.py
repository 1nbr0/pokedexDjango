from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# Extension de user pour mettre la currentteam
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentTeam = models.IntegerField(blank=True, null=True, unique=True)


# Les équipes de pokémon
class PokeTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(blank=True, null=True, max_length=100)
    idPokemon1 = models.IntegerField(blank=True, null=True)
    idPokemon2 = models.IntegerField(blank=True, null=True)
    idPokemon3 = models.IntegerField(blank=True, null=True)
    idPokemon4 = models.IntegerField(blank=True, null=True)
    idPokemon5 = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(blank=True, null=True)


# Pokémon
class Pokemon(models.Model):
    idPokemon = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=100)
    img = models.CharField(blank=True, null=True, max_length=1000)
    type = models.CharField(blank=True, null=True, max_length=100)
    color = models.CharField(blank=True, null=True, max_length=100)
    backgroundColor = models.CharField(blank=True, null=True, max_length=100)
