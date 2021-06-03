(function () {
    ael_ui_name();
})()


function ael_ui_name(){
    const name = document.getElementById("id_name");
    name.addEventListener("change", function(event){
        const form = document.getElementById("update_ingredient_form")
        let url = form.getAttribute("action");
        url += name.options[name.selectedIndex].text
        call_update_ingredient(url)
    })
}

function call_update_ingredient(url){
    window.location.href = url
}