import json
import traceback

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import JsonResponse
from django.core import serializers

# from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict
from .forms import (CreateMealPlanForm, UpdateMealPlanForm, DeleteMealPlanForm,
                    CreateFoodGroupsForm, UpdateFoodGroupsForm, DeleteFoodGroupsForm,
                    CreateDaysForm, UpdateDaysForm, DeleteDaysForm,
                    PresetDynamicFieldsForm, SearchForm)

from .models import MealPlans, Days, FoodGroup, Preset, MealPreset, DishItems
from .db_helper import create_day_initialize, copy_food_items
from .models import find_closed_preset


# Create your views here.


def meal_plan_home(request):
    return render(request, 'MealPlans/main_mealplans.html', context={'active': True})


def create_meal_plan(request):
    context = {
        "form": CreateMealPlanForm(),
    }
    if request.method == "POST":
        form = CreateMealPlanForm(request.POST)
        if form.is_valid():
            plan_name = form.cleaned_data['plan_name']
            meal_plan = MealPlans(plan_name=plan_name)
            meal_plan.save()

    return render(request, "MealPlans/MealPlan/create_meal_plan.html", context=context)


# accepts id to get plan name to delete
def delete_meal_plan(request):
    context = {
        "form": DeleteMealPlanForm()
    }
    try:
        if request.method == "POST":
            plan_name = request.POST.get("plan_name") or None
            print(plan_name)
            if plan_name is not None:
                MealPlans.objects.get(id=plan_name).delete()
    except MealPlans.DoesNotExist:
        traceback.print_exc()
    return render(request, "MealPlans/MealPlan/delete_meal_plan.html", context=context)


def update_meal_plan(request, plan_name=None):
    instance = None
    context = {
        "form": UpdateMealPlanForm(),
        "model": instance
    }
    if plan_name is not None:
        instance = MealPlans.objects.get(plan_name=plan_name)

        context = {
            "form": UpdateMealPlanForm(instance=instance, initial={"plan_name": instance.plan_name}),
            "model": instance,
        }

    if request.method == "POST":
        form = UpdateMealPlanForm(request.POST or None,
                                  instance=get_object_or_404(MealPlans, plan_name=request.POST.get("plan_name", None)))
        if form.is_valid():
            form.save()
        else:
            print("NOT VALID ", request.POST)
    return render(request, "MealPlans/MealPlan/update_meal_plan.html", context=context)


def ajax_load_meal_plans_based_on_day(request):
    day = None
    if request.method == "POST":
        data = json.loads(request.body)
        day_name = data["day_name"]
        try:
            day = Days.objects.get(title=day_name)
        except Days.DoesNotExist:
            day = None

    context = {
        "day": day,
    }
    return render(request, "MealPlans/Ajax/load_meals_based_on_day.html", context=context)


def get_meal_plan(request, plan_name=None):
    if plan_name:
        instance = MealPlans.objects.get(plan_name=plan_name)
    else:
        instance = MealPlans.objects.get(plan_name="Test Plan")

    all_instances = MealPlans.objects.all()
    all_attributes = model_to_dict(instance)
    all_attributes.pop('id')
    all_attributes.pop('plan_name')
    all_attributes.pop('default_day')
    days = all_attributes.keys()
    context = {
        'days': days,
        'instance': instance,
        'all_instances': all_instances,
    }
    data = serializers.serialize("json", [instance])
    my_data = request.session.get('instance')
    context['data'] = data
    request.session['instance'] = data

    return render(request, 'MealPlans/main_mealplans.html', context=context)


def create_food_group(request):
    context = {
        "form": CreateFoodGroupsForm()
    }

    if request.method == "POST":
        form = CreateFoodGroupsForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(request, "MealPlans/FoodGroups/create_food_groups.html", context=context)


def update_food_group(request, fg_id=None):
    context = {
        "form": UpdateFoodGroupsForm()
    }

    if fg_id is not None:
        form = UpdateFoodGroupsForm(instance=FoodGroup.objects.get(id=fg_id), initial={"title": fg_id})
        context["form"] = form

    if request.method == "POST":
        form = UpdateFoodGroupsForm(request.POST or None,
                                    instance=get_object_or_404(FoodGroup, title=request.POST.get("title")))

        if form.is_valid():
            form.save()
        else:
            context["form"] = form

    return render(request, "MealPlans/FoodGroups/update_food_groups.html", context=context)


