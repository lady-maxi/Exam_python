from django.contrib import admin
from .models import Ingredient, Recette

@admin.register(Recette)
class RecetteAdmin(admin.ModelAdmin):
    filter_horizontal = ('ingredients',)

admin.site.register(Ingredient)