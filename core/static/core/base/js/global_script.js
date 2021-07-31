
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


function ajax_initialize(name){
    const script_data = document.getElementById(name);
        const value = JSON.parse(script_data.textContent);
        window.clientStorage.setItem(name, value)
        script_data.remove();
}

class ClientObjectsHolder{
    all_objects = {}

    push(selector, properties={}, behaviours={}, initialize){
        this.all_objects[selector] = new ClientObject(selector, properties, behaviours,initialize )
        return this.all_objects[selector]
    }

    get(selector){
        return this.all_objects[selector]
    }

}

window.ClientObjectsHolder= new ClientObjectsHolder();


class ClientObject {
    html_object = null;
    state = {}
    behaviours = {}
    initialize= ()=>{console.log("Initialize is called without initialize")}

    setItem(key, value) {
        this.state[key] = value;
    }

    setBehaviour(key, functionDefinition){
        this.behaviours[key] = functionDefinition;
    }

    getBehaviour(key)
    {
        return this.behaviours[key];
    }

    callBehaviour(key){
        this.getBehaviour(key)(arguments)
    }


    getItem(key) {
        return this.state[key];
    }

    constructor(selector, properties= {}, behaviours={}) {
        this.html_object = document.querySelector(selector);
        for(let property in properties){
            this[property] = properties[property]
        }

        for(let behaviour in behaviours){
            this.setBehaviour(behaviour, behaviours[behaviour])
        }
    }

    ajax(properties={url:'', method:'', success:null, data:null}){
        $.ajax({
            url:properties.url,
            method: properties.method,
            success: function (data){
                properties.success(data);
            },
            data:properties.data,
            onerror: function (error){
                console.log(error)
            }
        });
    }

    attach_event_listeners(type='click', callable ){
        this.html_object.addEventListener(type, callable);
    }



}