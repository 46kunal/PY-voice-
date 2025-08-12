import speech_recognition as sr
import time
import os
import sys
from gui import launch_gui  # your assistant starts with GUI
from modules.settings import load_settings

settings = load_settings()  # Load settings at startup

WAKE_WORDS = ["hey ", "PieVoice", "hello pie"]

def detect_wake_word(text):
    return any(word in text.lower() for word in WAKE_WORDS)

def passive_listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Running silently... Say 'Hey' to activate.")

        while True:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                speech = recognizer.recognize_google(audio)
                print(f"Heard: {speech}")
                if detect_wake_word(speech):
                    print("Wake word detected. Launching assistant GUI...")
                    return True  # trigger assistant
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("⚠️ Network issue with Speech Recognition API")
                time.sleep(5)

if __name__ == "__main__":
    triggered = passive_listen()
    if triggered:
        launch_gui()  # launches your main assistant