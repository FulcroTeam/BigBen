$(document).ready(function() {
  $(".button-collapse").sideNav();

  $('#kitchen_light').click(function(e) {
    var request_data = {
      'command' : 'toggle',
      'pin' : 13,
      'value' : 0
    };
    $.post('http://192.168.1.3:8080/ajax', request_data, function(data) {
      console.log(data);
      $('#kitchen_light').prop('checked', data['on']);
    });
  });
});
