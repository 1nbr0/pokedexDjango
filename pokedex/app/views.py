from django.shortcuts import render
import requests
from django.shortcuts import redirect

# Import des models
from .models import PokeTeam
from .models import Pokemon
from .models import UserInfo

# Import pour compte utilisateur
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

import httpx
import asyncio
from asgiref.sync import sync_to_async

# Create your views here.
url = "https://pokeapi.co/api/v2/pokemon/"

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
            "normal": "#F5F5F5",
            "ghost": "#F5F5F5",
            "ice": "#74C1D9",
            "dark": "#848484",
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


@sync_to_async
def getIsUserAuthenticated(request):
    return request.user.is_authenticated


async def index(request):
    user = await getIsUserAuthenticated(request)

    urlPage = 'https://pokeapi.co/api/v2/pokemon/'
    page = []
    pokemonArray = []
    error = ""
    search = None
    if (request.GET.get('search')):
        search = False
    else:
        search = True

    if (request.POST.get('next')):
        urlPage = request.POST.get('next')
    elif (request.POST.get('previous')):
        urlPage = request.POST.get('previous')
    else:
        urlPage = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=30"

    async with httpx.AsyncClient() as client:
        responses = await asyncio.gather(*[getPagination(urlPage, client)])
        for response in responses:
            page = response

    context = {'user': user, 'pagination': page, 'search': search, 'pokemons': pokemonArray,'error': error}

    if (request.GET.get('search')):
        try:
            async with httpx.AsyncClient() as client:
                responses = await asyncio.gather(*[getPokemonByIdAsync(request.GET['search'].lower(), client) for i in range(1, 2)])
                for response in responses:
                    pokemonArray.append(response)
            return render(request, "pokedex/index.html", context)
        except:
            return render(request, "pokedex/index.html", context)

    else:
        pokemonOnPage = []
        async with httpx.AsyncClient() as client:
            responses = await asyncio.gather(*[getPokemonPageAsync(client, urlPage)])
            for response in responses:
                pokemonOnPage = response
        try:
            async with httpx.AsyncClient() as client:
                responses = await asyncio.gather(*[getPokemonByIdAsync(pokemon['name'], client) for pokemon in pokemonOnPage])
                for response in responses:
                    pokemonArray.append(response)
            return render(request, "pokedex/index.html", context)
        except:
            pokemonArray = []
            error = "ERREUR : Si le problème persiste, essayer de changer de connexion."
            return render(request, "pokedex/index.html", context)


async def getPagination(urlPage, client):
    r = await client.get(urlPage)
    results = r.json()
    pagination = {"next": results["next"], "previous": results["previous"]}
    return pagination


async def getPokemonPageAsync(client, urlPage):
    r = await client.get(f'{urlPage}')
    results = r.json()
    return results["results"]


async def getPokemonByIdAsync(id, client):
    api = f'{url}{id}'
    r = await client.get(api)

    results = r.json()
    pokemon = {
        "id": results["id"],
        "name": results["name"],
        "img": results["sprites"]["other"]["home"]["front_default"],
        "type": results["types"][0]["type"]["name"],
        "color": colors[results["types"][0]["type"]["name"]],
        "backgroundColor": backgroundColors[results["types"][0]["type"]["name"]]
    }
    return pokemon


def getPokemonById(id):
    api = f'{url}{id}'
    r = requests.get(api)
    if r.status_code == 200:
        results = r.json()
        return results


def pokemonDetails(request, id):
    pokemonDetails = []
    id = id
    if (request.POST.get('id')):
        id = request.POST.get('id')
        
    pokemonDetails.append(getPokemonById(id))
    urlDetails = f'https://pokeapi.co/api/v2/pokemon-species/{id}'
    r = requests.get(urlDetails)
    results = r.json()

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
        "normal": "#F5F5F5",
        "ghost": "#F5F5F5",
        "ice": "#74C1D9",
        "dark": "#848484",
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

    for pokemon in pokemonDetails:
        pokemon["backgroundColor"] = backgroundColors[pokemon["types"][0]["type"]["name"]]
        pokemon["color"] = colors[pokemon["types"][0]["type"]["name"]]
    Next = 1
    if(id is 1000):
        Next = 1000
    else:
        Next = id + 1
    Previous = 1
    if(id is 1):
        Previous = 1
    else:
        Previous = id - 1
    return render(request, "pokedex/pokemonDetails.html", {'pokemons': pokemonDetails, 'pokemonDetails': results, 'Previous': Previous, 'Next': Next})


