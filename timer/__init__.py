import threading
import time,subprocess
def play_audio(file_path:str,graphics:bool=False):subprocess.call(f'ffplay "{file_path}" -noborder -autoexit {"-showmode 1" if graphics else "-nodisp"}',shell=True)
TIMERS = []
ALARM = 'Alert'

def format_duration(duration_seconds:float,plural:bool=False) -> str:
    days = duration_seconds//86400
    duration_seconds-=days*86400
    hours = duration_seconds//3600
    duration_seconds-=hours*3600
    minutes = duration_seconds//60
    seconds=duration_seconds%60
    return_string=f'{days} day{"s" if plural and days!=1 else ""} ' if days else ''
    return_string+=f'{hours} hour{"s" if plural and hours!=1 else ""} ' if hours else ''
    return_string+=f'{minutes} minute{"s" if plural and minutes!=1 else ""} ' if minutes else ''
    return_string+=f'{seconds} second{"s" if plural and seconds!=1 else ""} '
    return return_string


def createTimer(seconds:float,name:str|None=None) -> None:
    name=(name or format_duration(seconds)[:-1])
    name+='' if name.endswith('timer') else ' timer'
    TIMERS.append({
        "name":name,
        "duration":seconds,
        "start":time.time()
    })

def clearTimer(name:str) -> None:
    TIMERS.sort(key=lambda x:int(x['name']==name+('' if name.endswith('timer') else ' timer')))
    TIMERS.pop()

def activateTimers() -> None:
    while True:
        for timer in TIMERS:
            if timer['start']+timer['duration'] >= time.time():
                clearTimer(timer['name'])
                play_audio(f'media/audio/alerts/{ALARM}.mp3')
            time.sleep(0.5)
timer_thread = threading.Thread(target=activateTimers)