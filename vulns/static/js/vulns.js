$(function () {
  $(".publish").click(function () {
    $("input[name='status']").val("P");
    $("form").submit();
  });

  /*$(".add").click(function () {
    $("form").submit();
  });
*/
  $(".draft").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });

  $(".preview").click(function () {
    $.ajax({
      url: '/vulns/preview/',
      data: $("form").serialize(),
      cache: false,
      type: 'post',
      beforeSend: function () {
        $("#preview .modal-body").html("<div style='text-align: center; padding-top: 1em'><img src='/static/img/loading.gif'></div>");
      },
      success: function (data) {
        $("#preview .modal-body").html(CKEDITOR.instances['id_description'].getData());
      }
    });
  });
    });


$(function () {
    $(".add_category_show_button").click(function () {
        $.ajax({
            type: 'GET',
            url: '/vulns/add_category/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                $('#add_category_modal_id').html(data);
                $('#add_category_modal_id').modal()
            }
        });
    });
});

$(function () {
    $(".add_category_submit_button").click(function () {
        $.ajax({
            type: 'POST',
            url: '/vulns/add_category/',
            data: $("form").serialize(),
            cache: false,
            success: function (data, status) {
                if (data['stat'] == "ok") {
                    $('#add_category_modal_id').modal('hide');
                    $('#add_category_modal_id').children().remove();
                    $('#id_category')
                        .append($("<option></option>")
                            .attr("value", data['new_item_key'])
                            .text(data['new_item_value']))
                        .val(data['new_item_key']);
                }
                else {
                    $('#add_category_modal_id').html(data);
                    $('#add_category_modal_id').modal('show');
                }
            }
        });
    });
});


