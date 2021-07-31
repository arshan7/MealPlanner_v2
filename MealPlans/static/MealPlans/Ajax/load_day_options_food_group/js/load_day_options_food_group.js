function ael_LDOFG_menu_items() {


    let copy_meals_from = window.ClientObjectsHolder.push("#copy_meals_from", {'send_type': false});
    let copy_meals_to = window.ClientObjectsHolder.push("#copy_meals_to", {'send_type': true});

    if(copy_meals_to.html_object)
    copy_meals_to.attach_event_listeners('click', (event) => {
        load_day_options_common_functionality(event, copy_meals_to,);
    });

    if(copy_meals_from.html_object)
    copy_meals_from.attach_event_listeners('click', (event) => {
        load_day_options_common_functionality(event, copy_meals_from,);
    });

}
function load_day_options_common_functionality(event, sub_menu_option, option_state) {

    if (event.target === sub_menu_option.html_object) {
        event.preventDefault();
        close_dialog_sub();
        let p = new Promise((resolve, reject) => {
            $.ajax({
                url: sub_menu_option.html_object.getAttribute("href"),
                type: "GET",
                data:{'copy_meals_from_or_to':sub_menu_option.send_type},
                success: function (data) {
                    document.querySelector(".dialog_main_content").innerHTML = data;
                    resolve();
                }
            });
        });

        p.then(() => {
            show_dialog_main();
            ajax_initialize("all_meal_plans");
            ael_CMW();
        })
    }
}