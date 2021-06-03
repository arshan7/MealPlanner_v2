from django.contrib import admin
from .models import FoodGroup, Days, MealPlans, DishItems, MealPreset, Preset
from django import forms
from django.db import models
from django.shortcuts import reverse
from .mealPlanWidgets import TimeWidget


class MultipleSelectChangeValue(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "food_items":
            kwargs['queryset'] = DishItems.objects.all()
            kwargs['to_field_name'] = "id"
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class PresetModelAdmin(admin.ModelAdmin):

    list_filter = ("presets",)
    formfield_overrides = {
        models.ForeignKey: {
            'widget': forms.Select(
                attrs={'data-ajax_url': "MealPlans/ajax/load/ajax_load_order_from_preset_objects/"})},
        models.TimeField: {'widget': TimeWidget}

    }


class FoodGroupModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {'widget': TimeWidget}
    }
    list_filter = ("food_day", "preset")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "preset":
            form_field = super(FoodGroupModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
            form_field.widget.attrs['data-ajax_url'] = reverse("MealPlans:ajax_load_foodgroups_order")
            return form_field
        return super(FoodGroupModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(FoodGroup, FoodGroupModelAdmin)
admin.site.register(Days)
admin.site.register(MealPlans)
admin.site.register(MealPreset)
admin.site.register(Preset, PresetModelAdmin)
