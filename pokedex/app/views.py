from django.shortcuts import render
import requests
from django.shortcuts import redirect

# Import des models
from .models import PokeTeam
from .models import UserInfo

# Import pour compte utilisateur
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



# Create your views here.
url = "https://pokeapi.co/api/v2"


def index(request):
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

    if(request.GET.get('search')):

        url = "https://pokeapi.co/api/v2/pokemon/" + request.GET['search']
        pokemonArray = []
        for i in range(1, 2):
            if(getPokemonById(request.GET['search']) != None):
                pokemonArray.append(getPokemonById(request.GET['search']))
            i += 1

        if(len(pokemonArray) > 0):
            for pokemon in pokemonArray:
                pokemon["backgroundColor"] = backgroundColors[pokemon["types"][0]["type"]["name"]]
                pokemon["color"] = colors[pokemon["types"][0]["type"]["name"]]

        
        return render(request, "pokedex/index.html", {'pokemons': pokemonArray})

    else:
        
        pokemonArray = []
        for i in range(1, 11):
            pokemonArray.append(getPokemonById(i))
            i += 1

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








# Gestion des équipes

# Modifier le titre de l'équipe actuelle
def updateTeamTitle(request):
    if request.user.is_authenticated:
        if(request.POST.get('title')):
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
        if(request.POST.get('id')):
            userInfo = UserInfo.objects.get(user=request.user)
            userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
            if(userCurrentTeam.idPokemon1 == None):
                userCurrentTeam.idPokemon1 = request.POST.get('id')
                userCurrentTeam.save()
            elif(userCurrentTeam.idPokemon2 == None):
                userCurrentTeam.idPokemon2 = request.POST.get('id')
                userCurrentTeam.save()
            elif(userCurrentTeam.idPokemon3 == None):
                userCurrentTeam.idPokemon3 = request.POST.get('id')
                userCurrentTeam.save()
            elif(userCurrentTeam.idPokemon4 == None):
                userCurrentTeam.idPokemon4 = request.POST.get('id')
                userCurrentTeam.save()
            elif(userCurrentTeam.idPokemon5 == None):
                userCurrentTeam.idPokemon5 = request.POST.get('id')
                userCurrentTeam.save()
            if((userCurrentTeam.idPokemon1 != None) and (userCurrentTeam.idPokemon2 != None) and (userCurrentTeam.idPokemon3 != None) and (userCurrentTeam.idPokemon4 != None) and (userCurrentTeam.idPokemon5 != None)):
                return redirect('dashboard')
            
        return redirect('index')
    else:
        return redirect('login')

# Retirer un pokemon dans l'équipe d'un utilisateur
def removePokemonInCurrentTeam(request):
    if request.user.is_authenticated:
        if(request.POST.get('idPokemon')):
            idPokemon = request.POST['idPokemon']
            userInfo = UserInfo.objects.get(user=request.user)
            userCurrentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
            if(idPokemon == "1"):
                userCurrentTeam.idPokemon1 = None
                userCurrentTeam.save()
            elif(idPokemon == "2"):
                userCurrentTeam.idPokemon2 = None
                userCurrentTeam.save()
            elif(idPokemon == "3"):
                userCurrentTeam.idPokemon3 = None
                userCurrentTeam.save()
            elif(idPokemon == "4"):
                userCurrentTeam.idPokemon4 = None
                userCurrentTeam.save()
            elif(idPokemon == "5"):
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
        if((userCurrentTeam.title != None) and (userCurrentTeam.idPokemon1 != None) and (userCurrentTeam.idPokemon2 != None) and (userCurrentTeam.idPokemon3 != None) and (userCurrentTeam.idPokemon4 != None) and (userCurrentTeam.idPokemon5 != None)):
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
        if(request.POST.get('id')):
            team = PokeTeam.objects.get(id=request.POST['id'], user=request.user).delete()
        return redirect('dashboard')
    else:
        return redirect('login')

# Affiche toutes les équipes publier
def pokemonTeamView(request):
    team_list = PokeTeam.objects.all().exclude(publish=False)
    full_team = []
    for team in team_list:
         full_team.append(team) 

    context = {
        'team_list' : full_team
    }
    return render(request, 'pokedex/pokemonTeam.html', context)



# Compte utilisateur

# Register d'un utilisateur
def RegisterView(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if(request.POST.get('username') and request.POST.get('password') and request.POST.get('email')):
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
    if request.user.is_authenticated:
        return redirect("dashboard")
    else: 
        if(request.POST.get('username') and request.POST.get('password')):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                context = { 'errors' : 'User Not Found' }
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
        currentTeam = PokeTeam.objects.get(id=userInfo.currentTeam)
        fullTeam = PokeTeam.objects.all().filter(user=request.user).exclude(publish=False)
        context = { 
            'currentTeam' : currentTeam,
            'fullTeam' : fullTeam 
        }
        return render(request, 'pokedex/account/dashboard.html', context)
    else:
        return redirect("login")