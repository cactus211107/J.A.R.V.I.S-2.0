if __name__!='__main__':quit(69)
import time,json,subprocess,os,sys,datetime,whisper,wave,speech_recognition as sr
# subprocess.call('pip install pyaudio',shell=True)
os.makedirs('media/downloaded/audio',exist_ok=True)
os.environ['AUDIO_FOLDER']='media/audio'
os.environ['GENERATED_FOLDER']='media/generated'
os.environ['SPEECH_TO_TEXT']='stt/model'
os.environ['CHATS_FOLDER']='media/chats'
os.environ['BASE_LLM']='llama3:8b' # llama3:8b is good aswell
os.environ['PARSER_MODEL']='llama2:13b'
os.environ['CURRENT_CHAT']=''
os.environ['STATE']='loading'
os.environ['CODE_FOLDER']=os.path.join(os.path.expanduser('~'),'Desktop','Code')

# Run options
SILENT=False
TTS_ENABLED = not SILENT
MODE = 'TEXT' if SILENT else 'SPEECH' # TEXT / SPEECH | Text Mode: You write the prompt in the terminal. Speech Mode: You speak the prompt outloud.
# you can change the modes above ^^^^^^^ by doing vvvvv
# TTS_ENABLED = True
# MODE = 'TEXT'

AUTOSTART = False # Prompts you to press the enter key (just calls an input function) to start JARVIS
CLEAR_CONSOLE = True # Just asthetics. if you want to clear the console at the start of the chat
ENGERGY_THRESHOLD = 1200 # Increase to at least 1000 when in a loud environment


import llm,llm.run_ollama,llm_parser,llm_parser.function_parser,timer,song_mixer # my libraries
if TTS_ENABLED:import tts # Elminates the tts library if TTS is not wanted

def addNewSentencesToQueue(new:list[str],old:list[str]):
    if TTS_ENABLED:[tts.addToQueue(item) for item in new[len(old):]]
    return new[len(new)-len(old):]
