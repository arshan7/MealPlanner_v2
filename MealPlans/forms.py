from django import forms

from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

from .mealPlanWidgets import AutoComplete

from .models import MealPlans, Days, FoodGroup, DishItems, Preset


class MealPlannerAutoComplete(AutocompleteSelect):

    def __init__(self, field):
        super(MealPlannerAutoComplete, self).__init__(field, admin.site)


class CreateMealPlanForm(forms.Form):
    plan_name = forms.CharField(max_length=256)


class UpdateMealPlanForm(forms.ModelForm):
    UpdateMealPlanForm_attrs = {"class": "UpdateMealPlan_Select"}

    def __init__(self, *args, **kwargs):
        super(UpdateMealPlanForm, self).__init__(*args, **kwargs)
        UpdateMealPlanForm.update_meal_plans_set_attrs(self.fields.values(), self.UpdateMealPlanForm_attrs)

    @staticmethod
    def update_meal_plans_set_attrs(fields, attrs):
        for attr_name, attr_value in attrs.items():
            for field in fields:
                field.widget.attrs[attr_name] = attr_value

    class Meta:
        model = MealPlans
        fields = ['plan_name', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    plan_name = forms.ModelChoiceField(widget=forms.Select, queryset=MealPlans.objects.all(),
                                       to_field_name="plan_name")


class DeleteMealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlans
        fields = ["plan_name"]

    plan_name = forms.ModelChoiceField(widget=forms.Select, queryset=MealPlans.objects.all())


# Food groups

class CreateFoodGroupsForm(forms.ModelForm):
    class Meta:
        model = FoodGroup
        fields = ["title"]

    food_items = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple, queryset=DishItems.objects.all(),
                                                error_messages={'invalid_pk_value': '%(pk)s is not a primary key '})


class UpdateFoodGroupsForm(forms.ModelForm):
    class Meta:
        model = FoodGroup
        fields = "__all__"

    title = forms.ModelChoiceField(queryset=FoodGroup.objects.all(), to_field_name="id")


class DeleteFoodGroupsForm(forms.ModelForm):
    class Meta:
        model = FoodGroup
        fields = ["title"]

    title = forms.ModelChoiceField(queryset=FoodGroup.objects.all())


class CreateDaysForm(forms.ModelForm):
    class Meta:
        model = Days
        fields = "__all__"


class UpdateDaysForm(forms.ModelForm):
    all_days = forms.ModelChoiceField(queryset=Days.objects.all(), to_field_name="id", required=False)

    class Meta:
        model = Days
        fields = ["all_days", "title", "preset"]


class DeleteDaysForm(forms.ModelForm):
    class Meta:
        model = FoodGroup
        fields = ["title"]

    title = forms.ModelChoiceField(queryset=Days.objects.all())


class PresetDynamicFieldsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        meal_preset_id = kwargs.pop('meal_preset_id')
        matching_dict = kwargs.pop('matching_dict')
        order_list = kwargs.pop('order_list')
        super(PresetDynamicFieldsForm, self).__init__(*args, **kwargs)

        for item in order_list:
            preset = matching_dict[item] if item in matching_dict else None
            self.fields[item.title] = forms.ModelChoiceField(
                queryset=Preset.objects.filter(presets_id=meal_preset_id),
                initial=preset.id if preset else None,
                to_field_name="id",
                required=True if preset else False
            )


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False)
