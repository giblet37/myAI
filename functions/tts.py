
import json
#import subprocess
import log
import settings
import sox
#import wave
import time
from apis import api_lib

def speak(message=None):
        data = json.loads(message)
        text = data['text']
        siteId = data['siteId']
        sessionId = data['sessionId']
        theId = data['id']

        filename = settings.VOICE_DIR + "/{}.aiff".format(siteId)
        newFilename = settings.VOICE_DIR + "/{}.wav".format(siteId)

        try:
            from AppKit import NSSpeechSynthesizer
            from AppKit import NSURL

            nssp = NSSpeechSynthesizer
            ve = nssp.alloc().init()
            #using the system default voice.. else can set it here
            #from_voice = "com.apple.speech.synthesis.voice.samantha.premium"
            #ve.setVoice_(from_voice)
            result_url = NSURL.fileURLWithPath_(filename)
            ve.startSpeakingString_toURL_(text, result_url)
            time.sleep(0.5)
        except:
            log.info("TTS Failed.. most likely not OSX system")
        else:
            tfm = sox.Transformer()
            tfm.convert(samplerate=16000, n_channels=1, bitdepth=16)
            tfm.build(filename, newFilename)

            fp = open(newFilename,'rb')
            f = fp.read()


            #send the ID in reverse to use it later when say finished in the mqtt_api
            topic = 'hermes/audioServer/{}/playBytes/{}'.format(siteId, theId[::-1])
            api_lib['mqtt'].publish_item(topic, bytearray(f))

            fp.close()

      

#hermes/tts/say
#{"text":"where to","lang":"en","id":"fb9687f7-991f-4638-9a9c-033ef008834a","siteId":"zero","sessionId":"22db028e-6f52-4455-b7eb-3b1798848cf0"}

#hermes/tts/sayFinished
#{"id":"7f82d563-5b25-410b-8fa9-5681c25c34b6","sessionId":null}