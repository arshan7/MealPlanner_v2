from django.urls import path, include

from .views import (
    meal_plan_home,
    create_meal_plan, update_meal_plan, ajax_load_meal_plans_based_on_day, delete_meal_plan, get_meal_plan,
    create_food_group, update_food_group, delete_food_group,
    create_day, update_day, delete_day, ajax_load_change_preset,
    ajax_load_order_from_preset_objects, ajax_load_load_default_order_for_food_group_based_on_preset,
    add_dishes_products_to_meal, ajax_load_items_or_more, ajax_save_items_to_food_group, ajax_save_default_day,
)

app_name = 'MealPlans'

urlpatterns = [

    path('', meal_plan_home, name="meal_plan_home"),
    path('plans/', get_meal_plan, name="get_meal_plan"),
    path('plans/<plan_name>', get_meal_plan, name="get_meal_plan_single"),
    path('create', create_meal_plan, name="create_meal_plan"),

    path('update/', update_meal_plan, name="update_meal_plan_all"),
    path('update/<plan_name>', update_meal_plan, name="update_meal_plan"),
    path('update/ajax/loadmealsbasedonday', ajax_load_meal_plans_based_on_day, name="ajax_load_meals_based_on_day"),
    path('delete', delete_meal_plan, name="delete_meal_plan"),
    path("foodgroups/create", create_food_group, name="create_food_group"),
    path("foodgroups/update/", update_food_group, name="update_food_group"),
    path("foodgroups/update/<int:fg_id>", update_food_group, name="update_food_group_single"),
    path("foodgroups/delete/", delete_food_group, name="delete_food_group"),
    path("ajax/load/ajax_load_order_from_preset_objects/", ajax_load_order_from_preset_objects,
         name="ajax_load_order_id"),
    path("ajax/load/foodgroups/oder", ajax_load_load_default_order_for_food_group_based_on_preset,
         name="ajax_load_foodgroups_order"),

    path("day/create", create_day, name="create_day"),
    path("day/update/", update_day, name="update_day"),
    path("day/update/<int:day_id>", update_day, name="update_day_single"),
    path("day/delete", delete_day, name="delete_day"),
    path("day/load_change_preset", ajax_load_change_preset, name="ajax_load_change_preset"),
    path("days/delete", delete_day, name="delete_day"),

    path("add/dishorproduct/", add_dishes_products_to_meal, name="add_dish_product_to_plan"),
    path("ajax/load_more_products", ajax_load_items_or_more, name="ajax_load_more_products"),
    path("ajax/save_items_to_food_group", ajax_save_items_to_food_group, name="ajax_save_item_to_food_group"),
    path("ajax/save_default_day", ajax_save_default_day, name="ajax_save_default_day"),
]
