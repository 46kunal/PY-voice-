import re
from modules.speech_engine import speak, listen, stop_speaking
from modules.weather import get_weather
from modules.wiki_lookup import get_wikipedia_summary
from modules.app_launcher import open_application
from modules.ai_chat import get_deepinfra_response

def process_voice_command(command, log_callback=None):
    if not command:
        return

    if log_callback:
        log_callback(f"You: {command}")

    if "exit" in command or "stop" in command:
        speak("Goodbye!")
        if log_callback:
            log_callback("Assistant: Goodbye!")
        return "exit"

    if "stop speaking" in command:
        stop_speaking()
        if log_callback:
            log_callback("Assistant: Stopped speaking as requested.")
        return

    if "weather" in command:
        city = "Pune"
        match = re.search(r"in\s+([a-zA-Z\s]+)", command)
        if match:
            city = match.group(1).strip()
        weather_info = get_weather(city)
        speak(weather_info)
        if log_callback:
            log_callback(f"Assistant: {weather_info}")
        return

    if "wikipedia" in command or "who is" in command or "what is" in command:
        topic = command.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        if topic:
            summary = get_wikipedia_summary(topic)
            speak(summary)
            if log_callback:
                log_callback(f"Assistant: {summary}")
        else:
            speak("Please specify a topic.")
            if log_callback:
                log_callback("Assistant: Please specify a topic.")
        return

    if open_application(command):
        if log_callback:
            log_callback("Assistant: Application opened.")
        return

    # fallback AI chatbot response
    response = get_deepinfra_response(command)
    speak(response)
    if log_callback:
        log_callback(f"Assistant: {response}")
