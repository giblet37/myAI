"""
The "Intent" class represents an action to be performed
"""

import re
import settings
from apis import api_lib
from functions.intent_parser import IntentParser


def speak(phrase, jsonObjects):
    siteId = jsonObjects['siteId']
    sessionId = jsonObjects['sessionId']

    if phrase == None:
        jsonString = "{\"sessionId\":\"" + sessionId + "\"}"
        print jsonString
    else:
        jsonString = "{\"text\":\"" + phrase + "\",\"sessionId\":\"" + sessionId + "\"}"
        print jsonString
        
    
    api_lib['mqtt'].publish_item("hermes/dialogueManager/endSession", jsonString)
    '''
    hermes/dialogueManager/endSession

    When the handler received the intents it needs, or when the handler wants to explicitly end a running session, it should send this endSession message with the given sessionId.

    Key	Value
    sessionId	String - Session identifier to end.
    text	Optional String - The text the TTS should say to end the session.
    If the text is null, the Dialog Manager will immediately send a endedSession message after receiving this message, otherwise, the endedSession will be sent after the text is said.
    '''
def slotValue(jsonObjects, slotName):
    return IntentParser.get_slot_value(jsonObjects,slotName)

def slotDateValue(jsonObjects, slotName):
    return IntentParser.parse_date_value(jsonObjects,slotName)

def slotDateRange(jsonObjects, slotName):
    return IntentParser.parse_date_range(jsonObjects,slotName)
    
def mqttPostTopic(topic,message=None):
    api_lib['mqtt'].publish_item(topic, message)

def parseDateRawValue (jsonObjects, slotName):
    return IntentParser.parse_date_raw_value(jsonObjects,slotName)


class Intent(object):
    speak = staticmethod(speak)
    slotValue = staticmethod(slotValue)
    slotDateValue = staticmethod(slotDateValue)
    slotDateRange = staticmethod(slotDateRange)
    parseDateRawValue = staticmethod(parseDateRawValue)

    def action(self, intent, objs):
        """ Execute the intent action """
        return

    def onError(self):
        """ Execute the intent error action """
        return

class ActiveIntent(Intent):
    def __init__(self,intent=None, user=[]):
        """ intent to match from the NLU return """
        self.intent = intent
        self.user = user


    def match(self, intent):
        """ Check if the nlu intent matches an activeintent object """
        is_match = False
        for intent_item in self.intent:
            if intent_item == intent:
                is_match = True
                break
       
        return is_match

