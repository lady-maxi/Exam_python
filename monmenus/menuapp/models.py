from django.db import models

# Create your models here.
class Ingredient(models.Model):
    CATEGORIES_CHOICES = [
    ('Légumes frais', 'Légumes frais'),
    ('Fruits frais', 'Fruits frais'),
    ('Viandes', 'Viandes'),
    ('Poissons', 'Poissons'),
    ('Produits laitiers', 'Produits laitiers'),
    ('Œufs', 'Œufs'),
    ('Charcuterie', 'Charcuterie'),
    ('Plats cuisinés', 'Plats cuisinés'),
    ('Pâtes', 'Pâtes'),
    ('Riz', 'Riz'),
    ('Légumineuses', 'Légumineuses'),
    ('Conserves', 'Conserves'),
    ('Épices', 'Épices'),
    ('Céréales', 'Céréales'),
    ('Biscuits & Snacks', 'Biscuits & Snacks'),
    ('Huiles & Vinaigres', 'Huiles & Vinaigres'),
    ('Farine & Sucre', 'Farine & Sucre'),
    ('Autre', 'Autre'),
]
    LIEU_CHOICES = [
        ('Frigo', 'Frigo'),
        ('Placard', 'Placard'),
    ]
    nom = models.CharField(max_length=100)
    quantite = models.FloatField()
    unite = models.CharField(max_length=50, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, blank=True)
    lieu = models.CharField(max_length=50, choices=LIEU_CHOICES, default='Frigo')

    def __str__(self):
        return self.nom

class Recette(models.Model):
    nom = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)
    cout_estime = models.FloatField()
    temps_preparation = models.IntegerField()  # En minutes
    instructions = models.TextField()
    image = models.ImageField(upload_to='recettes/', blank=True, null=True)

    def __str__(self):
        return self.nom
    

class Historique(models.Model):
    recette = models.ForeignKey('Recette', on_delete=models.CASCADE)
    date_validation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recette.nom} — {self.date_validation.strftime('%d/%m/%Y %H:%M')}"
    


class Favori(models.Model):
    recette = models.ForeignKey('Recette', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recette.nom} — {self.date_ajout.strftime('%d/%m/%Y %H:%M')}"