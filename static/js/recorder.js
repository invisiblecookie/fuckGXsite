var recordButton = document.getElementById('record-button');
var stopButton = document.getElementById('stop-button');
var audioChunks = [];
var mediaRecorder;
var audioContext = new AudioContext();



recordButton.addEventListener('click', function() {
    
    console.log("start recording");
    //console.log(MediaRecorder.isTypeSupported('audio/wav'));
    //console.log(MediaRecorder.isTypeSupported('audio/webm;codecs=opus'))
    //audio/webmcodecs=opus
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      console.log(mediaRecorder.state);

      mediaRecorder.addEventListener('dataavailable', function(event) {
        audioChunks.push(event.data);
      });
    });
});

stopButton.addEventListener('click', function() {
    console.log("pressed stop");

  mediaRecorder.requestData();
  mediaRecorder.stop();
  console.log(mediaRecorder.state);
  console.log(mediaRecorder.mimeType);
  var audioBlob = new Blob(audioChunks, { 'type' : 'audio/webm;codecs=opus' });
  var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  var formData = new FormData();
  formData.append('audio', audioBlob, 'audio.webm');
  formData.append('csrfmiddlewaretoken', csrfToken);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/save-audio/');
  xhr.onload = function() {
    console.log('音频上传');
  };
  xhr.send(formData);
});