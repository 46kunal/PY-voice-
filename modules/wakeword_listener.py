import speech_recognition as sr
import threading
import time

class WakeWordListener:
    def __init__(self, wake_word, callback):
        self.wake_word = wake_word.lower()
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    print("Wake word listener active...")
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    phrase = self.recognizer.recognize_google(audio).lower()
                    print(f"Wake word listener heard: {phrase}")
                    if self.wake_word in phrase:
                        print("Wake word detected!")
                        if self.callback:
                            self.callback()
                        time.sleep(2)  # pause a bit after wake word detected
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    print("Speech Recognition service error")