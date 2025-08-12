import json
import os

def resource_path(relative_path):
    """ Cross-platform path in user's home directory """
    return os.path.join(os.path.expanduser("~"), ".pievoice", relative_path)

SETTINGS_FILE = resource_path("settings.json")

# Ensure directory exists
os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

def get_default_settings():
    return {
        "voice": {"rate": 180, "voice_type": "default"},
        "wake_word": "hey Pie",
        "theme": "superhero",
        "auto_listen": True,
        "startup": {
            "start_minimized": True,
            "start_in_background": True
        },
        "assistant": {
            "greetings": True,
            "confirmations": True
        },
        "privacy": {
            "log_commands": False,
            "mic_access": True
        },
        "settings": {
            "volume": 1.0,
            "language": "en",
            "theme_color": "light",
            "voice_rate": 180,
            "voice_type": "default",
            "auto_listen": True
        }
    }

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(get_default_settings())
    with open(SETTINGS_FILE, "r") as file:
        return json.load(file)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(data, file, indent=4)
