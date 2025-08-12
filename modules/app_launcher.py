import subprocess
import webbrowser
import os
from modules.speech_engine import speak

def open_application(command):
    if "open chrome" in command:
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        speak("Opening Chrome")
        return True
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        return True
    elif "spotify" in command:
        path = r"C:\Users\YourUsername\AppData\Roaming\Spotify\Spotify.exe"
        if os.path.exists(path):
            subprocess.Popen(path)
            speak("Opening Spotify")
        else:
            speak("Spotify is not installed or the path is incorrect.")
        return True
    elif "file explorer" in command:
        subprocess.Popen("explorer.exe")
        speak("Opening File Explorer")
        return True
    return False
