from django.contrib import admin
from .models import DishItems, Dish, DishIngredients, Ingredients

# Register your models here.


admin.site.register(Dish)
admin.site.register(DishIngredients)
admin.site.register(Ingredients)
admin.site.register(DishItems)
