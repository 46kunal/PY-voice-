import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext, messagebox
import threading
import speech_recognition as sr
import time
from modules.speech_engine import speak, stop_speaking
from modules.voice_assistant import process_voice_command
from modules.settings import load_settings, save_settings
from modules.wakeword_listener import WakeWordListener

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyVoice")
        self.root.state('zoomed')  # Fullscreen
        self.root.resizable(True, True)

        self.settings = load_settings()

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.header = ttk.Label(
            self.main_frame,
            text="🤖 PYVoice Assistant",
            font=("Segoe UI", 18, "bold"),
            bootstyle="primary inverse"
        )
        self.header.pack(fill=X, pady=(0, 10))

        self.chat_log = scrolledtext.ScrolledText(
            self.main_frame,
            wrap="word",
            font=("Segoe UI", 11),
            height=20,
            state="disabled",
            background="#f8f9fa"
        )
        self.chat_log.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.typing_indicator = ttk.Label(
            self.main_frame,
            text="",
            font=("Segoe UI", 10, "italic"),
            bootstyle="info"
        )
        self.typing_indicator.pack(anchor="w", padx=12)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=X, pady=10)

        self.listen_btn = ttk.Button(
            self.input_frame,
            text="🎙️ Listen",
            bootstyle="success",
            command=self.start_listening_thread,
            width=20
        )
        self.listen_btn.pack(side=LEFT, padx=(10, 5))

        self.stop_btn = ttk.Button(
            self.input_frame,
            text="🛑 Stop Speaking",
            bootstyle="danger",
            command=self.handle_stop_speaking,
            width=20
        )
        self.stop_btn.pack(side=LEFT, padx=(5, 10))

        self.user_entry = ttk.Entry(self.input_frame, font=("Segoe UI", 11))
        self.user_entry.focus_set()
        self.user_entry.pack(side=LEFT, fill=X, expand=True, padx=(10, 5))
        self.user_entry.bind("<Return>", self.handle_text_input)

        self.send_btn = ttk.Button(
            self.input_frame,
            text="📤 Send",
            bootstyle="info",
            command=self.handle_text_input
        )
        self.send_btn.pack(side=LEFT, padx=(5, 10))

        self.log("Assistant: Hello ! Your PyVoice assistant is ready.")
        speak("Hello! Your PyVoice assistant is ready.")

        # Initialize and start wake word listener
        self.wake_listener = WakeWordListener(wake_word=self.settings["wake_word"], callback=self.on_wake_word_detected)
        self.wake_listener.start()

        # Handle window close event to stop background threads cleanly
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Settings Button
        self.settings_btn = ttk.Button(
            self.input_frame,
            text="⚙️ Settings",
            bootstyle="warning",
            command=self.open_settings,
            width=20
        )
        self.settings_btn.pack(side=LEFT, padx=(5, 10))

    def log(self, text):
        self.chat_log.configure(state="normal")
        self.chat_log.insert("end", f"{text}\n")
        self.chat_log.configure(state="disabled")
        self.chat_log.see("end")

    def set_typing(self, status=True):
        self.typing_indicator.config(text="Assistant is typing..." if status else "")

    def start_listening_thread(self):
        self.log("🎙️ Listening...")
        thread = threading.Thread(target=self.handle_command, daemon=True)
        thread.start()

    def handle_command(self):
        self.set_typing(True)
        from modules.speech_engine import listen  # local import to avoid previous import issues
        command = listen()
        if not command:
            self.log("Assistant: Sorry, I didn't catch that.")
            self.set_typing(False)
            return
        result = process_voice_command(command, self.log)
        self.set_typing(False)
        if result == "exit":
            self.on_close()

    def handle_text_input(self, event=None):
        user_input = self.user_entry.get().strip()
        if user_input:
            self.log(f"You: {user_input}")
            self.user_entry.delete(0, "end")
            self.set_typing(True)
            thread = threading.Thread(target=self.process_text_command, args=(user_input,), daemon=True)
            thread.start()

    def process_text_command(self, text):
        result = process_voice_command(text, self.log)
        self.set_typing(False)
        if result == "exit":
            self.on_close()

    def handle_stop_speaking(self):
        print("Stop button clicked")  # Debug print
        stop_speaking()
        self.log("🛑 Assistant stopped speaking.")

    def on_wake_word_detected(self):
        self.log("🔊 Wake word detected! Listening for command...")
        threading.Thread(target=self.handle_command, daemon=True).start()

    def on_close(self):
        self.wake_listener.stop()
        self.root.destroy()

    def open_settings(self):
        settings_window = ttk.Window(title="Settings", themename="superhero")
        settings_window.geometry("400x400")

        volume_label = ttk.Label(settings_window, text="Volume:")
        volume_label.pack(pady=5)
        volume_scale = ttk.Scale(settings_window, from_=0.0, to=1.0, orient="horizontal", value=self.settings["settings"]["volume"])
        volume_scale.pack(pady=5)

        language_label = ttk.Label(settings_window, text="Language:")
        language_label.pack(pady=5)
        language_var = ttk.StringVar(value=self.settings["settings"]["language"])
        language_menu = ttk.OptionMenu(settings_window, language_var, "en", "en", "es", "fr")
        language_menu.pack(pady=5)

        theme_color_label = ttk.Label(settings_window, text="Theme Color:")
        theme_color_label.pack(pady=5)
        theme_color_var = ttk.StringVar(value=self.settings["settings"]["theme_color"])
        theme_color_menu = ttk.OptionMenu(settings_window, theme_color_var, "light", "light", "dark")
        theme_color_menu.pack(pady=5)

        voice_rate_label = ttk.Label(settings_window, text="Voice Rate:")
        voice_rate_label.pack(pady=5)
        voice_rate_scale = ttk.Scale(settings_window, from_=100, to=300, orient="horizontal", value=self.settings["settings"]["voice_rate"])
        voice_rate_scale.pack(pady=5)

        voice_type_label = ttk.Label(settings_window, text="Voice Type:")
        voice_type_label.pack(pady=5)
        voice_type_var = ttk.StringVar(value=self.settings["settings"]["voice_type"])
        voice_type_menu = ttk.OptionMenu(settings_window, voice_type_var, "default", "default", "female", "male")
        voice_type_menu.pack(pady=5)

        auto_listen_label = ttk.Label(settings_window, text="Auto-Listen:")
        auto_listen_label.pack(pady=5)
        auto_listen_var = ttk.BooleanVar(value=self.settings["settings"]["auto_listen"])
        auto_listen_checkbox = ttk.Checkbutton(settings_window, text="Enable Auto-Listen", variable=auto_listen_var)
        auto_listen_checkbox.pack(pady=5)

        wake_word_label = ttk.Label(settings_window, text="Wake Word:")
        wake_word_label.pack(pady=5)
        wake_word_entry = ttk.Entry(settings_window)
        wake_word_entry.insert(0, self.settings["wake_word"])
        wake_word_entry.pack(pady=5)

        save_button = ttk.Button(settings_window, text="Save", command=lambda: self.save_settings(
            volume_scale.get(),
            language_var.get(),
            theme_color_var.get(),
            voice_rate_scale.get(),
            voice_type_var.get(),
            auto_listen_var.get(),
            wake_word_entry.get()
        ))
        save_button.pack(pady=10)

        settings_window.mainloop()

    def save_settings(self, volume, language, theme_color, voice_rate, voice_type, auto_listen, wake_word):
        self.settings["settings"]["volume"] = volume
        self.settings["settings"]["language"] = language
        self.settings["settings"]["theme_color"] = theme_color
        self.settings["settings"]["voice_rate"] = voice_rate
        self.settings["settings"]["voice_type"] = voice_type
        self.settings["settings"]["auto_listen"] = auto_listen
        self.settings["wake_word"] = wake_word
        save_settings(self.settings)
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.root.destroy()

def launch_gui():
    app = ttk.Window(themename="superhero")
    AssistantGUI(app)
    app.mainloop()
