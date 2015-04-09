$(function () {
    $(".publish").click(function () {

        $("form").submit();
    });
});

$(function () {
    $(".add_client_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/projects/add_client/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_client_modal_id').html(data);
                $('#add_client_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_client_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/projects/add_client/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_client_modal_id').modal('hide');
                    $('#add_client_modal_id').children().remove();
                    $('#id_client')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_client_modal_id').html(data);
                    $('#add_client_modal_id').modal('show');
                }
            }
        });
    });
});