# Gestion des équipes


# Modifier le titre de l'équipe actuelle
def updateTeamTitle(request):
    if request.user.is_authenticated:
        if (request.POST.get('title')):
            userInfo = UserInfo.objects.get(user=request.user)
            userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
            userCurrentTeam.title = request.POST['title']
            userCurrentTeam.save()
        return redirect('dashboard')
    else:
        return redirect('login')


# Ajoute un pokémon dans l'équipe d'un utilisateur
def addPokemonInCurrentTeam(request):
    if request.user.is_authenticated:
        if (request.POST.get('id')):
            userInfo = UserInfo.objects.get(user=request.user)
            userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
            if (userCurrentTeam.idPokemon1 is None):
                addPokemonInDB(request.POST.get('id'))
                userCurrentTeam.idPokemon1 = request.POST.get('id')
                userCurrentTeam.save()
            elif (userCurrentTeam.idPokemon2 is None):
                addPokemonInDB(request.POST.get('id'))
                userCurrentTeam.idPokemon2 = request.POST.get('id')
                userCurrentTeam.save()
            elif (userCurrentTeam.idPokemon3 is None):
                addPokemonInDB(request.POST.get('id'))
                userCurrentTeam.idPokemon3 = request.POST.get('id')
                userCurrentTeam.save()
            elif (userCurrentTeam.idPokemon4 is None):
                addPokemonInDB(request.POST.get('id'))
                userCurrentTeam.idPokemon4 = request.POST.get('id')
                userCurrentTeam.save()
            elif (userCurrentTeam.idPokemon5 is None):
                addPokemonInDB(request.POST.get('id'))
                userCurrentTeam.idPokemon5 = request.POST.get('id')
                userCurrentTeam.save()
            if ((userCurrentTeam.idPokemon1 is not None) and (userCurrentTeam.idPokemon2 != None) and (userCurrentTeam.idPokemon3 != None) and (userCurrentTeam.idPokemon4 != None) and (userCurrentTeam.idPokemon5 != None)):
                return redirect('dashboard')
        return redirect('index')
    else:
        return redirect('login')


# Retirer un pokemon dans l'équipe d'un utilisateur
def removePokemonInCurrentTeam(request):
    if request.user.is_authenticated:
        if (request.POST.get('idPokemon')):
            idPokemon = request.POST['idPokemon']
            userInfo = UserInfo.objects.get(user=request.user)
            userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
            if (idPokemon == "1"):
                userCurrentTeam.idPokemon1 = None
                userCurrentTeam.save()
            elif (idPokemon == "2"):
                userCurrentTeam.idPokemon2 = None
                userCurrentTeam.save()
            elif (idPokemon == "3"):
                userCurrentTeam.idPokemon3 = None
                userCurrentTeam.save()
            elif (idPokemon == "4"):
                userCurrentTeam.idPokemon4 = None
                userCurrentTeam.save()
            elif (idPokemon == "5"):
                userCurrentTeam.idPokemon5 = None
                userCurrentTeam.save()
        return redirect('dashboard')
    else:
        return redirect('login')


# Publier une équipe
def createTeam(request):
    if request.user.is_authenticated:
        userInfo = UserInfo.objects.get(user=request.user)
        userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
        if ((userCurrentTeam.title is not None) and (userCurrentTeam.idPokemon1 is not None) and (userCurrentTeam.idPokemon2 is not None) and (userCurrentTeam.idPokemon3 is not None) and (userCurrentTeam.idPokemon4 is not None) and (userCurrentTeam.idPokemon5 is not None)):
            userCurrentTeam.publish = True
            userCurrentTeam.save()
            poketeam = PokeTeam.objects.create(user=request.user, publish=False)
            poketeam.save()
            userInfo.currentTeam = poketeam.id
            userInfo.save()
        return redirect('dashboard')
    else:
        return redirect('login')


