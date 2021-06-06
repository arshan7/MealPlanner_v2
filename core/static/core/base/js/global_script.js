
function get_box_exact_location(elem){
    let left = window.scrollX !== undefined ? window.pageXOffset :
        (document.documentElement || document.body.parentNode || document.body).scrollLeft;
    let top = window.scrollY !== undefined ? window.pageYOffset :
        (document.documentElement || document.body.parentNode || document.body).scrollTop;
    let box = elem.getBoundingClientRect();

    let top_total = box.top;
    let left_total = box.left ;

    return {"top": top_total, "left": left_total}

}


// field attribute value must be stringified_json
function postForm(path, params) {

    let form = document.createElement('form');
    form.setAttribute('method', 'post');
    form.setAttribute('action', path);

    for (let key in params) {
        if (params.hasOwnProperty(key)) {
            let field = document.createElement('input');
            field.setAttribute('type', 'hidden');
            field.setAttribute('name', key);
            field.setAttribute('value', params[key]);
            form.appendChild(field);
        }
    }

    return form;
}
