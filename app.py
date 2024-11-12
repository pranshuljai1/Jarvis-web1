from flask import Flask, render_template, request, jsonify
import webbrowser
import os
import datetime
import pyttsx3
import wikipedia
import speech_recognition as sr  # Speech recognition for mic input

app = Flask(__name__)

# Initialize the speech engine for Jarvis to speak
engine = pyttsx3.init()

# Route to handle index page
@app.route('/')
def index():
    return render_template('index.html')

# Greet user based on time
def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# Respond to user with text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Handle Jarvis' greeting when the user opens the site
@app.route('/greet')
def greet():
    greeting = greet_user()
    return jsonify({"greeting": greeting})

# Handle user requests (e.g., song playing, website opening)
@app.route('/command', methods=['POST'])
def handle_command():
    command = request.form['command'].lower()

    # Greet commands
    if 'hi' in command or 'hello' in command:
        greeting = greet_user() + ", Sir! How can I assist you today?"
        speak(greeting)
        return jsonify({"response": greeting})

    # Open websites
    elif 'open instagram' in command:
        webbrowser.open("https://www.instagram.com")
        return jsonify({"response": "Opening Instagram..."})
    elif 'open facebook' in command:
        webbrowser.open("https://www.facebook.com")
        return jsonify({"response": "Opening Facebook..."})

    # Play songs (This is just an example, adjust as needed)
    elif 'play song' in command:
        song_name = command.replace('play song', '').strip()
        song_url = f"https://www.youtube.com/results?search_query={song_name}"
        return jsonify({"response": f"Playing {song_name}", "url": song_url})

    # Wikipedia search
    elif 'tell me about' in command:
        topic = command.replace('tell me about', '').strip()
        try:
            summary = wikipedia.summary(topic, sentences=1)
            return jsonify({"response": summary})
        except wikipedia.exceptions.DisambiguationError as e:
            return jsonify({"response": f"Multiple options found for {topic}. Please be more specific."})

    # Default fallback for unknown commands
    else:
        return jsonify({"response": "Sorry, I didn't understand that."})

# Route to handle mic input (speech recognition)
@app.route('/mic', methods=['POST'])
def mic_input():
    recognizer = sr.Recognizer()

    # Use the microphone for speech recognition
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        return handle_command_for_mic(command)
    except sr.UnknownValueError:
        return jsonify({"response": "Sorry, I couldn't understand that."})
    except sr.RequestError:
        return jsonify({"response": "Sorry, there was an issue with the speech service."})

# Handle mic input command
def handle_command_for_mic(command):
    # Repeat the same logic for mic command as regular command
    return handle_command()

if __name__ == '__main__':
    app.run(debug=True)
