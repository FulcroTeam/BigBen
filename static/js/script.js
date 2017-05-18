$(document).ready(function() {

  tmpUpdate();
  setInterval(tmpUpdate,6000);

  $(".button-collapse").sideNav();

  function tmpUpdate() {
      var request_data = {
        'command' : 'temperature',
        'pin' : 0,
        'value' : 0
      };
      $.post('http://localhost:8080/ajax', request_data, function(data) {
        data = JSON.parse(data)
        console.log(data);
        $('#tmp').text(data['temperature']+"°C");
      });

      return false;
  }

  $('#kitchen_light').click(function(e) {
    var request_data = {
      'command' : 'toggle',
      'pin' : 13,
      'value' : 0
    };
    $.post('http://localhost:8080/ajax', request_data, function(data) {
      data = JSON.parse(data)
      console.log(data);
      $('#kitchen_light').prop('checked', data['on']);
    });
  });



});
