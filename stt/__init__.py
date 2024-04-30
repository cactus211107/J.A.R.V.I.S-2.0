# This is the STT (Speech To Text / Speech Recognition) code
import time
import whisper
model = whisper.load_model("base")
print('Loaded SST Model')
def recognize(file,print_benchmark=False):
    s=time.perf_counter()
    result = model.transcribe(file)
    e=time.perf_counter()
    if print_benchmark:print('Completed Speech Recognition in',e-s,'seconds.')
    return result['text']


# Audio recording code
import wave
import speech_recognition as sr

def record_audio(output_file,benchmark=False):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for speech...")

    with microphone as source:
        audio_stream = recognizer.listen(source)

    print("Processing speech...")

    try:
        # Save recorded audio to WAV file
        with wave.open(output_file, 'wb') as wave_file:
            wave_file.setnchannels(1)  # mono
            wave_file.setsampwidth(2)  # 16-bit
            wave_file.setframerate(44100)
            wave_file.writeframes(audio_stream.get_wav_data())

        return recognize(output_file,benchmark)

    except sr.UnknownValueError:
        print("Speech not detected.")






print(record_audio('test.mp3',True))