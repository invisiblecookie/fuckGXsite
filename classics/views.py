from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotAllowed,JsonResponse, HttpResponseBadRequest

from django.views.decorators.csrf import csrf_exempt
from .models import *
from markdown import markdown
import wave,os,subprocess
from django.core.files.storage import FileSystemStorage

import pyaudio
import wave
import librosa
import numpy as np

from threading import Timer
import json

# Create your views here.
def home(request):
    cata1 = Book.objects.filter(set='经')
    cata2 = Book.objects.filter(set='史')
    cata3 = Book.objects.filter(set='子')
    cata4 = Book.objects.filter(set='集')
    
    context = {'cata1':cata1, 'cata2':cata2, 'cata3':cata3, 'cata4':cata4}
    return render(request,'classics/main.html', context)
    

def DisplayCatalog(request, slug): 
    
    book = Book.objects.get(slug=slug)
    subtitles = book.subtitle_set.all() 
    context = {'book':book, 'subtitles':subtitles}
    return render(request,'classics/catalog.html', context)

def Displaycontent(request, book_slug, sub_slug):
    subtitle = Subtitle.objects.get(slug=sub_slug)
    content = markdown(subtitle.content,extensions=[
		'markdown.extensions.extra',])
    context = {'subtitle':subtitle, 'content':content}
    return render(request,'classics/content.html', context)


def mfcc_librosa(wav_file):
    #wav_file="sj1.wav"
    # 读取音频数据
    y,sr = librosa.load(wav_file)
    #print(y,sr)
    # 提取特征
    fea = librosa.feature.mfcc(y=y,sr=sr,n_mfcc=13,n_mels=26,n_fft = 2048, win_length=2048,hop_length=80,lifter=12)
    print(fea.shape)
    # 进行正则化
    mean = np.mean(fea,axis=1,keepdims=True)
    std = np.std(fea,axis =1,keepdims=True)
    fea = (fea-mean)/std
    print(fea.shape)
    # 添加1阶差分
    fea_d = librosa.feature.delta(fea)
    fea = np.concatenate([fea.T, fea_d.T],axis=1)
    print(fea.shape)
    return fea 

'''

@csrf_exempt
def record_audio(request):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    #RECORD_SECONDS =5
    FILENAME = 'audio.wav'

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    stop_recording = False
    timer = None
    
    def timeout():
        nonlocal stop_recording 
        stop_recording = True
        
    timer = Timer(5, timeout)
    print(timer)
    timer.start()
    print(stop_recording)
    while not stop_recording:
        #print(stop_recording)
        data = stream.read(CHUNK)
        frames.append(data)
        #print(json.loads(request.body.decode()).get('stop'))
        if json.loads(request.body.decode()).get('stop') == 1:
            print("stop")
            stop_recording = True            
            if timer:
                timer.cancel()
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    labels = ["han-shu","lao-zi","zhou-yi","shi-jing"]
    models = np.load("models_hmmlearn_rosa.npy",allow_pickle=True)
    fea = mfcc_librosa("audio.wav")
    scores = []
    for m in range(4):
        model = models[m]
        score,_ = model.decode(fea)
        scores.append(score)
    
    det_lab = labels[np.argmax(scores)]
    print(det_lab)

    return HttpResponse('录音已完成')


@csrf_exempt
def save_audio(request):
    if request.method == 'POST' and request.FILES['audio']:
        audio_file = request.FILES['audio']
        fs = FileSystemStorage()

        if not os.path.exists('audio'):
            os.makedirs('audio')

        fs.save('audio/' + audio_file.name, audio_file)
        subprocess.call(['ffmpeg','-i','F:\\Computer\\Grad\\shit2\\guoxueSite\\audio\\audio.webm','audio.wav'])
        return HttpResponse('音频已上传')
    else:
        return HttpResponseNotAllowed(['POST'])
        '''
@csrf_exempt
def record_audio(request):
    global audio_frames

    # 检查请求方法是否为 GET
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    #RECORD_SECONDS =5
    #global FILENAME
    #FILENAME = 'audio.wav'

    global p
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    audio_frames = []
    while True:

        stop_flag = request.GET.get('stop', False)
        if stop_flag:
            break
        data = stream.read(CHUNK)
        audio_frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return JsonResponse({"message": "Recording stopped."})

@csrf_exempt
def save_audio(request):
    global audio_frames
    global p
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    #RECORD_SECONDS =5
    FILENAME = 'audio.wav'
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    wf = wave.open(FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

    # 清空音频数据列表
    audio_frames = []

    return JsonResponse({"message": "File saved."})
