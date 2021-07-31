(function () {
    ael_ud_name();
})()


function ael_ud_name() {
    const title = document.getElementById("id_all_days");
    title.addEventListener("change", function (event) {
        const form = document.getElementById("update_days_form")
        let url = form.getAttribute("action");
        url += title.options[title.selectedIndex].value
        call_update_food_groups(url)
    })
}

function call_update_food_groups(url) {
    window.location.href = url
}

$(document).ready(function () {
    let preset = $('#id_preset');
    let initial_preset = preset.val()
    preset.change(function () {
        let changed_preset = $(this).val()
        let day = $('#id_all_days').val();
        if (initial_preset !== changed_preset) {
            if (changed_preset !== "") {
                $.ajax(
                    {
                        url: "http://127.0.0.1:8000/mealplans/day/load_change_preset",
                        type: "POST",
                        headers: {
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        },

                        success: function (data) {
                            console.log( "success")
                            $('#load_change_preset').html(data)
                        },
                        data: {
                            'day_id': day,
                            'changed_preset': changed_preset,
                            'old_preset': initial_preset,
                        },
                        failure: function (data) {
                            console.log(data)
                        }
                    }
                );
            }

        }
    });
})