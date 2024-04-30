import pyttsx3

engine = pyttsx3.init('nsss')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate/1.25)
print('Default Rate:',rate)
print('Running At Rate:',rate/1.25)
voices = engine.getProperty('voices')


# for voice in voices[107:]:
#     print('Running Voice:',voice.name,'with id:',voice.id)
#     engine.setProperty('voice',voice.id)
#     engine.say('The quick brown fox jumped over the lazy dog.')
#     engine.runAndWait()


voice_candidates=['com.apple.eloquence.en-GB.Grandpa','com.apple.voice.compact.en-GB.Daniel','com.apple.speech.synthesis.voice.Fred','com.apple.eloquence.en-GB.Reed']
#com.apple.eloquence.en-GB.Grandpa
#com.apple.voice.compact.en-GB.Daniel
#com.apple.speech.synthesis.voice.Fred
#com.apple.eloquence.en-GB.Reed

#funny:com.apple.voice.compact.en-IN.Rishi

for voice in voice_candidates:
    engine.setProperty('voice',voice)
    print(engine.getProperty('voice'))
    engine.say('Hi, its me, Jarvis. Your AI assistant here! I would like to say some text!')
    engine.say('You spin me right round baby right round like a record baby')
    engine.say('I dont know man')
    engine.runAndWait()