# Supprimer une équipe
def removeTeam(request):
    if request.user.is_authenticated:
        if (request.POST.get('id')):
            team = PokeTeam.objects.get(id=request.POST['id'], user=request.user).delete()
        return redirect('dashboard')
    else:
        return redirect('login')


# Affiche toutes les équipes publier
def pokemonTeamView(request):
    teams = PokeTeam.objects.all().exclude(publish=False).order_by('-id')
    full_team = []

    for team in teams:
        newTeam = {
            'author': team.user,
            'title': team.title,
            'pokemon1': getPokemonInDB(team.idPokemon1),
            'pokemon2': getPokemonInDB(team.idPokemon2),
            'pokemon3': getPokemonInDB(team.idPokemon3),
            'pokemon4': getPokemonInDB(team.idPokemon4),
            'pokemon5': getPokemonInDB(team.idPokemon5),
        }
        full_team.append(newTeam)

    context = {'user': request.user.is_authenticated, 'team_list': full_team}
    return render(request, 'pokedex/pokemonTeam.html', context)

# Compte utilisateur


# Register d'un utilisateur
def RegisterView(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if (request.POST.get('username') and request.POST.get('password') and request.POST.get('email')):
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            poketeam = PokeTeam.objects.create(user=user, publish=False)
            poketeam.save()
            userinfo = UserInfo.objects.create(user=user, currentTeam=poketeam.id)
            userinfo.save()
            return redirect("login")
        else:
            return render(request, 'pokedex/account/register.html')


# Login utilisateur
def LoginView(request):
    if (request.user.is_authenticated):
        return redirect("index")
    else:
        if (request.POST.get('username') and request.POST.get('password')):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                context = {'errors': 'User Not Found'}
                return render(request, 'pokedex/account/login.html', context)
        else:
            return render(request, 'pokedex/account/login.html')


# Déconnexion
def LogoutView(request):
    logout(request)
    return redirect("index")


# Dashboard utilisateur 
def dashboardView(request):
    if request.user.is_authenticated:
        userInfo = UserInfo.objects.get(user=request.user)
        currentTeam = PokeTeam.objects.filter(id=userInfo.currentTeam)
        current_team = []
        for team in currentTeam:
            newTeam = {
                'author': team.user,
                'title': team.title,
                'pokemon1': getPokemonInDB(team.idPokemon1),
                'pokemon2': getPokemonInDB(team.idPokemon2),
                'pokemon3': getPokemonInDB(team.idPokemon3),
                'pokemon4': getPokemonInDB(team.idPokemon4),
                'pokemon5': getPokemonInDB(team.idPokemon5),
            }
            current_team.append(newTeam)

        teams = PokeTeam.objects.filter(user=request.user).exclude(publish=False).order_by('-id')
        full_team = []
        for team in teams:
            newTeam = {
                'id': team.id,
                'author': team.user,
                'title': team.title,
                'pokemon1': getPokemonInDB(team.idPokemon1),
                'pokemon2': getPokemonInDB(team.idPokemon2),
                'pokemon3': getPokemonInDB(team.idPokemon3),
                'pokemon4': getPokemonInDB(team.idPokemon4),
                'pokemon5': getPokemonInDB(team.idPokemon5),
            }
            full_team.append(newTeam)

        context = {
            'current_team': current_team,
            'team_list': full_team,
        }
        return render(request, 'pokedex/account/dashboard.html', context)
    else:
        return redirect("login")

# Pokemon BDD


# Ajout pokémon dans BDD s'il existe pas (par rapport a son id)
def addPokemonInDB(id):
    exist = list(Pokemon.objects.filter(idPokemon=id))
    if (len(exist) == 0):
        api = f'{url}{id}'
        r = requests.get(api)
        results = r.json()
        pokemon = Pokemon.objects.create(idPokemon=results["id"], name=results["name"], img=results["sprites"]["other"]["home"]["front_default"], type=results["types"][0]["type"]["name"], color=colors[results["types"][0]["type"]["name"]], backgroundColor=backgroundColors[results["types"][0]["type"]["name"]])
        pokemon.save()


def getPokemonInDB(id):
    exist = list(Pokemon.objects.filter(idPokemon=id))
    if (len(exist) != 0):
        return Pokemon.objects.filter(idPokemon=id)
    return None
