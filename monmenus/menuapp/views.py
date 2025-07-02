from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404 
# Create your views here.
from .models import Ingredient, Recette
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Favori
from .models import Historique
import random
import re

def accueil(request):
    total_ingredients = Ingredient.objects.count()
    ingredients_rupture = Ingredient.objects.filter(quantite=0)
    return render(request, 'menuapp/accueil.html', {
        'total_ingredients': total_ingredients,
        'ingredients_rupture': ingredients_rupture
    })
def frigo(request):
    ingredients = Ingredient.objects.filter(lieu="Frigo")
    return render(request, 'menuapp/frigo.html', {'ingredients': ingredients})
def ajouter_ingredient(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        unite = request.POST.get('unite')
        categorie = request.POST.get('categorie')
        lieu = "Frigo" 
        Ingredient.objects.create(
            nom=nom, 
            quantite=quantite, 
            unite=unite,
            categorie=categorie,
            lieu=lieu)
        return redirect('frigo')
    return render(request, 'menuapp/ajouter_ingredient.html')
def generer_menu(request):
    recettes = Recette.objects.all()
    recette = random.choice(recettes) if recettes else None
    return render(request, 'menuapp/generer_menu.html', {'recette': recette})

def export_pdf(request, recette_id):
    recette = Recette.objects.get(id=recette_id)
    template_path = 'menuapp/pdf_template.html'
    context = {'recette': recette}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="menu_{recette.nom}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF')
    return response


def modifier_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if request.method == 'POST':
        ingredient.nom = request.POST.get('nom')
        ingredient.quantite = request.POST.get('quantite')
        ingredient.unite = request.POST.get('unite')
        ingredient.categorie = request.POST.get('categorie')
        ingredient.save()
        return redirect('frigo')
    return render(request, 'menuapp/modifier_ingredient.html', {'ingredient': ingredient})


def modifier_ingredient_placard(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if request.method == 'POST':
        ingredient.nom = request.POST.get('nom')
        ingredient.quantite = request.POST.get('quantite')
        ingredient.unite = request.POST.get('unite')
        ingredient.categorie = request.POST.get('categorie')
        ingredient.save()
        return redirect('placard')
    return render(request, 'menuapp/modifier_ingredient_placard.html', {'ingredient': ingredient})


def supprimer_ingredient(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('frigo')
    return render(request, 'menuapp/supprimer_ingredient.html', {'ingredient': ingredient})

def supprimer_ingredient_placard(request, id):
    ingredient = get_object_or_404(Ingredient, id=id)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('placard')
    return render(request, 'menuapp/supprimer_ingredient_placard.html', {'ingredient': ingredient})


def placard(request):
    ingredients = Ingredient.objects.filter(lieu="Placard")
    return render(request, 'menuapp/placard.html', {'ingredients': ingredients})

def ajouter_ingredient_placard(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        quantite = request.POST.get('quantite')
        unite = request.POST.get('unite')
        categorie = request.POST.get('categorie')
        lieu = "Placard"  
        Ingredient.objects.create(
            nom=nom,
            quantite=quantite,
            unite=unite,
            categorie=categorie,
            lieu=lieu
        )
        return redirect('placard')
    return render(request, 'menuapp/ajouter_ingredient_placard.html')

def valider_recette(request, recette_id):
    recette = Recette.objects.get(id=recette_id)
    ingredients = recette.ingredients.all()

    if request.method == 'POST':
        for ing in ingredients:
            stock_actuel = float(ing.quantite)
            qte_utilisee = float(request.POST.get(f'quantite_{ing.id}', 0))
            ing.quantite = max(stock_actuel - qte_utilisee, 0)
            ing.save()
        # ➜ Sauvegarde dans Historique
        Historique.objects.create(recette=recette)
        return redirect('frigo')  # ou une page de confirmation
    return render(request, 'menuapp/confirmer_recette.html', {'recette': recette, 'ingredients': ingredients})


def confirmer_recette(request, recette_id):
    recette = get_object_or_404(Recette, id=recette_id)
    ingredients = recette.ingredients.all()

    if request.method == 'POST':
        for ing in ingredients:
            stock_actuel = ing.quantite
            qte_utilisee = float(request.POST.get(f'quantite_{ing.id}', 0))
            nouvelle_quantite = max(stock_actuel - qte_utilisee, 0)
            ing.quantite = nouvelle_quantite
            ing.save()
        # ➜ Enregistre l’action dans Historique ✅
        Historique.objects.create(recette=recette)
        return redirect('recettes')

    return render(request, 'menuapp/confirmer_recette.html', {
        'recette': recette,
        'ingredients': ingredients
    })

def recettes(request):
    recettes = Recette.objects.all()
    return render(request, 'menuapp/recettes.html', {'recettes': recettes})


def detail_recette(request, recette_id):
    recette = Recette.objects.get(id=recette_id)
    return render(request, 'menuapp/detail_recette.html', {'recette': recette})

def historique(request):
    historiques = Historique.objects.all().order_by('-date_validation')
    return render(request, 'menuapp/historique.html', {'historiques': historiques})

def ajouter_favori(request, recette_id):
    recette = get_object_or_404(Recette, id=recette_id)
    Favori.objects.create(recette=recette)
    return redirect('mes_favoris')

def mes_favoris(request):
    favoris = Favori.objects.all().order_by('-date_ajout')
    return render(request, 'menuapp/mes_favoris.html', {'favoris': favoris})