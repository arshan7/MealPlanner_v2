function ael_CMW() {

    this.clientStorage.setItem(clientStorageProperties.selected_plans, {});

    const add_meal = document.getElementById("CMW_add");
    add_meal.addEventListener("click", function (event) {
        event.preventDefault();
        add_selected_data_to_dialog()
    });
    make_CMW_button_disabled_enabled();

    const copyMeals_submit = document.getElementById("CMW_selected_submit");
    const token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    copyMeals_submit.addEventListener("click", function (event) {
        event.preventDefault();
        let data_to_send = {
                selected_plans: window.clientStorage.getItem("selected_plans"),
                source_food_id: window.clientStorage.getItem(clientStorageProperties.current_category_selected),
            };
        $.ajax({
            url: copyMeals_submit.getAttribute("data-url"),
            data: {"data":JSON.stringify(data_to_send)},
            method: "POST",
            headers: {
                "x-CSRFToken": token,
            },
            success: function (data) {
                window.location.href=data.url;
            }
        });
    });


    let plan_name_select = window.ClientObjectsHolder.push("#CMW_plan_name_select", {},
        {},);
    plan_name_select.initialize = () => {
        for (let plan in window.clientStorage.getItem("all_meal_plans")) {
            plan_name_select.html_object.append(create_option(plan, plan, false, false));
        }

    }
    plan_name_select.initialize();



    let day_name_select = window.ClientObjectsHolder.push("#CMW_day_name_select", {}, {},
    );
    day_name_select.initialize = () => {

        let all_meal_plans = window.clientStorage.getItem("all_meal_plans")
        let days = all_meal_plans[plan_name_select.html_object.value]["days"]

        for (let day in days) {
            day_name_select.html_object.append(create_option(day, day, false))
        }

    };

    plan_name_select.attach_event_listeners('change', () => {
        CMW_reset_option(day_name_select.html_object, "please select a meal");
        day_name_select.initialize(day_name_select);
        make_CMW_button_disabled_enabled();
    })


    let meal_name_select = window.ClientObjectsHolder.push("#CMW_meal_name_select", {}, {},
    );
    meal_name_select.initialize = () => {
        let all_meal_plans = window.clientStorage.getItem("all_meal_plans")
        let meals = all_meal_plans[plan_name_select.html_object.value]["days"][day_name_select.html_object.value]["food_groups"];

        for (let meal in meals) {
            meal_name_select.html_object.append(create_option(meal, meals[meal]['title'], false))
        }
    }


    day_name_select.attach_event_listeners('change', () => {
        CMW_reset_option(meal_name_select.html_object, "please select a meal");
        meal_name_select.initialize();
        make_CMW_button_disabled_enabled();
    });

    meal_name_select.attach_event_listeners('change', () => {

        let all_meal_plans = window.clientStorage.getItem("all_meal_plans")

        let foods = all_meal_plans[plan_name_select.html_object.value]["days"][day_name_select.html_object.value]["food_groups"][meal_name_select.html_object.value]["items"];

        const meals_container = document.getElementById("CMW_selected_available_container");
        meals_container.innerHTML = "";

        if (foods) {

            for (let food of foods) {
                let food_div = document.createElement('div');
                food_div.classList.add("CMW_meals");
                food_div.append(document.createTextNode(food))
                meals_container.appendChild(food_div);
            }

        } else {
            meals_container.append(document.createTextNode("No Meals are present"));
        }

        make_CMW_button_disabled_enabled();
    })


}



function CMW_reset_option(parent_object, string_to_display) {
    parent_object.innerHTML = "";
    parent_object.append(create_option(string_to_display, string_to_display, true, true))

}

function create_option(value, text, is_disabled, is_selected) {
    const option = document.createElement("option")
    option.setAttribute("value", value)
    option.append(document.createTextNode(text));
    if (is_disabled)
        option.setAttribute("disabled", "")
    if (is_selected)
        option.setAttribute("selected", "")
    return option;
}

function make_CMW_button_disabled_enabled() {
    const select_plan = document.getElementById("CMW_plan_name_select").selectedIndex;
    const select_day = document.getElementById("CMW_day_name_select").selectedIndex;
    const select_category = document.getElementById("CMW_meal_name_select").selectedIndex;
    const CMW_add = document.getElementById("CMW_add");
    if (select_plan === 0 || select_day === 0 || select_category === 0) {
        CMW_add.setAttribute("disabled", "");
    } else {
        CMW_add.removeAttribute("disabled");
    }
}

function add_selected_data_to_dialog() {
    const select_plan = document.getElementById("CMW_plan_name_select");
    const select_day = document.getElementById("CMW_day_name_select");
    const select_category = document.getElementById("CMW_meal_name_select");
    let existed_plans = clientStorage.getItem(clientStorageProperties.selected_plans);
    if (existed_plans[select_plan.value]) {
        if (existed_plans[select_plan.value][select_day.value]) {
            if (!existed_plans[select_plan.value][select_day.value].includes(select_category.options[select_category.selectedIndex].text)) {
                existed_plans[select_plan.value][select_day.value].push(select_category.value);
                clientStorage.setItem(clientStorageProperties.selected_plans, existed_plans);
                add_new_category(select_plan.value, select_day.value, select_category.options[select_category.selectedIndex].text);
            } else {
                console.log("already_submitted")
            }
        } else {
            existed_plans[select_plan.value][select_day.value] = [select_category.value];

            add_new_day(select_plan.value, select_day.value, select_category.options[select_category.selectedIndex].text);
        }
    } else {
        existed_plans[select_plan.value] = {[select_day.value]: [select_category.value]};
        add_new_plan(select_plan.value, select_day.value, select_category.options[select_category.selectedIndex].text);
    }
}

