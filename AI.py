#import os.path
#import shutil
import settings, apis, module, log
import json
from functions.intent_parser import IntentParser

inst = None


def init():
    global inst
    inst = AI()


class AI:
    intentHistory = {}

    def __init__(self):

        #load API classes
        apis.find_apis()
        apis.list_apis()

        #load INTENT modules
        module.find_mods()
        module.list_mods()
        module.list_enabled_mods()

    def set_intenthistory(self, siteId='default',intent='',json=''):
        intentHistory[siteId] = {'intent':intent, 'json':json}

    def get_intenthistory(self, siteId='default'):
        data = None
        if siteId in intentHistory:
            data = intentHistory[siteId]

        return data

    
    def parse_string(self, jsonObject):
        self.parse_intent(jsonObject)

    def parse_intent(self, jsonObject):
        settings.REQUESTS_COUNT += 1

        payload = json.loads(jsonObject.decode('utf-8'))
        intent = IntentParser.get_intent_name(payload)

        module_found = False
        for mod in module.mod_lib:
            if not mod.enabled:
                continue #dont work with modules if they are currently disabled
            """ Find matched module with intent """
            _mod = mod.intents[0]
            if _mod.match(intent):
                module_found = True
                if _mod.user:
                    print _mod.user
                _mod.action(intent, payload)
                break

        if module_found == False:
            settings.ERROR_COUNT += 1
            log.error("no module for {}".format(intent))

            #siteId = payload['siteId']
            phrase = 'I do not have a module to do {}'.format(intent)
            sessionId = payload['sessionId']
            jsonString = "{\"text\":\"" + phrase + "\",\"sessionId\":\"" + sessionId + "\"}"
            #print jsonString
            
            apis.api_lib['mqtt'].publish_item("hermes/dialogueManager/endSession", jsonString)

