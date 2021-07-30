from FlightRadar24.api import FlightRadar24API
from threading import Thread
from time import sleep

RETRIES = 3
RATE_LIMIT_DELAY = 1


ZONE_UK = {
    "tl_y": 62.61,
    "tl_x": -13.07,
    "br_y": 49.71,
    "br_x": 3.46,
}

ZONE_HOME = {
    "tl_y": 55.92860260752661,
    "tl_x": -4.359924486085342,
    "br_y": 55.89148040308923,
    "br_x": -4.324657457545864
}


class Overhead:
    def __init__(self):
        self._api = FlightRadar24API()
        self._data = []
        self._new_data = False
        self._processing = False

    def grab_data(self):
        Thread(target=self._grab_data).start()

    def _grab_data(self):
        # Mark data as old
        self._new_data = False
        self._processing = True
        data = []

        # Grab flight details
        bounds = self._api.get_bounds(ZONE_HOME)
        flights = self._api.get_flights(bounds=bounds)

        for flight in flights[:3]:
            retries = RETRIES

            while retries:
                # Rate limit protection
                sleep(RATE_LIMIT_DELAY)

                # Grab and store details
                try:
                    details = self._api.get_flight_details(flight.id)
                    data.append(
                        {
                            "plane": details["aircraft"]["model"]["text"],
                            "origin": flight.origin_airport_iata,
                            "destination": flight.destination_airport_iata,
                            "vertical_speed": flight.vertical_speed,
                            "altitude": flight.altitude,
                        }
                    )
                    break

                except (KeyError, AttributeError):
                    retries -= 1

        self._new_data = True
        self._processing = False
        self._data = data

    @property
    def new_data(self):
        return self._new_data

    @property
    def processing(self):
        return self._processing

    @property
    def data(self):
        self._new_data = False
        return self._data


# Main function
if __name__ == "__main__":

    o = Overhead()
    o.grab_data()
    while not o.new_data:
        print("processing...")
        sleep(1)

    print(o.data)
