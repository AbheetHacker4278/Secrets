import multiprocessing


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
    import subprocess
    import platform
    import time
    import pyautogui
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

    # def run_django_app():
    #     speak("Starting Django Server.")
    #     os.chdir('C:/Users/Abheet seth/Desktop/deep/Deepfake_detection_using_deep_learning/Django Application')
    #     subprocess.Popen(['start', 'cmd', '/k', 'python', 'manage.py', 'runserver'], shell=True)
    #     webbrowser.open("http://127.0.0.1:8000/")


    def security_check():
        speak("Security Check is starting , it may take a few seconds")
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



    def open_notepad(text=None):
        # Correct path to Notepad
        speak("Okay Boss, Opening Notepad")
        subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])
        
        # Wait for Notepad to open
        time.sleep(2)
        
        if text:
            # Type the text
            pyautogui.typewrite(text)
        
    def jarvis_brain(text):
        print(chat.history)
        q = text.split(" ")
        if q[0] == "open":
            if text=='open youtube':
                        webbrowser.open("https://www.youtube.com/")
                        speak("opening youtube")
            else:
                Open(" ".join(q[1::]),match_closest=True)
                speak(f'opening {" ".join(q[1::])}')
        
        elif q[0] == "close":
            Close(" ".join(q[1::]),match_closest=True)
            speak(f'closing {" ".join(q[1::])}')



        elif text == "open notepad":
            open_notepad()
        elif text == "write something on notepad":
            text_to_write = speak()
            if text_to_write:
                open_notepad(text_to_write)





        elif text=='play music':
                file=open("chose.txt",'r')
                chose=file.readlines()
                chose=int(chose[0])
                m='e:\\songs'
                song=os.listdir(m)
                length=len(song)
                speak("now music is playing")
                os.startfile(os.path.join(m,song[chose]))
                chose+=1
                file = open("chose.txt",'w')
                file.write(str(chose))
                file.close()
        elif text=='next':
                file=open("chose.txt",'r')
                chose=file.readlines()
                chose=int(chose[0])
                m='e:\\songs'
                song=os.listdir(m)
                length=len(song)
                if chose>=length:
                    speak("no more music to next")
                    speak("i'm playing music from starting")
                    chose=0
                    os.startfile(os.path.join(m,song[chose]))
                else:
                    os.startfile(os.path.join(m,song[chose]))
                    chose+=1
                file = open("chose.txt",'w')
                file.write(str(chose))
                file.close()

        # elif text == 'deep check':
        #     speak("opening deepfake application")
        #     run_django_app()
        #     speak("Running Local Server at port 8000")

        elif text == "run security check":
             security_check()

        elif text=='stop music':
                speak('ok boss')
                # Close("Media Player",match_closest=True)
                speak("now i stop music")
                # os.system('taskkill /F /FI "WINDOWTITLE eq Movies & Tv" ')
                os.system('taskkill /F /FI "WINDOWTITLE eq Media Player" ')
                
        else:
            response = chat.send_message(text)
            responsetext = to_text(response.text)
            speak(responsetext)
            # print("speaking...")
            todaydate = date.today()
            if not os.path.exists(f'outputhistory/{todaydate}'):
                os.mkdir(f'outputhistory/{todaydate}')
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            # print(f'{todaydate}/{current_time}.txt')
            f = open(os.path.join(f'outputhistory/{todaydate}/',f'{current_time}.txt'),'w')
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
                        # cp = multiprocessing.Process(target=jarvis_brain,args=(query,))
                        # cp.start()
                        jarvis_brain(query)
                        
                except Exception as e:
                    print(e)
                    pass
                    # speak("not recognize")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
