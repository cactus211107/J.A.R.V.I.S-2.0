import subprocess,requests,time
subprocess.call('open /Applications/Ollama.app',shell=True)
print('Waiting For Ollama to start.')
while True:
	try:
		if requests.get('http://localhost:11434/api/tags').status_code == 200:
			break
	except:pass
	time.sleep(0.5)
print('Successfully running Ollama')
subprocess.call('open "/Applications/Visual Studio Code.app"',shell=True)