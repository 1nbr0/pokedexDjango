from django.shortcuts import render
import requests

# Create your views here.
url = "https://pokeapi.co/api/v2"


def index(request):
    pokemonArray = []
    for i in range(1, 11):
        pokemonArray.append(getPokemonById(i))
        i += 1

    backgroundColors = {
        "fire": "#FDDFDF",
        "grass": "#DEFDE0",
        "electric": "#FCF7DE",
        "water": "#DEF3FD",
        "ground": "#f4e7da",
        "rock": "#d5d5d4",
        "fairy": "#fceaff",
        "poison": "#98d7a5",
        "bug": "#f8d5a3",
        "dragon": "#97b3e6",
        "psychic": "#eaeda1",
        "flying": "#F5F5F5",
        "fighting": "#E6E0D4",
        "normal": "#F5F5F5"
        }

    colors = {
        "bug": "#8CB230",
        "dark": "#58575F",
        "dragon": "#0F6AC0",
        "electric": "#EED535",
        "fairy": "#ED6EC7",
        "fighting": "#D04164",
        "fire": "#FD7D24",
        "flying": "#748FC9",
        "ghost": "#556AAE",
        "grass": "#62B957",
        "ground": "#DD7748",
        "ice": "#61CEC0",
        "normal": "#9DA0AA",
        "poison": "#A552CC",
        "psychic": "#EA5D60",
        "rock": "#BAAB82",
        "steel": "#417D9A",
        "water": "#417D9A",
        }

    for pokemon in pokemonArray:
        pokemon["backgroundColor"] = backgroundColors[pokemon["types"][0]["type"]["name"]]
        pokemon["color"] = colors[pokemon["types"][0]["type"]["name"]]

    return render(request, "pokedex/index.html", {'pokemons': pokemonArray})


def getPokemonById(id):
    api = url + "/pokemon/" + str(id)
    r = requests.get(api)
    if r.status_code == 200:
        results = r.json()
        return results


def pokemonDetails(request, id):
    pokemonDetails = []

    pokemonDetails.append(getPokemonById(id))

    colors = {
        "fire": "#FDDFDF",
        "grass": "#DEFDE0",
        "electric": "#FCF7DE",
        "water": "#DEF3FD",
        "ground": "#f4e7da",
        "rock": "#d5d5d4",
        "fairy": "#fceaff",
        "poison": "#98d7a5",
        "bug": "#f8d5a3",
        "dragon": "#97b3e6",
        "psychic": "#eaeda1",
        "flying": "#F5F5F5",
        "fighting": "#E6E0D4",
        "normal": "#F5F5F5"
    }

    for pokemon in pokemonDetails:
        pokemon["color"] = colors[pokemon["types"][0]["type"]["name"]]

    return render(
        request,
        "pokedex/pokemonDetails.html",
        {'pokemons': pokemonDetails})
