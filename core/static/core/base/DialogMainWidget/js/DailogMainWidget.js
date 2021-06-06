(function () {
    ael_DMW_cancel();
})();


function ael_DMW_cancel() {
    const close = document.querySelector(".dialog_main_close i");
    const wrapper_close = document.querySelector(".dialog_main_wrapper");
    const sub_dialog_container = document.querySelector(".dialog_main_container");

        [close, wrapper_close].forEach(function (element) {
            element.addEventListener('click', function (event) {

                if (event.target === element) {
                    const dialog_sub = document.querySelector(".dialog_main_wrapper");
                    dialog_sub.classList.toggle("dialog_main_show");
                    sub_dialog_container.classList.toggle("dialog_main_default_width_height");
                }
            })
        }
    );
}


function show_dialog_main(){
    document.querySelector(".dialog_main_wrapper").classList.toggle("dialog_main_show")
    document.querySelector(".dialog_main_container").classList.toggle("dialog_main_default_width_height");
}