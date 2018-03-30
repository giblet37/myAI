"""
        File Name: no_match.py
        When no module intents, patterns etc match we use this one
"""

from module import Module
from task import ActiveTask
import settings
import log
from six.moves import urllib


class AnswerTask(ActiveTask):

    def match(self, intent, jsonText):
        return False

    def action(self, intent, text):
        text_return = settings.ERROR

        data = {
            'input' : text['text'],
            'appid' : settings.WOLFRAM_KEY,
            'units' : settings.WOLFRAM_UNITS
        }

        data = urllib.parse.urlencode(data)
        url = 'https://api.wolframalpha.com/v1/result?format=plaintext&'
        log.info('Using Wolfram to search - ' + url + data)
        try: resp = urllib.request.urlopen(url + data)
        except urllib.error.URLError as e:
            log.error('Wolfram failed - ({}) reason: {}'.format(e.code, e.reason))
        except urllib.error.HTTPError as e:
            log.error('Wolfram failed - ({}) reason: {}'.format(e.code, e.reason))
        else:
            text_return = resp.read()

        return text_return


class Wolfram(Module):

    def __init__(self):
        tasks = [AnswerTask()]
        self.enabled = False
        super(Wolfram, self).__init__('wolfram', tasks, enabled=False)
