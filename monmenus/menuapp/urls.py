from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('frigo/', views.frigo, name='frigo'),
    path('ajouter-ingredient/', views.ajouter_ingredient, name='ajouter_ingredient'),
    path('ajouter-ingredient_placard/', views.ajouter_ingredient_placard, name='ajouter_ingredient_placard'),
    path('generer-menu/', views.generer_menu, name='generer_menu'),
    path('export-pdf/<int:recette_id>/', views.export_pdf, name='export_pdf'),
    path('modifier-ingredient/<int:id>/', views.modifier_ingredient, name='modifier_ingredient'),
    path('supprimer-ingredient/<int:id>/', views.supprimer_ingredient, name='supprimer_ingredient'),
    path('placard/', views.placard, name='placard'),
    path('confirmer-recette/<int:recette_id>/', views.confirmer_recette, name='confirmer_recette'),
    path('valider-recette/<int:recette_id>/', views.valider_recette, name='valider_recette'),
    path('recettes/', views.recettes, name='recettes'),
    path('recette/<int:recette_id>/', views.detail_recette, name='detail_recette'),
    path('modifier-ingredient_placard/<int:id>/', views.modifier_ingredient_placard, name='modifier_ingredient_placard'),
    path('supprimer-ingredient_placard/<int:id>/', views.supprimer_ingredient_placard, name='supprimer_ingredient_placard'),
    path('historique/', views.historique, name='historique'),
    
    ]