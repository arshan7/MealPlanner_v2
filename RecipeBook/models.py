from django.db import models
from django.shortcuts import reverse

# Create your models here.
from polymorphic.models import PolymorphicModel


class DishItems(PolymorphicModel):
    name = models.CharField(max_length=256, null=False, blank=False,
                            primary_key=True, validators=[])


class Dish(DishItems):
    picture = models.ImageField(blank=False, null=False)
    category_choices = (('Veg', 'Veg'), ('NonVeg', 'NonVeg'))
    category = models.CharField(max_length=60, choices=category_choices,
                                null=False, blank=False)
    total_Rating = models.IntegerField(default=0, null=False,
                                       blank=False)

    def __str__(self):
        return self.name


class Ingredients(DishItems):
    picture = models.ImageField(blank=False, null=False)

    category_choices = (('Veg', 'Veg'), ('NonVeg', 'NonVeg'))
    category = models.CharField(max_length=60, choices=category_choices, blank=False,
                                null=False)
    amount_choices = (('gms', 'gms'), ('oneserv', 'oneserv'), ('ml', 'ml'))
    amount_type = models.CharField(max_length=60, blank=False, null=False,
                                   choices=amount_choices)

    def __str__(self):
        return self.name

    def get_update_meal_plan_url(self):
        return reverse("RecipeBook:update_ingredient_single", kwargs={
            "name": self.name
        })


class DishIngredients(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE,
                             related_name="dName", blank=False, null=False)
    dishItems = models.ManyToManyField('DishItems',
                                       related_name='dishIngredients', blank=False)

    def __str__(self):
        return self.dish.name
