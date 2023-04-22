var recordButton = document.getElementById('record-button');
var stopButton = document.getElementById('stop-button');
/*
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  var csrftoken = getCookie('csrftoken');
*/
var stop_flag;

function startRecording() {
  stop_flag = false
  var xhr = new XMLHttpRequest();

  xhr.open("POST", "/record_audio/");

  xhr.send();

  setTimeout(function() {
    if (!stop_flag){
      stopRecording();
    }
    
  }, 5000);
}

function stopRecording() {
  recordButton.innerText = '语音搜索';
  stop_flag = true
  var xhr = new XMLHttpRequest();

  xhr.open("POST", "/save_audio/");

  var data = new FormData();
  data.append('stop', true);

  xhr.send(data);
}

recordButton.addEventListener('click', function() {
    recordButton.innerText = '正在录音';
    startRecording();
  });

stopButton.addEventListener('click', function() {
    
    stopRecording();
  }); 

    //var xhr = new XMLHttpRequest();
    //xhr.open('POST', '/save_audio/');
    //xhr.setRequestHeader('X-CSRFToken', csrftoken);
    //xhr.setRequestHeader('Content-Type', 'application/json');
    //xhr.send(JSON.stringify({stop: 1}));
    //var data = new FormData();
    //data.append('stop', true);
    //xhr.send(data);



