from django import forms
from .models import Ingredients, Dish


class CreateIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ["picture", "name", "category", "amount_type"]

    picture = forms.ImageField(required=False)


class UpdateIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ["picture", "name", "category", "amount_type"]

    name = forms.ModelChoiceField(queryset=Ingredients.objects.all())
    picture = forms.ImageField(required=False)


class DeleteIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = ['name']

    name = forms.ModelChoiceField(queryset=Ingredients.objects.all())

#
# class GetIngredientForm(forms.ModelForm):
#     class Meta:
#         model = Ingredients


# Dish code

class CreateDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"

    picture = forms.ImageField(required=False)


class UpdateDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"

    picture = forms.ImageField(required=False)

    name = forms.ModelChoiceField(queryset=Dish.objects.all())


class DeleteDishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name']

    name = forms.ModelChoiceField(queryset=Dish.objects.all())