(function(){
    ael_FGW_fgdw_collapse();
})();


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