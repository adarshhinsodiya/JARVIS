# JARVIS - Your Voice Controlled Python Assistant

JARVIS is a simple, voice-controlled desktop assistant written in Python. It can greet you based on the time of day, recognize your voice commands, search the web, play music from your local library, and more. The assistant uses text-to-speech (TTS) and speech recognition to interact with you, providing a hands-free experience.

---

## Features

- **Voice Recognition:** Listens for your commands using your system microphone.
- **Text-to-Speech:** Responds via speech using system-installed voices.
- **Web Search:** Searches using ChatGPT and Perplexity or opens websites like Google, YouTube, and Stack Overflow in the Brave browser.
- **Music Player:** Lists and plays songs from your local directory.
- **Time Announcement:** Tells you the current time.
- **Custom Greetings:** Greets you based on the time of day.
- **Command-Line Selection:** Lets you select songs from the terminal interface.

---

## Requirements

- Python 3.7+
- Windows OS (due to `sapi5` voice engine and Brave browser path defaults)
- Brave browser installed (adjust the path as needed)
- Microphone connected

### Python Dependencies

Install via pip:
```bash
pip install pyttsx3 SpeechRecognition