function add_new_category(plan, day, category) {
    create_copyMeal_selected_category(plan, day, category);
}

function add_new_day(plan, day, category) {
    create_copyMeal_selected_day(plan, day);
    create_copyMeal_selected_category(plan, day, category);
}

function add_new_plan(plan, day, category) {
    create_copyMeal_selected_plan(plan);
    create_copyMeal_selected_day(plan, day);
    create_copyMeal_selected_category(plan, day, category);

}

function remove_exist_category(plan, day, category) {

    document.getElementById("copyMeal_selected_categories_" + plan + "_" + day).removeChild(
        document.getElementById("CMW_selected_category_" + plan + "_" + day + "_" + category)
    );

    let plans = window.clientStorage.getItem(clientStorageProperties.selected_plans);
    plans[plan][day].indexOf(category) !== -1 ? plans[plan][day].splice(plans[plan][day].indexOf(category), 1) : "";

    if (plans[plan][day].length === 0) {
        if (Object.keys(plans[plan]).length === 1) {
            remove_exist_plan(plan);
        } else {
            remove_exist_day(plan, day);
        }
    }
}

function remove_exist_day(plan, day) {
    let plans = window.clientStorage.getItem(clientStorageProperties.selected_plans);
    document.getElementById("CMW_selected_days_container_" + plan).removeChild(
        document.getElementById("CMW_selected_day_" + plan + "_" + day)
    );
    delete plans[plan][day];

    if (Object.keys(plans[plan]).length === 0) {
        remove_exist_plan(plan);
    }

}

function remove_exist_plan(plan) {
    let plans = window.clientStorage.getItem(clientStorageProperties.selected_plans);
    document.getElementById("CMW_selected_meals_container").removeChild(
        document.getElementById("CMW_selected_plan_" + plan)
    );
    delete plans[plan];
}

function create_copyMeal_selected_plan(plan) {
    let CMW_selected_plan = document.createElement('div');
    CMW_selected_plan.classList.add("CMW_selected_plan");
    CMW_selected_plan.setAttribute("id", "CMW_selected_plan_" + plan);

    let CMW_selected_plan_header = document.createElement("header");
    CMW_selected_plan_header.classList.add("CMW_selected_plan_header");

    let CMW_selected_plan_name = document.createElement("p");
    CMW_selected_plan_name.innerText = plan;

    let CMW_selected_plan_close = document.createElement("button");
    CMW_selected_plan_close.innerText = "Remove plan";
    CMW_selected_plan_close.setAttribute("id", "CMW_selected_plan_close");
    CMW_selected_plan_close.addEventListener("click", function () {
        remove_exist_plan(plan);
    });

    CMW_selected_plan_header.append(CMW_selected_plan_name, CMW_selected_plan_close);

    let CMW_selected_days_container = document.createElement("div");
    CMW_selected_days_container.setAttribute("id", "CMW_selected_days_container_" + plan);

    CMW_selected_plan.append(CMW_selected_plan_header, CMW_selected_days_container);

    const CMW_selected_meals_container = document.getElementById("CMW_selected_meals_container");
    CMW_selected_meals_container.appendChild(CMW_selected_plan);
}

function create_copyMeal_selected_day(plan, day) {
    let CMW_selected_day = document.createElement("div");
    CMW_selected_day.setAttribute("id", "CMW_selected_day_" + plan + "_" + day);
    CMW_selected_day.classList.add("CMW_selected_day");

    let CMW_selected_day_name = document.createElement("div");
    CMW_selected_day_name.classList.add("CMW_selected_day_name");

    let CMW_selected_day_name_p = document.createElement("p");
    CMW_selected_day_name_p.innerText = day;
    CMW_selected_day_name.appendChild(CMW_selected_day_name_p);


    let CMW_selected_categories = document.createElement("div");
    CMW_selected_categories.setAttribute("id", "copyMeal_selected_categories_" + plan + "_" + day);
    CMW_selected_categories.classList.add("CMW_selected_categories");

    let CMW_selected_day_close = document.createElement("button");
    CMW_selected_day_close.classList.add("CMW_selected_day_close")
    CMW_selected_day_close.setAttribute("id", "CMW_selected_day_close");
    CMW_selected_day_close.innerText = "Remove day";
    CMW_selected_day_close.addEventListener("click", function () {
        remove_exist_day(plan, day);
    })

    CMW_selected_day.append(CMW_selected_day_name,
        CMW_selected_categories,
        CMW_selected_day_close);

    document.getElementById("CMW_selected_days_container_" + plan).append(CMW_selected_day);
}

function create_copyMeal_selected_category(plan, day, category) {

    let CMW_selected_category = document.createElement("div");
    CMW_selected_category.classList.add("copyMeal_selected_category");
    CMW_selected_category.setAttribute("id", "CMW_selected_category_" + plan + "_" + day + "_" + category)

    let CMW_selected_category_name = document.createElement("p");
    CMW_selected_category_name.innerText = category;

    let CMW_selected_category_close = document.createElement("button");
    CMW_selected_category_close.innerText = "Remove";
    CMW_selected_category_close.addEventListener("click", function () {
        remove_exist_category(plan, day, category);
    });

    CMW_selected_category.append(CMW_selected_category_name, CMW_selected_category_close);
    document.getElementById("copyMeal_selected_categories_" + plan + "_" + day).appendChild(CMW_selected_category);

}