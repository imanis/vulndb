$(function () {
    $(".publish").click(function () {

        $("form").submit();
    });
});

$(function () {
    $(".add_contact_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_contact/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_contact_modal_id').html(data);
                $('#add_contact_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_contact_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_contact/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_contact_modal_id').modal('hide');
                    $('#add_contact_modal_id').children().remove();
                    $('#id_contact')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_contact_modal_id').html(data);
                    $('#add_contact_modal_id').modal('show');
                }
            }
        });
    });
});