def delete_food_group(request):
    context = {
        "form": DeleteFoodGroupsForm()
    }

    if request.method == "POST":
        form = DeleteFoodGroupsForm(request.POST or None,
                                    instance=FoodGroup.objects.get(title=request.POST.get('title')))
        if form.is_valid():
            FoodGroup.objects.get(title=form.cleaned_data['title']).delete()
        else:
            context["form"] = form

    return render(request, "MealPlans/FoodGroups/delete_food_groups.html", context=context)


def ajax_load_order_from_preset_objects(request):
    total = -1
    if request.method == "POST":
        total = len(Preset.objects.filter(presets_id=int(request.POST.get('val'))))
    return JsonResponse({"total": total + 1})


def ajax_load_load_default_order_for_food_group_based_on_preset(request):
    default_order = 0
    if request.method == "POST":
        default_order = Preset.objects.get(id=int(request.POST.get('val'))).order
    return JsonResponse({"default_order": default_order})


# days

def create_day(request):
    context = {
        "form": CreateDaysForm()
    }

    if request.method == "POST":
        form = CreateDaysForm(request.POST)
        if form.is_valid():
            form.save()
            create_day_initialize(form.instance)
        else:
            context['form'] = form
    return render(request, "MealPlans/Days/create_days.html", context=context)


def update_day(request, day_id=None):
    context = {
        "form": UpdateDaysForm()
    }
    if day_id is not None:
        try:
            instance = Days.objects.get(id=int(day_id))
            context['form'] = UpdateDaysForm(instance=instance, initial={"all_days": day_id})
        except Days.DoesNotExist:
            pass

    if request.method == "POST":
        instance = Days.objects.get(id=request.POST.get("all_days"))
        print(request.POST)
        form = UpdateDaysForm(request.POST or None,
                              instance=instance)
        if form.has_changed():
            if "preset" in form.changed_data and instance:
                already_food_group_list = {}
                already_preset_list = []

                for foodgroup in instance.FoodGroup.all():

                    change_to_preset_id = request.POST.get(foodgroup.title)
                    if change_to_preset_id in already_food_group_list:
                        if foodgroup.food_items.all():
                            already_food_group_list[change_to_preset_id].food_items.add(foodgroup.food_items.all())
                        foodgroup.delete()
                    elif change_to_preset_id:
                        preset = Preset.objects.get(id=change_to_preset_id)
                        already_food_group_list[change_to_preset_id] = foodgroup
                        already_preset_list.append(preset)
                        foodgroup.preset.id = preset.id
                        foodgroup.time = preset.time
                        foodgroup.order = preset.order
                        foodgroup.title = preset.name
                        foodgroup.save()
                    else:
                        foodgroup.delete()
                left_out_presets = set(MealPreset.objects.get(id=request.POST.get('preset')).preset_set.all()) - set(
                    already_preset_list)
                for preset in left_out_presets:
                    food_group = FoodGroup.objects.create(title=preset.name,
                                                          food_day=instance, preset=preset,
                                                          order=preset.order,
                                                          time=preset.time)
                    food_group.save()

            if form.is_valid():
                form.save()

        else:
            context['form'] = form
        pass
    return render(request, "MealPlans/Days/update_days.html", context=context)


def ajax_load_change_preset(request):
    if request.method == "POST":
        new_preset = MealPreset.objects.get(id=request.POST.get("changed_preset"))

        current_day = Days.objects.get(id=request.POST.get("day_id"))
        current_day_fg = current_day.FoodGroup.all().order_by('time')
        new_preset_list = new_preset.preset_set.all().order_by('time')

        condition = len(current_day_fg) >= len(new_preset_list)
        if condition:
            highest_scheme = current_day_fg
            smallest_scheme = new_preset_list

        else:
            highest_scheme = new_preset_list
            smallest_scheme = current_day_fg

        mapping_list = {}
        for item_smallest in smallest_scheme:
            closest_in_highest, is_before = find_closed_preset(highest_scheme, item_smallest, mapping_list)
            if condition:
                mapping_list[closest_in_highest] = item_smallest
            else:
                mapping_list[item_smallest] = closest_in_highest

        form = PresetDynamicFieldsForm(meal_preset_id=new_preset.id,
                                       matching_dict=mapping_list,
                                       order_list=current_day_fg)

        left_out_list = {}

        if not condition:
            left_out_list = set(highest_scheme) - set(mapping_list.values())

        context = {
            'first_preset': current_day_fg,
            'second_preset': mapping_list,
            'left_out_preset': left_out_list,
            'form': form,
        }
        return render(request, "MealPlans/Ajax/load_change_preset.html", context=context)


