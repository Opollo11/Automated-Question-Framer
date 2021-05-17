from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .utils import audio_to_questions
import os
from mysite.settings import BASE_DIR


from pydub import AudioSegment
import math

class SplitWavAudioMubin():
    def __init__(self, folder, filename,filepath):
        self.folder = folder
        self.filename = filename
        self.filepath = filepath
        
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        split_audio = self.audio[t1:t2]
        new_file_name = os.path.join(self.folder, split_filename)
        split_audio.export(new_file_name, format="wav")
        return new_file_name

    def multiple_split(self, sec_per_split):
        total_sec = math.floor(self.get_duration())
        print(f"{total_sec=}")
        split_file_list = []
        for i in range(0, total_sec, sec_per_split):
            split_fn = str(i) + '_' + self.filename
            new_file_path = self.single_split(i, min(i+sec_per_split,total_sec), split_fn)            
            split_file_list.append(new_file_path)
        return split_file_list


@csrf_exempt
def audioToQuestions(request):
    if(request.method=="POST"):
        request_file = request.FILES['audio_file']
        if request_file:            
            fs = FileSystemStorage()
            file = fs.save(request_file.name, request_file)
            folder = os.path.join(BASE_DIR, 'media')                
            split_wav = SplitWavAudioMubin(folder, file, os.path.join(BASE_DIR, 'media',file))
            split_file_list = split_wav.multiple_split(sec_per_split=10)                                
            questions = audio_to_questions(split_file_list)

            return JsonResponse({"questions":questions})
            # return JsonResponse(None)