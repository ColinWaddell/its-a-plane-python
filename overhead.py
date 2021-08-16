from FlightRadar24.api import FlightRadar24API
from threading import Thread, Lock
from time import sleep

RETRIES = 3
RATE_LIMIT_DELAY = 1
MAX_FLIGHT_LOOKUP = 5
MAX_ALTITUDE = 10000  # feet
BLANK_FIELDS = ["", "N/A", "NONE"]


ZONE_UK = {"tl_y": 62.61, "tl_x": -13.07, "br_y": 49.71, "br_x": 3.46}
ZONE_HOME = {"tl_y": 56.06403, "tl_x": -4.51589, "br_y": 55.89088, "br_x": -4.19694}
ZONE_DEFAULT = ZONE_HOME


class Overhead:
    def __init__(self):
        self._api = FlightRadar24API()
        self._lock = Lock()
        self._data = []
        self._new_data = False
        self._processing = False

    def grab_data(self):
        Thread(target=self._grab_data).start()

    def _grab_data(self):
        # Mark data as old
        with self._lock:
            self._new_data = False
            self._processing = True

        data = []

        # Grab flight details
        bounds = self._api.get_bounds(ZONE_DEFAULT)
        flights = self._api.get_flights(bounds=bounds)

        # Sort flights by altitude, lowest first
        flights = [f for f in flights if f.altitude < MAX_ALTITUDE]
        flights = sorted(flights, key=lambda f: f.altitude)

        for flight in flights[:MAX_FLIGHT_LOOKUP]:
            retries = RETRIES

            while retries:
                # Rate limit protection
                sleep(RATE_LIMIT_DELAY)

                # Grab and store details
                try:
                    details = self._api.get_flight_details(flight.id)

                    # Get plane type
                    try:
                        plane = details["aircraft"]["model"]["text"]
                    except (KeyError, TypeError):
                        plane = ""

                    # Tidy up what we pass along
                    plane = (
                        plane
                        if not (plane.upper() in BLANK_FIELDS)
                        else ""
                    )

                    origin = (
                        flight.origin_airport_iata
                        if not (flight.origin_airport_iata.upper() in BLANK_FIELDS)
                        else ""
                    )

                    destination = (
                        flight.destination_airport_iata
                        if not (flight.destination_airport_iata.upper() in BLANK_FIELDS)
                        else ""
                    )


                    callsign = (
                        flight.callsign 
                        if not (flight.callsign.upper() in BLANK_FIELDS) 
                        else ""
                    )

                    data.append(
                        {
                            "plane": plane,
                            "origin": origin,
                            "destination": destination,
                            "vertical_speed": flight.vertical_speed,
                            "altitude": flight.altitude,
                            "callsign": callsign,
                        }
                    )
                    break

                except (KeyError, AttributeError):
                    retries -= 1

        with self._lock:
            self._new_data = True
            self._processing = False
            self._data = data

    @property
    def new_data(self):
        with self._lock:
            return self._new_data

    @property
    def processing(self):
        with self._lock:
            return self._processing

    @property
    def data(self):
        with self._lock:
            self._new_data = False
            return self._data
    
    @property
    def data_is_empty(self):
        return len(self._data) == 0


# Main function
if __name__ == "__main__":

    o = Overhead()
    o.grab_data()
    while not o.new_data:
        print("processing...")
        sleep(1)

    print(o.data)
