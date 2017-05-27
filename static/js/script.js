$(document).ready(function() {

  //navbar collapse (navigation drawer)
  $(".button-collapse").sideNav();


  function request(data, handler) {
    $.post('/ajax', data, function(data) {
      data = JSON.parse(data);
      console.log(data);
      if(!data.logged) {
        if (window.location.pathname != '/login') {
          window.location = '/login';
        }
      }
      handler(data);
    });
  }

  function tmpUpdate() {
    request({
      'command' : 'temperature',
      'pin' : 1,
      'value' : 0
    }, function(data) {
      $('#tmp').text(data['temperature']+"°C");
    });
  }
  if (window.location.pathname != '/login') {
    tmpUpdate();
    setInterval(tmpUpdate,6000);
  }

  $('.toggle').click(function(e) {
    console.log("toggle: " + this.getAttribute('data-pin'));
    id = this.getAttribute('id');
    request({
      'command' : 'toggle',
      'pin' : this.getAttribute('data-pin'),
      'value' : 0
    }, function(data) {
      $('#' + id).prop('checked', data['on']);
    });
  });
});
