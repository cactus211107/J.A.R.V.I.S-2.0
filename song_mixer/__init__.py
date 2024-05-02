import pytube,os
from mixer import Audio

SONG:Audio=None

def download_song(song,filepath,filename:str|None=None):
    result:pytube.YouTube=pytube.Search(song).results[0]
    filename=filename or result.title
    if os.path.exists(os.path.join(filepath,filename)):return
    yt=pytube.YouTube(result.watch_url)
    yt.streams.get_audio_only().download(filepath,filename+'.mp3') 

def startSong(path):
    try:SONG.stop()
    except:0
    SONG=Audio(path)
def pauseSong():
    try:SONG.pause()
    except:0
def playSong():
    try:SONG.play()
    except:0
def stopSong():
    try:SONG.stop()
    except:0
def waitTillSongFinished():
    try:SONG.wait()
    except:0


if __name__ == '__main__':
    download_song('somebody that i used to know','','ahh')