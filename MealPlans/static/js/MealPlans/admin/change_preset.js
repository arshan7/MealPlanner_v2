$(document).ready(function () {
    const initial_value_select = $('#id_presets').val();
    const initial_order = $("#id_order").val();
    $("#id_presets").change(
        function () {

            let val = $(this).val()
            if (initial_value_select !== val) {

                    $.ajax(
                        {
                            url: "http://127.0.0.1:8000/" + this.getAttribute("data-ajax_url"),
                            type: "POST",
                            headers: {
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                            },

                            success: function (data) {
                                console.log(data, "success")
                                $("#id_order").val(data["total"])
                            },
                            data: {

                                'val': val,
                            },
                            failure: function (data) {
                                console.log(data)
                            }
                        }
                    );
                } else {
                    $("#id_order").val(initial_order)
                }
            }

    )
})