def delete_day(request):
    context = {
        "form": DeleteDaysForm()
    }

    if request.method == "POST":
        form = DeleteDaysForm(request.POST or None,
                              instance=Days.objects.get(id=request.POST.get('title')))
        if form.is_valid():
            try:
                Days.objects.get(id=form.cleaned_data['title'].id).delete()
            except Days.DoesNotExist:
                pass
        else:
            context["form"] = form

    return render(request, "MealPlans/Days/delete_days.html", context=context)


def add_dishes_products_to_meal(request):
    context = {'form': SearchForm()}
    if request.method == "POST":
        request.session['group_id'] = request.POST.get("group_id")
        request.session['visible'] = 0
        return render(request, "MealPlans/main_add_dishes_products.html", context=context)


def ajax_load_items_or_more(request):
    context = {}
    display_count = 10
    if request.method == "POST":
        group_id = request.session.get("group_id")
        existing_food_items = FoodGroup.objects.get(id=group_id).food_items.all()
        visible = request.session.get("visible")
        search_changed = request.POST.get("search-changed")
        if search_changed == "true":
            visible = display_count
        else:
            visible += display_count

        filter_items = DishItems.objects.filter(
            name__icontains=request.POST.get("search-keyword"))[visible - display_count:visible]

        context = {'filter_items': filter_items,
                   'existing_food_items': existing_food_items}
        if len(filter_items) == 0 and search_changed != "true":
            return JsonResponse(data={'max_size': 'true'})

        request.session['visible'] = visible
    return render(request, 'MealPlans/Ajax/load_items_or_more.html', context=context)


def ajax_save_items_to_food_group(request):
    if request.method == "POST":

        instance = json.loads(request.session.get("instance"))
        group_id = json.loads(request.session.get("group_id"))
        print(request.POST.get("item_state"))
        add = True if request.POST.get("item_state") == "true" else False
        if add:
            FoodGroup.objects.get(id=int(group_id)).food_items.add(
                DishItems.objects.get(name=request.POST.get("item_key")))
            print("added")
        else:
            FoodGroup.objects.get(id=int(group_id)).food_items.remove(
                DishItems.objects.get(name=request.POST.get("item_key")))
            print("removed")

    return JsonResponse({'status': "success"})


def ajax_save_default_day(request):
    if request.method == "POST":
        data = request.session.get("instance")
        my_dict = json.loads(data)
        my_dict = my_dict[0]
        meal_instance = MealPlans.objects.get(id=int(my_dict['pk']))
        meal_instance.default_day = request.POST.get("current_day").upper()
        meal_instance.save()
        return JsonResponse(data={'status': 'success'})
    return JsonResponse(data={'status': 'fail'})


def ajax_load_days_options_food_group_sub_menu(request, fg_id):
    if request.method == "GET":
        data = request.session.get("instance")
        my_dict = json.loads(data)
        my_dict = my_dict[0]
        fg = FoodGroup.objects.get(id=fg_id)
        context = {
            "meal_items": fg.food_items.all()
        }
        return render(request, "MealPlans/Ajax/load_day_options_food_group_sub_menu.html", context=context)


def ajax_load_copy_meals(request):
    if request.method == "GET":
        copy_meals_from_or_to = request.GET.get("copy_meals_from_or_to")
        copy_meals_from_or_to = True if copy_meals_from_or_to == "true" else False
        request.session["copy_meals_from_or_to"] = copy_meals_from_or_to
        all_meal_plans = {}
        for meal_plan in MealPlans.objects.all():
            all_meal_plans[meal_plan.plan_name] = meal_plan.get_json()

    context = {
        'all_meal_plans': all_meal_plans,
    }
    return render(request, "MealPlans/Ajax/load_copy_meals_widget.html", context=context)


def ajax_submit_copy_meals(request):
    if request.method == "POST":

        data = json.loads(request.POST.get("data"))
        source = int(data['source_food_id'])
        selected_plans = data['selected_plans']
        source_to_selected_plans = request.session['copy_meals_from_or_to']
        selected_plans_food_groups = []

        for plan in selected_plans:
            for day in selected_plans[plan]:
                for meals in selected_plans[plan][day]:
                    selected_plans_food_groups.append(int(meals))

        session = json.loads(request.session.get("instance"))[0]

        plan_name = session["fields"]["plan_name"]

        copy_food_items(source, selected_plans_food_groups, source_to_selected_plans)
        return JsonResponse(
            {"response": "success", "url": reverse("MealPlans:get_meal_plan_single", kwargs={"plan_name": plan_name})})
