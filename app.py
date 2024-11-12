import pyttsx3  # For text-to-speech
import wikipedia  # For fetching information from Wikipedia
import webbrowser  # To open websites
import datetime  # For date and time functionality
import speech_recognition as sr  # For speech recognition (if you still want to use mic input)
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Initialize pyttsx3 engine (text-to-speech)
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Greet the user when they visit the app
@app.route('/')
def index():
    return render_template('index.html')

# Handle text-based commands
@app.route('/command', methods=['POST'])
def command():
    user_input = request.form['user_input'].lower()

    if 'hello' in user_input or 'hi' in user_input:
        speak("Hi boss, how can I assist you today?")
        return render_template('index.html', response="Hi boss, how can I assist you today?")
    
    elif 'who is your creator' in user_input:
        speak("My creator is Pranshul Jain.")
        return render_template('index.html', response="My creator is Pranshul Jain.")
    
    elif 'what is the date today' in user_input:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {today}.")
        return render_template('index.html', response=f"Today is {today}.")
    
    elif 'open' in user_input:
        if 'instagram' in user_input:
            webbrowser.open('https://www.instagram.com')
            speak("Opening Instagram.")
            return render_template('index.html', response="Opening Instagram.")
        elif 'facebook' in user_input:
            webbrowser.open('https://www.facebook.com')
            speak("Opening Facebook.")
            return render_template('index.html', response="Opening Facebook.")
    
    elif 'wikipedia' in user_input:
        topic = user_input.replace('wikipedia', '').strip()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
            return render_template('index.html', response=summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Could you please be more specific?")
            return render_template('index.html', response="There are multiple results. Could you please be more specific?")
        except wikipedia.exceptions.HTTPTimeoutError:
            speak("Sorry, I couldn't retrieve the information from Wikipedia. Please try again later.")
            return render_template('index.html', response="Sorry, I couldn't retrieve the information from Wikipedia. Please try again later.")
    
    else:
        speak("Sorry, I didn't understand that command.")
        return render_template('index.html', response="Sorry, I didn't understand that command.")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
