function save_item_to_food_group(element) {
    console.log(element.checked)

    $.ajax({
        url: $('#food_item_load_submit').attr('formaction'),
        type: "POST",
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        data: {
            'item_state': element.checked,
            'item_key' : $(element).attr('data-item_id'),
            'item_key' : $(element).attr('data-item_id'),
        },
        success: function (data) {
            console.log("success")
        },}
    );
}