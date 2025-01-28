import os
import pyttsx3
import speech_recognition as sr  # For adding voice interaction if required
import datetime
import subprocess  # For opening Brave with arguments
import urllib.parse  # For URL encoding

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to the first voice

def speak(audio):
    """Converts text to speech."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("I am JARVIS, your assistant. Please tell me how may I help you.")

def takeCommand():
    """Listens for a command and returns it as a string."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Please say again.")
        return "None"
    return query.lower()  # Return the recognized command in lowercase

def list_and_play_songs(music_dir):
    """Lists available songs and allows the user to choose one to play."""
    # List only .mp3 and .m4a files
    songs = [song for song in os.listdir(music_dir) if song.endswith(('.mp3', '.m4a'))]

    if not songs:
        speak("No songs found in the directory.")
        return

    # Display available songs
    print("Available songs:")
    for i, song in enumerate(songs):
        print(f"{i + 1}. {song}")

    # Ask the user to choose a song
    speak("Please enter the number of the song you want to play.")
    choice = input("Enter the number of the song you want to play: ")

    try:
        song_index = int(choice) - 1
        if 0 <= song_index < len(songs):
            selected_song = songs[song_index]
            print(f"Playing: {selected_song}")
            speak(f"Playing {selected_song}")
            os.startfile(os.path.join(music_dir, selected_song))  # Play the selected song
        else:
            speak("Invalid selection. Please try again.")
    except ValueError:
        speak("Invalid input. Please enter a number.")

def open_in_brave(url):
    """Open a URL in Brave browser."""
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Update the path if needed
    if os.path.exists(brave_path):
        subprocess.run([brave_path, '--new-tab', url])  # Use subprocess to pass arguments
    else:
        speak("Brave browser not found. Please check the path.")

def search_in_brave(query):
    """Encodes query and opens the search results in Brave."""
    # URL-encode the query
    encoded_query = urllib.parse.quote(query)
    
    # Construct the URL for ChatGPT and Perplexity
    open_in_brave(f"https://chatgpt.com?q={encoded_query}")
    open_in_brave(f"https://www.perplexity.ai/?q={encoded_query}")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        # Search Google instead of Wikipedia
        if 'search' in query:
            speak('Searching...')
            query = query.replace("search", "")
            search_in_brave(query)  # Use the new search function

        elif 'youtube' in query:
            query = query.replace("youtube", "")
            open_in_brave(f"https://youtube.com/results?search_query={query}")

        elif 'open google' in query:
            open_in_brave("https://google.com")

        elif 'stack overflow' in query:
            open_in_brave("https://stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\adars\\All Songs'  # Update this with your music directory path
            list_and_play_songs(music_dir)
            break

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            
        elif 'exit' in query:
            speak("Goodbye! Sir")
            break
