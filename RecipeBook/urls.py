from django.urls import path
from .views import (create_ingredient, update_ingredient, delete_ingredient,
                    create_dish, update_dish, delete_dish)

app_name = "RecipeBook"

urlpatterns = [

    path("create", create_ingredient, name="create_ingredient"),
    path("update/", update_ingredient, name="update_ingredient"),
    path("update/<name>", update_ingredient, name="update_ingredient_single"),
    path("delete", delete_ingredient, name="delete_ingredient"),
    path("dish/create/", create_dish, name="create_dish"),
    path("dish/update/", update_dish, name="update_dish"),
    path("dish/update/<name>", update_dish, name="update_dish_single"),
    path("dish/delete", delete_dish, name="delete_dish")

]
