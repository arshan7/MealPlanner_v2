from django.db import models
from django.shortcuts import reverse
from datetime import datetime
from RecipeBook.models import DishItems
from django.db.models.signals import pre_save
from django.forms.models import model_to_dict


# Create your models here.
# meal plans


class FoodGroup(models.Model):
    title = models.CharField(max_length=1024, blank=False, null=False, )
    food_items = models.ManyToManyField(DishItems, related_name='FoodGroup', blank=True)
    food_day = models.ForeignKey('Days', related_name='FoodGroup', blank=True, null=True, on_delete=models.CASCADE)
    preset = models.ForeignKey("Preset", related_name="preset", blank=True, null=True, on_delete=models.DO_NOTHING)
    order = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['time', 'order', 'preset']

    def save(self, *args, **kwargs):
        old, dont_execute, insert, swap = get_initial_conditions_for_food_group_and_preset(self, FoodGroup, *args,
                                                                                           **kwargs)

        if self.food_day is not None and dont_execute:
            filter_args = {"food_day_id": self.food_day.id,
                           "order": self.order}
            exclude_args = {"id": self.id}
            change_order_on_model_if_same_order_is_preset(self, old, FoodGroup, insert, swap, ["time", "order"],
                                                          filter_args, exclude_args)

        super(FoodGroup, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.food_day.title if self.food_day else ''}"


