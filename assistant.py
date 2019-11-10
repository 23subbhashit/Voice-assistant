import speech_recognition as sr
import re
import wikipedia
from pyowm import OWM
import webbrowser
import subprocess
import smtplib
import random
from datetime import datetime
r=sr.Recognizer()                                                                         #for speech recognition
greet_in= ("hello", "hi", "greetings", "sup", "what's up","hey")
greet_out= ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
  for word in sentence.split():
        if word.lower() in greet_in:
            return random.choice(greet_out)
with sr.Microphone() as source:
    print("say something...")
    audio=r.listen(source)
try:
    text=r.recognize_google(audio)    
    print("you said::",text)
except:
    print("translation failed:.")

if 'tell me about' in text:                                       #To know about something
        exp= re.search('tell me about (.*)',text)
        try:
            if exp:
                topic = exp.group(1)
                ny = wikipedia.page(topic)
                print(ny.content[:200])
        except Exception as e:
                pass
elif 'current weather' in text:                                   #To know the current weather
     exp = re.search('current weather in (.*)',text)
     if exp:
         city = exp.group(1)
         API_key = ''                                             #API key has to be generated
         owm = OWM(API_key)
         obs = owm.weather_at_place(city)
         w = obs.get_weather()
         k = w.get_status()
         x = w.get_temperature(unit='celsius')
         print("city:",city)
         print("Temprature:",k)
         print("max:",x["temp_max"])
elif "open" in text:                                              #To open a url
    exp=re.search("open (.*)",text)
    if exp:
        d=exp.group(1)
        print(d)
        url = 'https://www.' + d+".com"
        webbrowser.open(url)
        print("website is opened")
    else:
        pass
elif text.lower() in greet_in:                                  #Greet        
    a=greeting(text.lower())
    print(a) 
elif 'launch' in text:                                          #To open an app in your system
        exp= re.search('launch (.*)', text)
        if exp:
            appname = exp.group(1)
            appname1 = appname+".exe"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
elif 'time' in text:                                            #Shows the current time
     now = datetime.now()
     print('Current time is %d hours %d minutes' % (now.hour, now.minute))
elif 'email' in text:                                           #To email someone
    sender=input("Please enter your email :")
    receiver=input("Please enter receiver's email")
    password=input("please enter your password")
    print('What should I say to him?')
    with sr.Microphone() as source:
        print("content")
        b=r.listen(source)
    try:
        content=r.recognize_google(audio)
        print("content is :",content)
    except:
        print("translation failed:.")
            
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender,password)
    mail.sendmail(sender,receiver,content)
    mail.close()
    print('Email has been sent successfuly. You can check your inbox.')
