$(function () {
    $(".publish").click(function () {

        $("form").submit();
    });
});

$(function () {
    $(".add_frontcover_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_frontcover/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_frontcover_modal_id').html(data);
                $('#add_frontcover_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_frontcover_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_frontcover/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_frontcover_modal_id').modal('hide');
                    $('#add_frontcover_modal_id').children().remove();
                    $('#id_front_cover')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_frontcover_modal_id').html(data);
                    $('#add_frontcover_modal_id').modal('show');
                }
            }
        });
    });
});