def handleResponse(response:llm.requests.Request):
    os.environ['STATE']='generating'
    response_text = ''
    sentences=[]
    old_sentences=[]
    words=[]
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                CHUNK=json.loads(chunk)['message']['content']
                print(CHUNK,end='')
                sys.stdout.flush()
                response_text+=CHUNK
                response_text=response_text.replace('[INST]','').replace('[/INST]','')
                words=response_text.split(' ')
                # renderer.setWordList(words)
                sentences = llm_parser.getSentences(response_text)
                if sentences!=old_sentences:addNewSentencesToQueue(sentences,old_sentences)
                old_sentences=sentences
    os.environ['STATE']='generating finished'
    """
    ChatGPT has >150 billion parameters vs Me ≈ 8-13 billion parameters
    """
    print('\nProcessing Response...')
    keywords = ['app','open','timer','searching','airplay','screen mirror','boot','load','launching','code project','coding','song','play']
    if True in [keyword in response_text.lower() for keyword in keywords]:
        print('Keyword Detected')
        parsed_response:list[dict] = llm_parser.function_parser.parse_response(response_text)
        print(parsed_response)
        for response in parsed_response:
            try:
                action = response.get('action')
                content = response.get('content')
                if action == 'timer':
                    timer_seconds = int(response['content'])
                    name = content
                    timer.createTimer(timer_seconds,name)
                    if TTS_ENABLED:tts.addToQueue(f'Setting {name} timer for {timer.format_duration(timer_seconds,True)}')
                if action == 'timer_stop':
                    timer_name = content
                    try:timer_name=timer.format_duration(int(timer_name))
                    except:pass
                    timer.clearTimer(timer_name)
                    tts.addToQueue(f'Clearing your {timer_name} timer sir.'.replace('  ',' '))
                if action == 'app':
                    app = content
                    process = subprocess.Popen(f'open -a "{app}"',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    out, err = process.communicate()
                    # if process.returncode != 0:tts.addToQueue(f"Sorry Sir, but I couldn't find {app}. Try giving me the full name of the app.")
                if action == 'search': # disabled for now (when i asked about something. it was lazy and just made me search)
                    query = content
                    if TTS_ENABLED:tts.addToQueue(f'Searching For "{query}"')
                    subprocess.call(f'open -a "Microsoft Edge.app" "{"https://google.com/search?q="+query}"',shell=True)
                if action == 'code_project':
                    project_name=content
                    path=os.path.join(os.environ['CODE_FOLDER'],str(project_name))
                    os.makedirs(path,exist_ok=True)
                    subprocess.call(f'code "{path}" -n',shell=True)
                if action == 'play_song':
                    song_name = content
                    if TTS_ENABLED:tts.addToQueue('Hold on while I download the song...')
                    song_mixer.stopSong()
                    song_mixer.download_song(song_name,'media/downloaded/audio',song_name)
                    song_mixer.startSong(os.path.join('media/downloaded/audio',song_name+'.mp3'))
                    os.environ['STATE']='playing song'
                    # song_mixer.waitTillSongFinished()
                    # if TTS_ENABLED:tts.addToQueue('Hope you enjoyed the song sir.')
                    # time.sleep(4)
                    # os.environ['STATE']='listening'
            except:0
                
    
    else:
        print('Keyword Not Detected. Potentially overlooking an action.')
    # if action == 'airplay':
    #     device=action_text
    #     # airplay.\
    llm.addMessageToChat({
        "role":"assistant",
        "content":response_text
    },os.environ['CURRENT_CHAT'])

llm.createJARVISModel()
llm.deleteAllChats()

chat = llm.createChat()
llm.initiateChat(chat)

if not AUTOSTART:input("Press Enter To Continue To JARVIS\n")
os.environ['STATE']='loaded'
if MODE == 'SPEECH':
    # This is the STT (Speech To Text / Speech Recognition) code
    print('Loading SST Model')
    model = whisper.load_model("base")
    print('Loaded SST Model')
    def recognize(file:str,print_benchmark:bool=False):
        s=time.perf_counter()
        result = model.transcribe(file)
        e=time.perf_counter()
        if print_benchmark:print('Completed Speech Recognition in',e-s,'seconds.')
        return result['text']
    def record_audio(output_file:str,benchmark:bool=False):
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = ENGERGY_THRESHOLD
        microphone = sr.Microphone()
        print("Listening for speech...")
        with microphone as source:audio_stream = recognizer.listen(source)
        print("Processing speech...")
        try:# Save recorded audio to WAV file
            with wave.open(output_file, 'wb') as wave_file:
                wave_file.setnchannels(1)  # mono
                wave_file.setsampwidth(2)  # 16-bit
                wave_file.setframerate(44100)
                wave_file.writeframes(audio_stream.get_wav_data())
            return recognize(output_file,benchmark)
        except sr.UnknownValueError:print("Speech not detected.")
    if CLEAR_CONSOLE:os.system('cls' if os.name == 'nt' else 'clear')
    print("Running JARVIS Speech Mode")
    os.environ['STATE']='listening'
    while True:
        if os.environ['STATE'] == 'listening':
            time.sleep(1) # just some time for the human to understand
            prompt = record_audio(os.path.join(os.environ['CHATS_FOLDER'],os.environ['CURRENT_CHAT'],'history','audio','human',str(datetime.datetime.now())+'.wav'))
            if len(prompt)>0:
                print('You:',prompt)
                response = handleResponse(llm.interact(prompt,chat))
if MODE == 'TEXT':
    if CLEAR_CONSOLE:os.system('cls' if os.name == 'nt' else 'clear')
    print("Running JARVIS Text Mode")
    while True:
        prompt=input('Write a prompt: ')
        response=handleResponse(llm.interact(prompt,chat))
        print('\n')
