import pyttsx3
import speech_recognition as sr
import threading
from modules.settings import load_settings

settings = load_settings()
engine = pyttsx3.init()
engine.setProperty('rate', settings["settings"].get("voice_rate", 180))
engine.setProperty('volume', settings["settings"].get("volume", 1.0))

voices = engine.getProperty('voices')
if settings["settings"].get("voice_type", "default") != "default":
    engine.setProperty('voice', voices[1].id if settings["settings"]["voice_type"] == "female" else voices[0].id)

_speak_lock = threading.Lock()
_speaking_thread = None
_stop_flag = False


def _speak_text(text, callback):
    global _stop_flag
    with _speak_lock:
        if _stop_flag:
            return
        _stop_flag = False
        engine.say(text)
        engine.runAndWait()
        if callback and not _stop_flag:
            callback()


def speak(text, callback=None):
    global _speaking_thread
    stop_speaking()  # ensure previous speech is stopped
    _speaking_thread = threading.Thread(target=_speak_text, args=(text, callback), daemon=True)
    _speaking_thread.start()


def stop_speaking():
    global _stop_flag
    with _speak_lock:
        _stop_flag = True
        engine.stop()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not get that.")
        return ""
    except sr.RequestError:
        print("Could not request results from Speech Recognition service")
        return ""
