""" Assistant start script """
import web, os
import json
import AI
from datetime import datetime
import json
import log
import settings
import sys
from os import path

sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

urls = (
    '/', 'index',
    '/parse', 'parse'
)

VERSION = '1.0'
settings.MODEL_DIR = os.path.join(os.getcwd(), "data/model")

class index:
    def GET(self):
        log.info('About called')
        Z = datetime.now() - settings.SERVER_STARTTIME
        days = Z.days
        hours = Z.seconds // 3600
        minutes = (Z.seconds % 3600) // 60
        seconds = (Z.seconds % 60)

        t = ''
        if days > 0:
            t = '{} days '.format(days)
        if hours > 0:
            t = '{}{} hours '.format(t,hours)
        if minutes > 0:
            t = '{}{} minutes '.format(t,minutes)
        if seconds > 0:
            t = '{}{} seconds'.format(t, seconds)

        return json.dumps({'Janet Version': VERSION,
                           'Up Time': '{}'.format(t),
                           'Requests': settings.REQUESTS_COUNT})

class parse:
    def GET(self):
        web.header('Content-Type', 'application/json')
        user_data = web.input(q=u'', device=u'')
        if not user_data.q or not user_data.device:
            log.error("invalid URL string provided - {}".format(web.ctx.fullpath))
            return "invalid URL.. must be in the pattern of /parse?q=question+to+ask&device=rpi \nonly {} was passed".format(web.ctx.fullpath)
        else:
            return json.dumps(brain.inst.parse_text(user_data.q, user_data.device))


class myAI(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
    #app = web.application(urls, globals())
    settings.SERVER_STARTTIME = datetime.now()
    settings.REQUESTS = 0
    
    log.info('')
    log.info('')
    log.info('')
    log.info('')
    log.info("****************************************")
    log.info("***          Starting Janet v{}     ***".format(VERSION))
    log.info("****************************************")
    log.info('')
    log.info('')
    log.info("Started {}".format(settings.SERVER_STARTTIME))
    
    AI.init()
   
    
    app = myAI(urls, globals())
    app.run(port=8888)


