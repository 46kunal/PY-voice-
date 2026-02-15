🎙️ PY-Voice — AI Based Voice Assistant

An AI-powered voice assistant built using Python that can understand voice commands and perform various automated tasks.

🚀 Features

🎤 Voice Recognition

🗣️ Text-to-Speech Response

🌐 Web Search Integration

📂 Open Applications via Voice

⏰ Tell Time and Date

💻 Basic System Commands

🎨 Simple GUI Interface (if using gui.py)

🛠️ Tech Stack

Python 3.x

speech_recognition

pyttsx3

os

datetime

webbrowser

tkinter (for GUI)

📂 Project Structure
PY-voice/
│
├── main.py           # Main execution file
├── config.py         # Configuration settings
├── gui.py            # GUI implementation
├── settings.json     # Assistant settings
├── modules/          # Custom modules
├── build/            # Build files
├── dist/             # Distribution files
└── README.md         # Project Documentation

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/46kunal/PY-voice-.git
cd PY-voice-

2️⃣ Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows

3️⃣ Install Required Libraries
pip install speechrecognition pyttsx3 pyaudio


If pyaudio fails on Windows:

pip install pipwin
pipwin install pyaudio

▶️ How to Run
python main.py


If using GUI:

python gui.py
