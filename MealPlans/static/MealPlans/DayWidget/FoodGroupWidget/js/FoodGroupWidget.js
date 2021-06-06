(function(){
    ael_FGW_fgdw_collapse();
    ael_FGW_to_show_sub_dialog();
})();


function ael_FGW_to_show_sub_dialog(){
    document.querySelectorAll(".food_group_options").forEach(function (element){
        element.addEventListener("click", function (event){
            if (event.currentTarget === element){
                show_dialog_sub(element);
            }
        })
    })
}

function ael_FGW_fgdw_collapse(){

    document.querySelectorAll(".food_group_details_wrapper").forEach(
        function (elem){
            elem.addEventListener('click', function (event){

                let parent = elem.closest(".food_group_main_wrapper");
                let child = parent.querySelector(".food_items_section");
                let arrow = parent.querySelector(".food_group_details i");
                if(event.currentTarget === elem){

                    child.classList.toggle("food_items_section_collapse");
                    arrow.classList.toggle("food_group_details_arrow_change");
                }
            })
        }
    )

}