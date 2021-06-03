
from django.forms.widgets import Select, TextInput


class AutoComplete(Select):
    template_name = "MealPlans/MealPlanCustomWidgets/datalist.html"
    option_template_name = "MealPlans/MealPlanCustomWidgets/datalist_option.html"


class TimeWidget(TextInput):
    input_type = 'time'
