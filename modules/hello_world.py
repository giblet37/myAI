"""
        File Name: hello_world.py
        saying hello.. a greeting
        Usage Examples:
        - "Hey Janet.. Hello"
"""

from module import Module
from task import ActiveTask
from apis import api_lib
import random

foo = ['Hello, what can I do for you', 'Hi, what can I do for you', 'Hi there, what can I do for you', 'Hey you, what can I do for you', 'What\'s up, what can I do for you']


class SpeakPhrase(ActiveTask):

    def __init__(self):
        # Matches any statement with these words
        super(SpeakPhrase, self).__init__(intent=['Helloworld'])

    def action(self, intent, objs):
        secure_random = random.SystemRandom()

        say = secure_random.choice(foo)
        siteId = objs['siteId']
        sessionId = objs['sessionId']

        action = "{\"text\":\"" + say + "\",\"sessionId\":\"" + sessionId + "\"}"
        api_lib['mqtt'].publish_item("hermes/dialogueManager/continueSession", action)


# This is a bare-minimum module
class HelloWorld(Module):

    def __init__(self):
        tasks = [SpeakPhrase()]
        self.enabled = False
        super(HelloWorld, self).__init__('hello_world', tasks, enabled=False)
