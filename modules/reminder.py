import re
import time
import threading
from modules.speech_engine import speak

reminders = []

def parse_reminder(command):
    match = re.search(r"remind me to (.+) at (\d{1,2})(:(\d{2}))?\s*(am|pm)?", command)
    if not match:
        speak("Sorry, I couldn't understand the time.")
        return

    task = match.group(1).strip()
    hour = int(match.group(2))
    minute = int(match.group(4)) if match.group(4) else 0
    meridian = match.group(5)

    if meridian == "pm" and hour != 12:
        hour += 12
    elif meridian == "am" and hour == 12:
        hour = 0

    reminders.append((task, hour, minute))
    speak(f"Reminder set for {task} at {hour:02d}:{minute:02d}")

def reminder_loop():
    while True:
        now = time.localtime()
        for task, hour, minute in reminders[:]:
            if now.tm_hour == hour and now.tm_min == minute:
                speak(f"This is your reminder: {task}")
                reminders.remove((task, hour, minute))
        time.sleep(30)
