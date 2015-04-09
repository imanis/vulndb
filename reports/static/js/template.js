$(function () {
    $(".publish").click(function () {

        $("form").submit();
    });
});


//frontcover
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

// font
$(function () {
    $(".add_font_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_font/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_font_modal_id').html(data);
                $('#add_font_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_font_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_font/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_font_modal_id').modal('hide');
                    $('#add_font_modal_id').children().remove();
                    $('#id_font')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_font_modal_id').html(data);
                    $('#add_font_modal_id').modal('show');
                }
            }
        });
    });
});



// footers
$(function () {
    $(".add_footer_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_footer/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_footer_modal_id').html(data);
                $('#add_footer_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_footer_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_footer/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_footer_modal_id').modal('hide');
                    $('#add_footer_modal_id').children().remove();
                    $('#id_footer')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_footer_modal_id').html(data);
                    $('#add_footer_modal_id').modal('show');
                }
            }
        });
    });
});



// header
$(function () {
    $(".add_header_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_header/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_header_modal_id').html(data);
                $('#add_header_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_header_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_header/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_header_modal_id').modal('hide');
                    $('#add_header_modal_id').children().remove();
                    $('#id_header')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_header_modal_id').html(data);
                    $('#add_header_modal_id').modal('show');
                }
            }
        });
    });
});


// fontsize
$(function () {
    $(".add_fontsize_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/reports/add_font_size/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_fontsize_modal_id').html(data);
                $('#add_fontsize_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_fontsize_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/reports/add_font_size/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_fontsize_modal_id').modal('hide');
                    $('#add_fontsize_modal_id').children().remove();
                    $('#id_font_size')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_fontsize_modal_id').html(data);
                    $('#add_fontsize_modal_id').modal('show');
                }
            }
        });
    });
});