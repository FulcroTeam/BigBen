$(document).ready(function() {
  $(".button-collapse").sideNav();

  $('#kitchen_light').click(function(e) {
    var request_data = {
      'command' : 'toggle',
      'pin' : 13,
      'value' : 0
    };
    $.post('http://localhost:8080/ajax', request_data, function(data) {
      console.log(data);
      $('#kitchen_light').prop('checked', data['on']);
    });
  });
  $('#condizionatore').click(function(e) {
    var request_data = {
      'command' : 'toggle',
      'pin' : 3,
      'value' : 0
    };
    $.post('http://localhost:8080/ajax', request_data, function(data) {
      console.log(data);
      $('#condizionatore').prop('checked', data['on']);
    });
  });
});
