(function () {
    ael_ui_name();
})()


function ael_ui_name() {
    const name = document.getElementById("id_title");
    name.addEventListener("change", function (event) {
        const form = document.getElementById("update_food_groups_form")
        let url = form.getAttribute("action");
        url += name.options[name.selectedIndex].value
        call_update_food_groups(url)
    })
}

function call_update_food_groups(url) {
    window.location.href = url
}