$(function () {
  function check_messages() {
    $.ajax({
      url: '/messages/check/',
      cache: false,
      success: function (data) {
        $("#unread-count").text(data);
        if (data !=0)
            $("#unread-count").addClass("new-notifications");
      },
      complete: function () {
        window.setTimeout(check_messages, 60000);
      }
    });
  };
  check_messages();
});