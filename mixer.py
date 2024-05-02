import subprocess

class Audio:
    def __init__(self,path:str) -> None:
        self.path=path
        self.is_playing=True
        self._process=subprocess.Popen(['ffplay',path,'-autoexit', '-hide_banner', '-loglevel', 'error', '-nodisp'])
    def play(self):
        self._process.send_signal(subprocess.signal.SIGCONT)
        self.is_playing=True
    def pause(self):
        self._process.send_signal(subprocess.signal.SIGSTOP)
        self.is_playing=False
    def stop(self):
        self._process.terminate()
    def wait(self):
        self._process.wait()