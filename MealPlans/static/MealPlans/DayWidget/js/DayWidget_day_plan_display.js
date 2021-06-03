(function (){
   ael_DW_MPDNW();
})();


function ael_DW_MPDNW() {
    console.log('DayPlanDisplay initializing........');
    let selected_day = window.clientStorage.getItem("instance")['fields']['default_day'].toLowerCase()
   window.clientStorage.setItem(clientStorageProperties.current_day_selected, selected_day );
    document.querySelectorAll('.meal_plans_day_button').forEach(item => {
        item.addEventListener('click', displayPlan);
    });



    function displayPlan() {
        let active_day_id = window.clientStorage.getItem(clientStorageProperties.current_day_selected)
        if (active_day_id) {
            let active_day = document.getElementById("day_"+active_day_id);
            active_day.classList.toggle("day_hide")
            let id = this.getAttribute('id');
            let select_day_id = id.slice(id.indexOf("_")+1, );
            console.log($('#meal_plans_menu_bar'))
            let select_day = document.getElementById("day_"+select_day_id);
            select_day.classList.toggle("day_hide")
            $.ajax({
                url: $('#meal_plans_menu_bar').attr('data-url'),
                type: "POST",
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },

                data: {
                    'current_day': select_day_id,
                },

                success: function (data){
                    console.log(data)
                }
            })
            window.clientStorage.setItem(clientStorageProperties.current_day_selected,select_day_id);

        } else
            console.log("last_plan_id is not utilized properly")


    }


}

