"""
        File Name: openweathermap.py
        Tells you weather information
        Usage Examples:
        - "What the weather like today"
"""

import dateutil.parser as parser
import pyowm
from pyowm.caches.lrucache import LRUCache
from pyowm.utils import timeformatutils
from pyowm.utils import timeutils
from pyowm.webapi25 import forecast, forecaster
import json
import time
import settings
import datetime
from module import Module
from intent import ActiveIntent

cache = LRUCache()

_url = 'http://api.openweathermap.org/data/2.5/weather?APPID=%s&units=%s&', (settings.OWM_API_KEY, settings.OWM_UNITS)

class Weather(ActiveIntent):

    def __init__(self):
        # Matches any statement with these words
        super(Weather, self).__init__(intent=['weather'])

    def onError(self,objs):
        self.speak('I can not do that with the weather module', objs)

    def action(self, intent, objs):
        q = None
        owm = pyowm.OWM(settings.OWM_API_KEY)

        #country = jsonentities.find_value(objs['entities'], 'country')
        place = self.slotValue(objs,'location') #location in the house.. kitchen, bedroom 
        weather_item = self.slotValue(objs, 'weatherItem')
        forDate = self.slotDateValue(objs, 'date')

        startDate = datetime.datetime.today()
        endDate = datetime.datetime.today()

        print type(forDate)
        calcTotalDays = 0
        if type(forDate) == dict:
            text = objs['input']
            if 'weekend' in text:
                startDate = forDate["start"] + datetime.timedelta(hours=6)
                endDate = startDate + datetime.timedelta(days=1)
                calcTotalDays = 2
            else:
                startDate = forDate["start"]
                endDate = forDate["end"]
                calcTotalDays = (endDate - startDate).days
        else:
            print "single date"
            startDate = forDate
            endDate = forDate
            calcTotalDays = 1

        calcStartDays = (datetime.date.today() - startDate.date()).days
        calcEndDays = (datetime.date.today() - endDate.date()).days

        if (calcStartDays > 0) and (type(forDate) != dict):
            #we dont do the past
            print "starting date is in the past"
            self.speak('I can not do weather information from the past, only the future', objs)
        elif (type(forDate) == dict) and (calcEndDays >= 0):
            #we dont do the past
            print "date range in the past"
            self.speak('I can not do weather information from the past, only the future', objs)
        elif (type(forDate) == dict) and (calcStartDays >= 0):
            #pad the start date to today to forget about past dates
            #asking for "this week" and if today is wednesday, the dates returned will include the past mon and tues
            startDate = datetime.datetime.today()
            calcTotalDays = (endDate.replace(tzinfo=None) - startDate.replace(tzinfo=None)).days + 1
        elif (calcStartDays < -15):
            #we dont do that far into the future
            print "starting date is to far into the future"
            self.speak('I can not do weather that far into the future', objs)

        startDate = startDate.replace(hour=0, minute=0, second=0)
        endDate = endDate.replace(hour=23, minute=59, second=59)
        
        #****************************************************************************************************
        if place is None:
            #then we are wanting to know about real weather info for the suburb
            q = '%s' % (settings.OWM_LOCATION)
        else:
            #if there was a place then its a reading from an IoT sensor in the house 'location'/'place'
            q = '%s' % (place)
            print 'a reading from an IoT sensor in the house'
            return

        if q is None:
            self.onError(objs)
            return
        
        '''
        ddd = startDate
        c = timeformatutils.to_date(ddd)
        
        strDayName = ''

        calcDays = (datetime.date.today() - c.date()).days
        if calcDays > 0:
            #we dont do the past
            print "in the past"
            self.speak('I can not do weather information from the past, only the future', objs)
        elif calcDays == 0:
            strDayName = 'today'
        elif calcDays == -1:
            strDayName = 'tomorrow'
        else:
            strDayName =  c.strftime("%A")
        
        '''

        fc = owm.daily_forecast(q,16)
        #fc = obs.daily_forecast()
        #print "when raining"
        #print fc.when_rain()

        w = None
      
   
        weathers =[]
        firstDate = startDate
        for x in range(0, calcTotalDays):
            c = timeutils.next_hour(firstDate)
            w = fc.get_weather_at(c)
            weathers.append(w)
            firstDate = firstDate + datetime.timedelta(days=1)

        #nfc = forecaster.Forecaster(weathers)
        current_time = int(round(time.time()))
        #fc.get_forecast().get_interval()
        nfc = forecast.Forecast(None, current_time, fc.get_forecast().get_location(), weathers)
        nfc.set_interval("daily")
        fc = forecaster.Forecaster(nfc)
    
        
        sayString = ''
        sayString = self.parseDateRawValue(objs,"date")
        if sayString == 'weekend':
            sayString = "this " + sayString
        sayString = sayString + ", "
        
        if len(weathers) == 1:
            weather = weathers[0]
            temp = weather.get_temperature(unit=settings.OWM_TEMPUNIT)
            detail = weather.get_detailed_status()
            sayString += "{}, with a top of {}.".format(detail, int(temp["max"]))  
        elif len(weathers) > 1:
            if weather_item is None:
                for weather in weathers:
                    sayString += self.generalWeatherInfo(weather)
                    startDate = startDate + datetime.timedelta(days=1)
            else:
                if 'weekend' in sayString:
                    for weather in weathers:
                        sayString += self.generalWeatherInfo(weather)
                        startDate = startDate + datetime.timedelta(days=1)
                else:
                    if weather_item == 'hot':
                        w = fc.most_hot()
                        sayString += self.generalSlotWeatherInfo(w, "warmest")
                    elif weather_item == 'cold':
                        w = fc.most_cold()
                        sayString += self.generalSlotWeatherInfo(w, "coolest")
                    elif weather_item == 'rain':
                        w = fc.most_rainy()
                        if len(w) > 0:
                            sayString += self.generalSlotWeatherInfo(w, "wettest")
                        else:
                            sayString += "it's not forecast to rain"
        else:
            #there is no weather info
            self.speak('I can not do the weather. Might not be able to access the weather website, the internet, or something went wrong', objs)

        print sayString
        self.speak(sayString, objs)

    

    def generalWeatherInfo(self, weather):
        temp = weather.get_temperature(unit=settings.OWM_TEMPUNIT)
        detail = weather.get_detailed_status()
        dateName = self.weatherDateString(weather.get_reference_time(timeformat='date'))
        return "{}, {}, with a top of {}.".format(dateName, detail,int(temp["max"])) 

    def generalSlotWeatherInfo(self, weather, text):
        temp = weather.get_temperature(unit=settings.OWM_TEMPUNIT)
        detail = weather.get_detailed_status()
        dateName = self.weatherDateString(weather.get_reference_time(timeformat='date'))
        return "{} will be the {} day, {}, with a top of {}.".format(dateName, text, detail,int(temp["max"])) 

    def weatherDateString(self, inputDate):
        calcDays = (datetime.date.today() - inputDate.date()).days
        if calcDays == 0:
            return 'today'
        elif calcDays == -1:
            return'tomorrow'
        else:
            return inputDate.strftime("%A")

    


