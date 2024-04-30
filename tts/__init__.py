import os,subprocess,pyttsx3,threading,time,re
from queue import Queue

import llm_parser
import llm_parser.function_parser
# from pydub import AudioSegment
# from pydub.playback import play

# Global shared queue
QUEUE = Queue()
_SPEAKING_QUEUE = Queue()
VOICE = 'com.apple.eloquence.en-GB.Reed'

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('voice', VOICE)

is_llm_finished = False

# def play_wav(file_path):
#     # Load the MP3 file
#     audio = AudioSegment.from_file(file_path,'aviff')

#     # Play the audio
#     play(audio)
import subprocess,random
def play_audio(file_path:str,graphics:bool=False):subprocess.call(f'ffplay "{file_path}" -noborder -autoexit -hide_banner -loglevel error {"-showmode 1" if graphics else "-nodisp"}',shell=True,stdout=subprocess.PIPE)
def speak():
    while True:
        if not _SPEAKING_QUEUE.empty():
            item = _SPEAKING_QUEUE.get()
            if item.startswith('*') and item.find('whir'):
                play_audio(f'media/audio/sfx/whirr{random.randint(1,3)}.wav')
            else:
                play_audio(item)
        if _SPEAKING_QUEUE.empty() and os.environ['STATE']=='generating finished':
            os.environ['STATE']='listening'
        time.sleep(0.5)

def save_to_folder():
    i = 1
    while True:
        if not QUEUE.empty():
            folder = os.path.join(os.environ['CHATS_FOLDER'], os.environ['CURRENT_CHAT'], 'history', 'audio', 'ai')
            if engine._inLoop:engine.endLoop()
            item:str = QUEUE.get()
            # mp3_path = os.path.join(folder, filename) + '.mp3'
            noisified = llm_parser.getNoises(item)
            for part in noisified:
                if part.startswith('*') and part.lower().find('whir'):
                    _SPEAKING_QUEUE.put(part)
                else:
                    no_asterics=re.sub(r'\*.*\*','',part)
                    if not no_asterics:continue
                    filename = f'''{i}. {no_asterics.replace("$","").replace(".","").replace("!","").replace("?","").replace('"',"").replace("'","").replace(" ","_").replace("..",".").replace('*','+')}'''[:192].replace('\n','')
                    path = os.path.join(folder, filename) + '.wav'
                    engine.save_to_file(part, path)
                    engine.runAndWait()
                    _SPEAKING_QUEUE.put(path)
            i += 1
        time.sleep(0.2)

def addToQueue(item):
    QUEUE.put(item)  # Add item to the shared queue

save_thread=threading.Thread(target=save_to_folder,daemon=True)
save_thread.start()
speak_thread=threading.Thread(target=speak)
speak_thread.start()
print('TTS Initiated')