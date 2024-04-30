import pyaudio
import wave
import speech_recognition as sr

def record_audio(output_file):
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

        recording_complete()

    except sr.UnknownValueError:
        print("Speech not detected.")

def recording_complete(path):
    pass

if __name__ == "__main__":
    output_file = "output.wav"
    record_audio(output_file)