# This is a bare-minimum module
class OpenWeatherMap(Module):

    def __init__(self):
        intent = [Weather()]
        self.enabled = True
        super(OpenWeatherMap, self).__init__('weather', intent)




'''
# Will it be rainy, sunny, foggy or snowy at the specified GMT time?
time = "2013-09-19 12:00+00"
>>> fc.will_be_rainy_at(time)
False
>>> fc.will_be_sunny_at(time)
True
>>> fc.will_be_foggy_at(time)
False
>>> fc.will_be_cloudy_at(time)
False
>>> fc.will_be_snowy_at(time)
False
>>> fc.will_be_sunny_at(0L)           # Out of weather forecast coverage
pyowm.exceptions.not_found_error.NotFoundError: The searched item was not found.
Reason: Error: the specified time is not included in the weather coverage range



# List the weather elements for which the condition will be:
# rain, sun, fog and snow
>>> fc.when_rain()
[<weather.Weather at 0x00DB22F7>,<weather.Weather at 0x00DB2317>]
>>> fc.when_sun()
[<weather.Weather at 0x00DB62F7>]
>> fc.when_clouds()
[<weather.Weather at 0x00DE22F7>]
>>> fc.when_fog()
[<weather.Weather at 0x00DC22F7>.]
>>> fc.when_snow()
[]                                   # It won't snow: empty list



# Get weather for the hottest, coldest, most humid, most rainy, most snowy
# and most windy days in the forecast
>>> fc.most_hot()
<weather.Weather at 0x00DB67D9>
>>> fc.most_cold()
<weather.Weather at 0x00DB62F7>
>>> fc.most_humid()
<weather.Weather at 0x00DB62F7>
>>> fc.most_rainy()
<weather.Weather at 0x00DB62F7>
>>> fc.most_snowy()
None                                 # No snow in the forecast
>>> fc.most_windy()
<weather.Weather at 0x00DB62F7>

'''