import os  # Provides functions to interact with the operating system (e.g., file listing).
import pyttsx3  # Text-to-speech conversion library.
import speech_recognition as sr  # For speech-to-text (voice recognition).
import datetime  # For working with dates and times.
import subprocess  # To run external applications (e.g., open Brave browser).
import urllib.parse  # For encoding URLs and query strings.

# Initialize the text-to-speech engine using the 'sapi5' driver (Windows TTS).
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')  # Get available voices on the system.
engine.setProperty('voice', voices[0].id)  # Set the engine to use the first voice.

def speak(audio):
    """Converts text to speech."""
    engine.say(audio)  # Queue the text to be spoken.
    engine.runAndWait()  # Process the voice queue and speak out loud.

def wishMe():
    """Greets the user based on the current time of day."""
    hour = int(datetime.datetime.now().hour)  # Get current hour (0-23).
    if hour < 12:
        speak("Good Morning Sir!")  # Morning greeting.
    elif hour < 18:
        speak("Good Afternoon Sir!")  # Afternoon greeting.
    else:
        speak("Good Evening Sir!")  # Evening greeting.
    speak("I am JARVIS, your assistant. Please tell me how may I help you.")

def takeCommand():
    """Listens for a command from the microphone and returns it as a string."""
    r = sr.Recognizer()  # Create a new speech recognizer instance.
    with sr.Microphone() as source:  # Use system microphone as the audio source.
        print("Listening...")
        r.pause_threshold = 1  # Waits for 1 second of silence before considering input complete.
        audio = r.listen(source)  # Listen and record the user's speech.

    try:
        print("Recognizing...")
        # Use Google Web Speech API to transcribe audio to text.
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Please say again.")
        return "None"  # Return "None" if speech was not understood.
    return query.lower()  # Return the recognized command in lowercase.

def list_and_play_songs(music_dir):
    """Lists available songs in a directory and lets the user choose one to play."""
    # Collect all .mp3 and .m4a files in the given directory.
    songs = [song for song in os.listdir(music_dir) if song.endswith(('.mp3', '.m4a'))]

    if not songs:
        speak("No songs found in the directory.")
        return

    # Display the list of available songs to the user.
    print("Available songs:")
    for i, song in enumerate(songs):
        print(f"{i + 1}. {song}")

    # Ask the user (via CLI) to select a song by number.
    speak("Please enter the number of the song you want to play.")
    choice = input("Enter the number of the song you want to play: ")

    try:
        song_index = int(choice) - 1  # Convert input to zero-based index.
        if 0 <= song_index < len(songs):
            selected_song = songs[song_index]  # Get the chosen song.
            print(f"Playing: {selected_song}")
            speak(f"Playing {selected_song}")
            # Play the selected song using the default media player.
            os.startfile(os.path.join(music_dir, selected_song))
        else:
            speak("Invalid selection. Please try again.")
    except ValueError:
        speak("Invalid input. Please enter a number.")

def open_in_brave(url):
    """Open a given URL in the Brave browser (new tab)."""
    # Path to Brave browser executable (update if installed elsewhere).
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    if os.path.exists(brave_path):
        # Open the URL in a new Brave tab.
        subprocess.run([brave_path, '--new-tab', url])
    else:
        speak("Brave browser not found. Please check the path.")

def search_in_brave(query):
    """Encodes the search query and opens ChatGPT and Perplexity with the query in Brave."""
    encoded_query = urllib.parse.quote(query)  # URL-encode the search query.
    # Open ChatGPT search page with the query.
    open_in_brave(f"https://chatgpt.com?q={encoded_query}")
    # Open Perplexity search page with the query.
    open_in_brave(f"https://www.perplexity.ai/?q={encoded_query}")

if __name__ == "__main__":
    wishMe()  # Greet the user on startup.
    while True:
        query = takeCommand()  # Listen for a voice command.

        # If the command includes 'search', search using ChatGPT and Perplexity.
        if 'search' in query:
            speak('Searching...')
            query = query.replace("search", "")
            search_in_brave(query)

        # If the command includes 'youtube', search YouTube with the query.
        elif 'youtube' in query:
            query = query.replace("youtube", "")
            open_in_brave(f"https://youtube.com/results?search_query={query}")

        # If the command is 'open google', open Google homepage.
        elif 'open google' in query:
            open_in_brave("https://google.com")

        # If the command is 'stack overflow', open Stack Overflow homepage.
        elif 'stack overflow' in query:
            open_in_brave("https://stackoverflow.com")

        # If the command is 'play music', list and play songs from the specified directory.
        elif 'play music' in query:
            music_dir = 'C:\\Users\\adars\\All Songs'  # Update this path as needed.
            list_and_play_songs(music_dir)
            break  # Exit after playing music.

        # If the command is 'the time', speak the current time.
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        # If the command is 'exit', say goodbye and terminate the program.
        elif 'exit' in query:
            speak("Goodbye! Sir")
            break
