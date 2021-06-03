(function () {
    attach_event_listener_for_plan_name();
    ael_for_upm_selects();
})()

function attach_event_listener_for_plan_name() {
    const select_plan = document.getElementById("id_plan_name");
    select_plan.addEventListener("change", function (event) {
        call_update_meal_plan(select_plan.options[select_plan.selectedIndex].text)
    });
}

function call_update_meal_plan(plan_name) {
    const form = document.getElementById("update_meal_plan_form");
    window.location.href = form.getAttribute("action")+ plan_name;
}

//attach event listeners for Update meal plans
function ael_for_upm_selects() {
    const form = document.getElementById("update_meal_plan_form");
    document.querySelectorAll(".UpdateMealPlan_Select").forEach(function (select) {
            select.addEventListener("change", function (event) {
                    let request = form.getAttribute("data-ajax_load");
                    let day_name = select.options[select.selectedIndex].text;
                    let where_to_load = select.getAttribute("name")
                    const token = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    AjaxHandler({
                        request_location: request,
                        data: JSON.stringify({"day_name": day_name}),
                        method: "POST",
                        token:{header:"X-CSRFToken", value:token},
                        handler: function (response) {
                            let id = where_to_load
                            handle_load_meal_plans_based_on_day(response, id)
                        },
                    }).then();

                }
            )
        }
    );
}

function handle_load_meal_plans_based_on_day(response, id) {
    document.getElementById("load_meal_" + id).innerHTML = response
}

