import multiprocessing
import loding



def speakchild(text):
    import pyttsx3
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[0].id)
    rate=engine.getProperty('rate')
    engine.setProperty("rate",rate-30)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    import struct
    import pyaudio
    import pvporcupine
    import speech_recognition as sr
    from pydub.playback import play
    from pydub import AudioSegment
    import google.generativeai as genai
    import os
    import pyttsx3
    import os
    from dotenv import load_dotenv
    from IPython.display import Markdown
    import textwrap
    import markdown
    from bs4 import BeautifulSoup
    from AppOpener import open as Open,close as Close
    import webbrowser
    from datetime import date,datetime
    import datetime
    import subprocess
    import platform
    import time
    import pyautogui
    import requests
    import signal
    import sys

    load_dotenv()
    porcupine=None
    paud=None
    audio_stream=None
    cp = None
    GOOGLE_API_KEY = "AIzaSyA1n_-a3nzYm1kiLdj8lgRzhX6OSQejkd8"
    genai.configure(api_key=GOOGLE_API_KEY)
    def startsound():
        audio=AudioSegment.from_wav("start up sound.wav")
        play(audio)

    def endsound():
        audio=AudioSegment.from_wav("end up sound.wav")
        play(audio)
    
    def speak(text):
        global cp
        print("Jarvis:",text)
        cp = multiprocessing.Process(target=speakchild,args=(text,))
        cp.start()
        
    def to_text(text):
        text = text.replace('•', '  *')
        md = Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
        html_text = markdown.markdown(md.data)
        text = "".join(BeautifulSoup(html_text,"html.parser").findAll(text=True))
        return text

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    if not os.path.exists('chose.txt'):
        f = open("chose.txt", 'w')
        f.write('0')
        f.close()
    
    if not os.path.exists(os.path.join('outputhistory/')):
        os.mkdir(os.path.join('outputhistory/'))

    def security_check():
        speak("Security Check is starting , it may take a few seconds")
        loding.main()
        open_settings_command = "start windowsdefender://threat"
        os.system(open_settings_command)
        powershell_command = "powershell -Command \"Start-MpScan -ScanType QuickScan\""
        subprocess.run(powershell_command, shell=True)
        powershell_report_command = "powershell -Command \"Get-MpThreatDetection\""
        result = subprocess.run(powershell_report_command, shell=True, capture_output=True, text=True)
        speak("Security check completed.")

        if result.returncode == 0:
            threats = result.stdout.strip()
            if threats:
                speak(f"Threat report: {threats}")
            else:
                speak("No threats found.")
        else:
            speak("Failed to retrieve threat report.")

    def main():
        # Open a new terminal window for user input
        subprocess.Popen(['start', 'cmd', '/k', 'python', 'timee.py'], shell=True)


    def open_notepad(text=None):
        # Correct path to Notepad
        speak("Okay Boss, Opening Notepad")
        subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])
        
        # Wait for Notepad to open
        time.sleep(2)
        
        if text:
            # Type the text
            pyautogui.typewrite(text)
        
    
    def wishme():
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            speak("Good Morning Boss, how may I help you today?")
        elif 12 <= hour < 18:
            speak("Good Afternoon Boss, how may I help you today?")
        else:
            speak("Good Evening Boss, how may I help you today?")

    wishme()

    def terminate_processes(signal_number, frame):
        print("Terminating processes...")
        if cp is not None:
            cp.terminate()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, terminate_processes)
    signal.signal(signal.SIGTERM, terminate_processes)

    def jarvis_brain(text):
        print(chat.history)
        q = text.split(" ")
        if q[0] == "open":
            if text == 'open youtube':
                speak("Boss, can you please tell me about the topic that you want to play?")
                recognize = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = recognize.listen(source)
                try:
                    topic = recognize.recognize_google(audio, language='en-in')
                    print("Topic:", topic)
                    webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
                    speak(f"Opening YouTube and searching for {topic}")
                except Exception as e:
                    print(e)
                    speak("Sorry, I couldn't understand the topic.")
            else:
                Open(" ".join(q[1:]), match_closest=True)
                speak(f'opening {" ".join(q[1:])}')
        
        elif q[0] == "close":
            Close(" ".join(q[1:]), match_closest=True)
            speak(f'closing {" ".join(q[1:])}')
        
        elif text == "open notepad":
            open_notepad()
        elif text == "write something on notepad":
            text_to_write = speak()
            if text_to_write:
                open_notepad(text_to_write)
        elif text == 'play music':
            file = open("chose.txt", 'r')
            chose = file.readlines()
            chose = int(chose[0])
            m = 'e:\\songs'
            song = os.listdir(m)
            length = len(song)
            speak("now music is playing")
            os.startfile(os.path.join(m, song[chose]))
            chose += 1
            file = open("chose.txt", 'w')
            file.write(str(chose))
            file.close()
        elif text == 'next':
            file = open("chose.txt", 'r')
            chose = file.readlines()
            chose = int(chose[0])
            m = 'e:\\songs'
            song = os.listdir(m)
            length = len(song)
            if chose >= length:
                speak("no more music to next")
                speak("i'm playing music from starting")
                chose = 0
                os.startfile(os.path.join(m, song[chose]))
            else:
                os.startfile(os.path.join(m, song[chose]))
                chose += 1
            file = open("chose.txt", 'w')
            file.write(str(chose))
            file.close()
        elif text == "run security check":
            security_check()
        
        elif text == "run firewall in graphical mode":
            import firewall

        elif text == "timer chalu karo":
            main()

        elif text == "shutdown":
            cp = None
            try:
                speak("Shutting down. Goodbye, Boss!")
                multiprocessing.freeze_support()
                # Your main logic here
            except KeyboardInterrupt:
                terminate_processes(None, None)
            finally:
                terminate_processes(None, None)
            
        elif text == "check climate condition":
            speak("Boss")
            import weather
            api_key = "da7fcfac8bffd01e83fcd97fd91d4c9e" 
            while True:
                location = weather.get_location_from_voice()
                if location:
                    weather.get_weather(api_key, location)
                    choice = weather.get_location_from_voice2().lower()
                    if choice == "terminate" or choice == "no":
                        speak("Terminating the weather check process. Goodbye!")
                        break
                    elif choice == "yes":
                        location = weather.get_location_from_voice()
                else:
                    speak("Boss, Maybe you said the wrong city name")
                    weather.play_beep()  # Play beep if location input fails

        elif text == 'stop music':
            speak('ok boss')
            speak("now I stop music")
            os.system('taskkill /F /FI "WINDOWTITLE eq Media Player" ')
            
        else:
            response = chat.send_message(text)
            responsetext = to_text(response.text)
            speak(responsetext)
            todaydate = date.today()
            if not os.path.exists(f'outputhistory/{todaydate}'):
                os.mkdir(f'outputhistory/{todaydate}')
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            f = open(os.path.join(f'outputhistory/{todaydate}/', f'{current_time}.txt'), 'w')
            f.writelines(responsetext)
            f.close()


    try:
       
        print(pvporcupine.KEYWORDS)
        porcupine=pvporcupine.create(keywords=["jarvis"]) #pvporcupine.KEYWORDS for all keywords
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
            keyword_index=porcupine.process(keyword)
            if keyword_index>=0:
                print("hotword detected")
                startsound()
                if cp:
                    cp.kill()
                recognize=sr.Recognizer()
                with sr.Microphone() as source:
                    audio=recognize.listen(source)
                    endsound()
                try:
                    query=recognize.recognize_google(audio,language='en-in')
                    print(query)
                    query = str(query).lower()
                    if query != " " and query != "":
                        jarvis_brain(query)
                        
                except Exception as e:
                    print(e)
                    pass

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

