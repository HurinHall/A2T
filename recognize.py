import speech_recognition as sr
from googletrans import Translator
import sys, os, uuid

def Google(r, audio):
    return r.recognize_google(audio, key="Your Key")
    #return r.recognize_google(audio)
    #return r.recognize_google_cloud(audio, credentials_json="Your Key") 

def Wit(r, audio):
    return r.recognize_wit(audio, key="Your Key")

def Bing(r, audio):
    #active for 30 days https://azure.microsoft.com/en-us/try/cognitive-services/my-apis/
    return r.recognize_bing(audio, key="Your Key")

def Houndify(r, audio):
    #100/day
    return r.recognize_houndify(audio, client_id="Client ID", client_key="Client Key")

def Sphinx(r, audio):
    return r.recognize_sphinx(audio)

def ReadAudio(r, file):
    try:
        with sr.AudioFile(file) as source:
            audio = r.record(source)
    except FileNotFoundError:
        print("Audio file '"+file+"' does not exist")
    return audio

def Export(file, str):
    f = open(file, "w")
    f.write(str)
    f.close()
    
def Print(str):
    print(str)

def Main():
    method = ["Google", "Wit", "Bing", "Houndify", "Sphinx"]
    r=sr.Recognizer()
    if len(sys.argv) < 2:
        print('Please specify recognition tool')
        print('Like: Google, Wit, Bing, Houndify, Sphinx')
    elif (len(sys.argv) == 2 and sys.argv[1] == 'help'):
        print('Usage:')
        print('recognize.py method audiofile [output file]/[-translate] [translate language]')
        print('Method: Google, Wit, Bing, Houndify, Sphinx')
        print('Language: zh-CN, zh-TW, en')
    elif method.index(sys.argv[1]) == -1:
        print('Recognition tool does not exist!')
    elif len(sys.argv) < 3:
        print('Please input audio file')
    elif not sys.argv[2].lower().endswith(('.flac', '.wav')):
        print('Please input valid audio file such as .flac, .wav')
    elif (len(sys.argv) >= 3):
        try:
            file = sys.argv[2]
            audio = ReadAudio(r, file)
            if sys.argv[1] == 'Google':
                str = Google(r, audio)
            elif sys.argv[1] == 'Wit':
                str = Wit(r, audio)
            elif sys.argv[1] == 'Bing':
                str = Bing(r, audio)
            elif sys.argv[1] == 'Houndify':
                str = Houndify(r, audio)
            elif sys.argv[1] == 'Sphinx':
                str = Sphinx(r, audio)
            Print(str)
            if (len(sys.argv) > 3 and not sys.argv[3].startswith('-')):
                Export(sys.argv[3], str)
            elif (len(sys.argv) > 3 and sys.argv[3] == '-translate'):
                translator = Translator()
                if len(sys.argv) > 4:
                    translation = translator.translate(str, dest=sys.argv[4])
                else:
                    translation = translator.translate(str)
                print('\nTranslate:')
                Print(translation.text)
            if (len(sys.argv) > 4 and sys.argv[4] == '-translate'):
                translator = Translator()
                if len(sys.argv) > 5:
                    translation = translator.translate(str, dest=sys.argv[5])
                else:
                    translation = translator.translate(str)
                print('\nTranslate:')
                Print(translation.text)
        except IndexError:
            print("No internet connection")
        except KeyError:
            print("Invalid API key or quota maxed out")
        except LookupError:
            print("Could not understand audio")
        except sr.UnknownValueError:
            print("Unknow error")
        except UnboundLocalError:
            pass
    else:
        print('Usage:')
        print('recognize.py method audiofile [output file]')
        print('Method: Google, Wit, Bing, Houndify, Sphinx')

Main()
