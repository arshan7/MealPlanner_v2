(function () {
    ael_submit_search_load_more()
    ael_main_add_items_scroll();
})();


function  ael_main_add_items_scroll(){
    const load_div = document.getElementById("main_add_items");
    load_div.onscroll = function (){
        if(this.scrollTop === this.scrollHeight - this.offsetHeight)
        {
             ajax_search_load_more(false);
        }
    }
}

function ael_submit_search_load_more() {
    const search = document.querySelector("[name=search]");
    let search_value = null
    search.addEventListener("keyup", function (event) {

        if (search_value !== this.value) {
            ajax_search_load_more(true);
            search_value = this.value;
        }

    });

}


function ajax_search_load_more(search_changed) {

    let search_wrapper = document.getElementById("main_add_items_form")
    $.ajax({
        url: search_wrapper.getAttribute("data-url"),
        type: "POST",
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },

        data: {
            'search-keyword': $('[name=search]').val(),
            'search-changed': search_changed,
        },

        success: function (data) {
            if (search_changed) {
                document.getElementById("main_add_items").innerHTML = data;
            } else {
                if (data.hasOwnProperty("max_size"))
                    console.log("do something")
                else
                    document.getElementById("main_add_items").innerHTML += data;
            }
        }
    });

}
