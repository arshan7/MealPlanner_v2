from .models import FoodGroup, MealPreset


def create_day_initialize(day_instance):
    if day_instance.preset:
        meal_preset = day_instance.preset
    else:
        meal_preset = MealPreset.objects.get(default=True)
    for preset in meal_preset.preset_set.all():
        food_group = FoodGroup.objects.create(title=preset.name,
                                              food_day=day_instance, preset=preset,
                                              order=preset.order,
                                              time=preset.time)
        food_group.save()
    return day_instance.FoodGroup.all()


def copy_food_items(source, destination, reverse):
    print(source, destination, reverse, "ok test")
    if source is not None and destination is not None:

        if not reverse:
            for destination_id in destination:
                FoodGroup.objects.get(id=source).food_items.add(*FoodGroup.objects.get(id=destination_id).food_items.all())
        else:
            for destination in destination:
                FoodGroup.objects.get(id=destination).food_items.add(*FoodGroup.objects.get(id=source).food_items.all())
    else:
        pass
