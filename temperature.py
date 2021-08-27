import urllib.request
import json

URL = 'https://taps-aff.co.uk/api/'
LOCATION = 'Glasgow'

class Temperature:
    def __init__(self, location=LOCATION):
        self._location = LOCATION
    
    def grab(self):
        current_temp = None

        try:
            request = urllib.request.Request(URL + self._location)
            raw_data = urllib.request.urlopen(request).read()
            content = json.loads(raw_data.decode('utf-8'))
            current_temp = content["temp_c"]

        except:
            pass

        return current_temp
