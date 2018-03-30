from module import Module
from task import ActiveTask
from apis import api_lib
from apscheduler.schedulers.background import BackgroundScheduler
import string
import random
import dateutil.parser as parser
from functions import jsonentities
from datetime import datetime
from pyowm.utils import timeutils
import json
import log

scheduler = BackgroundScheduler()
scheduler.start()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def timer_function(id,text):
    print(text)
    scheduler.print_jobs()
    api_lib['sql'].delete_item('timers', 'key', id)
    print('Scheduled Timers Remaining..')
    scheduler.print_jobs()


class Timers(ActiveTask):

    def __init__(self):
        # timer intent must contain the entity TIME and the question has to be asked as in the patterns
        super(Timers, self).__init__(intent=['timer'], slots=['time'], patterns=[r'.*\b(?:set)\b.*\b(?:timer|reminder)\b.*', r'.*\b(?:remind me)\b.*\b(?:to|in)\b.*'])

    def onError(self):
        self.speak('something went wrong, Did you specify when to set the timer')

    def action(self, intent, objs):
        self.speak('timer action fired')

        forDate = None
        message = None

        q = objs['entities']

        for d in q:
            if d.get("entity", "") == "time":
                forDate = d['value']['value']
            elif d.get("entity", "") == "timer_message":
                message = d['value']

        if forDate:
            uniqueid = id_generator()
            d = parser.parse(forDate)

            api_lib['sql'].insert_item('timers', {'at': d,
                                                     'key': uniqueid,
                                                     'message':message})

            scheduler.add_job(timer_function, 'date', run_date=d, args=[uniqueid,message])

            print('Current Scheduled Timers..')
            scheduler.print_jobs()
        else:
            self.speak('timer module could not determine when to set the timer')


class CancelTimer(ActiveTask):

    def __init__(self):
        # Matches any statement with these words .*\bstop|cancel.*timer|reminder
        super(CancelTimer, self).__init__(intent=['timer'], patterns=[r'.*\b(stop|cancel).*(timer|reminder)'])

    def action(self, intent, text):
        return self.speak('Canceling timer.')


class Timer(Module):

    def __init__(self):
        log.debug("Timer Module INIT...")
        #we use a DB so make sure the table is there
        sql_create_timers_table = """ CREATE TABLE IF NOT EXISTS timers (
                                                id integer PRIMARY KEY,
                                                at text NOT NULL,
                                                key text NOT NULL,
                                                message text
                                            ); """

        api_lib['sql'].create_table(sql_create_timers_table)

        #remove any old timers that should have run already incase the system was down when they should have fired
        sql = 'DELETE FROM timers WHERE at < "{0}"'.format(datetime.now())
        api_lib['sql'].run_sql(sql)

        #get any records that still are there after deleting old ones
        ts = api_lib['sql'].get_all_records('timers')

        if len(ts) == 0:
            log.debug("No timers need to be recreated")
        else:
            log.debug("{} timers being created".format(len(ts)))
            for records in ts:
                d = parser.parse(records[1])
                job = scheduler.add_job(timer_function, 'date', misfire_grace_time=4, run_date=d, args=[records[2], records[3]], id=records[2])
                #print(job.misfire_grace_time)
                log.info(scheduler.print_jobs())


        tasks = [Timers(), CancelTimer()]
        super(Timer, self).__init__('timer', tasks, enabled=False)