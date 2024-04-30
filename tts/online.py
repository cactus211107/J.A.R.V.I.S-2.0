import requests,json,pygame.mixer as mixer,time,soundfile
mixer.init(channels=1)
def tts(text:str,save_path:str):
    request = requests.post('https://api.elevenlabs.io/v1/text-to-speech/IKne3meq5aSn9XLyUdCD/stream',json.dumps({"text":text,"model_id":"eleven_multilingual_v2"}))
    print(request)
    with open(save_path,'wb') as f:f.write(request.content)
    playFile(save_path)
def playFile(path:str):
    mixer.music.load(path)
    mixer.music.play()
    f=soundfile.SoundFile(path)
    t=f.frames / f.samplerate
    print(t)
    time.sleep(t)
    mixer.music.unload(path)
if __name__=='__main__':
    tts('yooo','test.mp3')