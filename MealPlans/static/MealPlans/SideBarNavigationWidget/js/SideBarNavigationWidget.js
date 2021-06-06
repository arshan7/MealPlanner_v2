(function () {
    initialize_side_bar_navigation()
})();

function initialize_side_bar_navigation() {
    const side_bar_button = document.getElementById("meal_plans_side_bar_button");
    const side_bar_close = document.getElementById("meal_plans_side_bar_close");
    side_bar_button.addEventListener("click", function (event) {
        event.preventDefault();
        if (event.currentTarget === side_bar_button) {
            const meal_plan_menu_bar = document.getElementById("meal_plans_menu_bar");
            let box = get_box_exact_location(meal_plan_menu_bar);
            // let style = window.getComputedStyle(side_bar_button);
            let side_bar_height = box.top + meal_plan_menu_bar.offsetHeight;
            const sidebar = document.getElementById("meal_plans_side_bar");
            sidebar.style.top = side_bar_height + "px";
            meal_plan_collapse_sidebar();
        }
    });

    side_bar_close.addEventListener("click", meal_plan_collapse_sidebar);
}

function meal_plan_collapse_sidebar() {

    const sidebar = document.getElementById("meal_plans_side_bar");
    sidebar.classList.toggle("meal_plans_side_bar_show");

}