class Days(models.Model):
    title = models.CharField(max_length=256)
    preset = models.ForeignKey("MealPreset", on_delete=models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return f"{self.title} {'-'.join([fg.title for fg in self.FoodGroup.all()])}"


class MealPlans(models.Model):
    DAYS = [('MONDAY', 'MONDAY'), ('TUESDAY', 'TUESDAY'), ('WEDNESDAY', 'WEDNESDAY'),
            ('THURSDAY', 'THURSDAY'), ('FRIDAY', 'FRIDAY'), ('SATURDAY', 'SATURDAY'),
            ('SUNDAY', 'SUNDAY')]

    plan_name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    monday = models.ForeignKey('Days', on_delete=models.CASCADE,
                               related_name='mondayGroup', blank=True,
                               null=True)
    tuesday = models.ForeignKey('Days', on_delete=models.CASCADE,
                                related_name='tuesdayGroup', blank=True,
                                null=True)
    wednesday = models.ForeignKey('Days', on_delete=models.CASCADE,
                                  related_name='wednesdayGroup', blank=True,
                                  null=True)
    thursday = models.ForeignKey('Days', on_delete=models.CASCADE,
                                 related_name='thursdayGroup', blank=True,
                                 null=True)
    friday = models.ForeignKey('Days', on_delete=models.CASCADE,
                               related_name='fridayGroup', blank=True,
                               null=True)
    saturday = models.ForeignKey('Days', on_delete=models.CASCADE,
                                 related_name='saturdayGroup', blank=True,
                                 null=True)
    sunday = models.ForeignKey('Days', on_delete=models.CASCADE,
                               related_name='sundayGroup', blank=True,
                               null=True
                               )
    default_day = models.CharField(choices=DAYS, max_length=10)

    def __str__(self):
        return self.plan_name

    def get_absolute_url(self):
        return reverse("MealPlans:get_meal_plan_single", kwargs={'plan_name': self.plan_name})


class Preset(models.Model):
    name = models.CharField(max_length=69, blank=False, null=False)
    presets = models.ForeignKey("MealPreset", on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['time', 'order', 'presets']

    def save(self, *args, **kwargs):
        # dont_execute = kwargs.pop('dont_execute') if 'dont_execute' in kwargs else False
        # change_order_swap = kwargs.pop('swap') if 'swap' in kwargs else True
        # old = Preset.objects.filter(id=getattr(self, "id", None)).first()
        # if old is not None:
        #     changed_data = get_changed_data(old, self)
        # else:
        #     changed_data = {}
        #
        # insert = True if 'presets' in changed_data or 'time' in changed_data or self._state.adding else False
        # swap = True if 'order' in changed_data and 'presets' not in changed_data and 'time' not in changed_data and change_order_swap else False

        old, dont_execute, insert, swap = get_initial_conditions_for_food_group_and_preset(self, Preset, *args,
                                                                                           **kwargs)

        if self.presets is not None and not dont_execute:
            # if old and old.presets:
            #     preset_changed = True if old.presets.id != self.presets.id else False
            # else:
            #     preset_changed = True if self.presets is not None else False
            # if old and old.order:
            #     order_changed = True if old.order != self.order else False
            # else:
            #     order_changed = True if self.order else False

            filter_args = {"presets_id": self.presets.id,
                           "order": self.order}
            exclude_args = {"id": self.id}

            change_order_on_model_if_same_order_is_preset(self, old, Preset, insert, swap,
                                                          ["time", "order"],
                                                          filter_args, exclude_args)
        if 'swap' in kwargs:
            kwargs.pop('swap')

        if 'dont_execute' in kwargs:
            kwargs.pop('dont_execute')

        super(Preset, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.presets.name if self.presets else ''}"


class MealPreset(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False, unique=True)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.id} status {self.active}"


def change_order_on_model_if_same_order_is_preset(self, old, model, insert, swap, properties_to_change,
                                                  filter_args,
                                                  exclude_args):
    results = model.objects.filter(**filter_args).exclude(**exclude_args)
    matched_instance = results[0] if results else None

    if insert:
        closest_preset, is_before_equal = find_closed_preset(
            self.presets.preset_set.all().exclude(id=self.id).order_by("order"),
            self, {})
        if closest_preset:
            if is_before_equal:
                self.order = closest_preset.order
            else:
                self.order = closest_preset.order + 1
            filter_args['order'] = self.order
            change_order_on_model_if_same_order_is_preset(self, old, model,
                                                          False, False, properties_to_change, filter_args, exclude_args)
    elif matched_instance and swap:
        for attribute in properties_to_change:
            att1 = getattr(old, attribute)
            att2 = getattr(matched_instance, attribute)
            setattr(self, attribute, att2)
            setattr(matched_instance, attribute, att1)
        matched_instance.save(dont_execute=True)
    elif matched_instance:
        matched_instance.order += 1
        matched_instance.save(swap=False)
    else:
        print("invalid options case arised try to solve it")




def get_changed_data(old, new):
    # use Preset._meta.get_fields(include_parents=False) if you want all fields
    old_dict = model_to_dict(old)
    new_dict = model_to_dict(new)
    changed_dict = {}
    if old.__class__.__name__ == new.__class__.__name__:
        for key in model_to_dict(old).keys():
            if old_dict.get(key) != new_dict.get(key):
                changed_dict[key] = {'old': old_dict.get(key), 'new': new_dict.get(key)}
    return changed_dict


def find_closed_preset(find_in_list, current_preset, existed_dict):
    closest = 24 * 60 * 60
    closest_item = None
    is_before_equal = None
    for item in find_in_list:
        if item not in existed_dict:
            preset_date = datetime.combine(datetime.today(), item.time)
            current_date = datetime.combine(datetime.today(), current_preset.time)
            if preset_date >= current_date:
                time_difference = preset_date - current_date
            else:
                time_difference = current_date - preset_date

            if time_difference.seconds <= closest:
                closest = time_difference.seconds
                closest_item = item
                is_before_equal = current_date <= preset_date
    return closest_item, is_before_equal


def get_initial_conditions_for_food_group_and_preset(self, Model, *args, **kwargs):
    dont_execute = kwargs.pop('dont_execute') if 'dont_execute' in kwargs else False
    change_order_swap = kwargs.pop('swap') if 'swap' in kwargs else True

    old = Model.objects.filter(id=getattr(self, "id", None)).first()
    if old is not None:
        changed_data = get_changed_data(old, self)
    else:
        changed_data = {}

    insert = True if 'presets' in changed_data or 'time' in changed_data or self._state.adding else False
    swap = True if 'order' in changed_data and 'presets' not in changed_data and 'time' not in changed_data and change_order_swap else False
    return old, dont_execute, insert, swap,


def detect_changes_in_preset_update_food_groups(sender, instance, **kwargs):
    old = Preset.objects.filter(id=getattr(instance, "id", None)).first()
    if old is not None:
        changed_data = get_changed_data(old, instance)
    else:
        changed_data = {}

    if len(changed_data) > 0:
        update_params = {}
        all_food_groups = FoodGroup.objects.filter(preset=instance)
        for changed_attributes in changed_data.keys():
            update_params[changed_attributes] = changed_data[changed_attributes]['new']
        all_food_groups.update(**update_params)


pre_save.connect(detect_changes_in_preset_update_food_groups, sender=Preset)
