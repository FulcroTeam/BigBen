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

  function notesLoad(){
     console.log("Ci Pruvamo");
     db = openDatabase('database.db', 1.0, 'my database', 2 * 1024 * 1024);
     db.transaction(function (tx) {
          tx.executeSql('SELECT * FROM notes', [], function (tx, results) {
              var len = results.rows.length, i;
              for (i = 0; i < len; i++) {
                var row = resultSet.rows.item(i);
                document.getElementById("content").innerHTML = ""+document.getElementById("content").innerHTML+
                    "<div class=\"card indigo lighten-1\"><div class=\"card-content white-text\"><span class=\"note-title\">"+row['title']+"</span>"+
                     row['body']+"</div></div><br>";
              }
          });
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
