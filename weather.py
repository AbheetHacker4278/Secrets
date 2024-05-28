import requests
import speech_recognition as sr
import pyttsx3

def play_beep():
    import platform
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms
    else:
        print("\a")  # ASCII Bell

def speak(text):
    print("Jarvis:", text)
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty("rate", rate - 30)
    engine.say(text)
    engine.runAndWait()

def get_weather(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description'].capitalize()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        country = data['sys']['country']

        speak(f"Weather in {location}, {country}:")
        speak(f"Description: {weather_description}")
        speak(f"Temperature: {temperature}°C")
        speak(f"Humidity: {humidity}%")
        speak(f"Wind Speed: {wind_speed} m/s")
    else:
        speak("Failed to fetch weather data.")

def get_location_from_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say the city, state, or country name.")
        audio = recognizer.listen(source)

    try:
        location = recognizer.recognize_google(audio, language='en-in')
        return location
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the location. Please try again.")
        return None
    except sr.RequestError:
        speak("Sorry, I'm unable to access the Google API. Please try again later.")
        return None
    
def get_location_from_voice2():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Do you want the weather detail of any other geographic location?")
        audio = recognizer.listen(source)

    try:
        location = recognizer.recognize_google(audio, language='en-in')
        return location
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the location. Please try again.")
        return None
    except sr.RequestError:
        speak("Sorry, I'm unable to access the Google API. Please try again later.")
        return None
