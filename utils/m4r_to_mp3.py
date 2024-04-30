import os,subprocess
os.chdir('./media/audio/alerts')
files = os.listdir()
# convert:
for file in files:
    subprocess.call(f'ffmpeg -i "{file}" "{file.split(".")[0]}".mp3',shell=True)

# remove:
files = os.listdir()
for file in files:
    if file.endswith('.m4r'):
       os.remove(file)

# remove "-EncoreInfinitum" from files
files = os.listdir()
for file in files:
    os.rename(file,file.replace("-EncoreInfinitum",''))

"""Now nothing here is used bc it is not needed anymore. But i will keep it anyways"""