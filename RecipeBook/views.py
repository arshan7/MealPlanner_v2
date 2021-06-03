from django.shortcuts import render, get_object_or_404
from .forms import (CreateIngredientForm, UpdateIngredientForm, DeleteIngredientForm,
                    CreateDishForm, UpdateDishForm, DeleteDishForm)
from .models import Ingredients, Dish

import traceback

# Create your views here.


def create_ingredient(request):
    context = {
        "form": CreateIngredientForm()
    }

    if request.method == "POST":
        form = CreateIngredientForm(request.POST)
        if form.is_valid():
            form.save()
            print("ok")
        else:
            context['form'] = form
    else:
        print("not post")
    return render(request, "RecipeBook/Ingredient/create_ingredient.html", context=context)


def update_ingredient(request, name=None):
    instance = None
    if name is not None:
        try:
            instance = Ingredients.objects.get(name=name)
        except Ingredients.DoesNotExist:
            print("not found")

    else:
        print("name is none")
    context = {
        "form": UpdateIngredientForm(instance=instance),
        "model": instance,
    }

    if request.method == "POST":
        form = UpdateIngredientForm(request.POST or None,
                                    instance=get_object_or_404(Ingredients, name=request.POST.get("name", None)))
        if form.is_valid():
            form.save()

    return render(request, "RecipeBook/Ingredient/update_ingredient.html", context=context)


def delete_ingredient(request):
    context = {
        'form': DeleteIngredientForm(),
    }

    if request.method == "POST":
        form = DeleteIngredientForm(request.POST or None,
                                    instance=get_object_or_404(Ingredients, name=request.POST.get("name", None)))
        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                Ingredients.objects.get(name=name).delete()
            except(Ingredients.DoesNotExist, Exception) as e:
                print(e)
        else:
            print(form.errors)
    return render(request, "RecipeBook/Ingredient/delete_ingredient.html", context=context)


def get_ingredient(request):
    pass


# Dishes


def create_dish(request):
    context = {
        "form": CreateDishForm()
    }

    if request.method == "POST":
        form = CreateDishForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context['form'] = form

    return render(request, "RecipeBook/Dish/create_dish.html", context=context)


def update_dish(request, name=None):
    context = {
        "form": UpdateDishForm()
    }

    if name is not None:
        form = UpdateDishForm(instance=Dish.objects.get(name=name))
        context['form'] = form

    if request.method == "POST":
        form = UpdateDishForm(request.POST or None,
                              instance=get_object_or_404(Dish, name=request.POST.get("name", None)))

        if form.is_valid():
            form.save()
        else:
            context['form'] = form

    return render(request, "RecipeBook/Dish/update_dish.html", context)


def delete_dish(request):
    context = {
        "form": DeleteDishForm(),
    }

    if request.method == "POST":
        try:
            form = DeleteDishForm(request.POST or None,
                                  instance=Dish.objects.get(name=request.POST.get("name", None)))

            if form.is_valid():
                Dish.objects.get(name=form.cleaned_data["name"]).delete()
            else:
                context["form"] = form
        except (Dish.DoesNotExist, Exception) as e:
            print(e)
            traceback.print_exc()

    return render(request, "RecipeBook/Dish/delete_dish.html", context)


def get_dish(request):
    pass
