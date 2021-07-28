from threading import Thread
from time import sleep
import urllib.request, json


class Overhead:
    def __init__(
        self,
        refresh_seconds=30,
        lat_min=55.89148040308923,
        lng_min=-4.359924486085342,
        lat_max=55.92860260752661,
        lng_max=-4.324657457545864,
    ):
        self.refresh_seconds = refresh_seconds
        self.lat_min = lat_min
        self.lng_min = lng_min
        self.lat_max = lat_max
        self.lng_max = lng_max

    def run(self):
        Thread(target=self._grab_data).start()

    def _api_url(self):
        return (
            "https://opensky-network.org/api/states/all?"
            f"lamin={self.lat_min}&lomin={self.lng_min}&lamax={self.lat_max}&lomax={self.lng_max}"
        )

    def _grab_data(self):
        with urllib.request.urlopen(self._api_url()) as url:
            data = json.loads(url.read().decode())
            print(data)
        sleep(self.refresh_seconds)
