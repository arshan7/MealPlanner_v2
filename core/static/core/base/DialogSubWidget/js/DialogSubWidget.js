(function () {
    ael_DSW_cancel();
})();


function ael_DSW_cancel() {
    const close = document.querySelector(".dialog_sub_close i");
    const wrapper_close = document.querySelector(".dialog_sub_wrapper");


    [close, wrapper_close].forEach(function (element) {
            element.addEventListener('click', function (event) {

                if (event.target === element) {
                    close_dialog_sub();
                }
            })
        }
    );
}

function close_dialog_sub() {
    const dialog_sub = document.querySelector(".dialog_sub_wrapper");
    const sub_dialog_container = document.querySelector(".dialog_sub_container");
    dialog_sub.classList.toggle("dialog_sub_show");
    sub_dialog_container.classList.toggle("dialog_default_width_height");
}

function show_dialog_sub(called_element, class_name_for_width_height) {

    const sub_dialog = document.querySelector(".dialog_sub_wrapper");

    let positionBox = called_element.getBoundingClientRect();

    const sub_dialog_container = document.querySelector(".dialog_sub_container");
    sub_dialog.classList.toggle("dialog_sub_show");
    sub_dialog_container.classList.toggle("dialog_default_width_height");

    let bottom_space_available = Math.abs(window.innerHeight - positionBox.bottom);
    let upper_space_available = positionBox.top;

    let right_space_available = Math.abs(window.innerWidth - positionBox.right);
    let left_space_available = positionBox.left;

    let scrollbar_width;
    let scrollbar_height;
    if (window.scrollbars.visible) {

        scrollbar_width = Math.abs(window.innerWidth - document.documentElement.clientWidth);
        scrollbar_height = Math.abs(window.innerHeight - document.documentElement.clientHeight)
    }

    sub_dialog_container.style.top = ""
    sub_dialog_container.style.bottom = ""
    sub_dialog_container.style.left = ""
    sub_dialog_container.style.right = ""

    let dialog_from_right = Math.abs(window.innerWidth - positionBox.left - scrollbar_width) + "px";
    let dialog_from_bottom = Math.abs(window.innerHeight - positionBox.top - scrollbar_height) + "px"

    if (sub_dialog_container.offsetWidth <= right_space_available) {
        sub_dialog_container.style.left = positionBox.right + "px";
    } else if (sub_dialog_container.offsetWidth < left_space_available) {
        sub_dialog_container.style.right = dialog_from_right;
    } else {
        if (left_space_available >= right_space_available) {
            sub_dialog_container.style.right = dialog_from_right;
            sub_dialog_container.style.width = left_space_available + "px";
        } else {
            sub_dialog_container.style.left = positionBox.right + "px";
            sub_dialog_container.style.width = right_space_available + "px";
        }

    }


    if (sub_dialog_container.offsetHeight <= bottom_space_available) {
        sub_dialog_container.style.top = positionBox.bottom + "px";
    } else if (sub_dialog_container.offsetHeight <= upper_space_available) {
        sub_dialog_container.style.bottom = dialog_from_bottom;
    } else {
        if (left_space_available >= right_space_available) {
            sub_dialog_container.style.right = dialog_from_right;
        } else {
            sub_dialog_container.style.left = positionBox.right + "px";
        }
        sub_dialog_container.style.top = positionBox.top + (called_element.offsetHeight / 2)
            - (sub_dialog_container.offsetHeight / 2) + "px";
    }


}