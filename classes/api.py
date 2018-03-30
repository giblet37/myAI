"""
The "Api" class is used when an instance
of an API is required in the apis.api_lib

Use "from apis import api_lib" & "api_lib['(api_name_key)']"
to access instances of APIs.
"""
import traceback


class Api(object):

    def __init__(self, key, enabled=True):
        """ Make a unique api key name (e.g. 'spotify_api') """
        self.key = key
        self.enabled = enabled


