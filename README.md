# Documentation

[Blog article about this project](https://blog.colinwaddell.com/flight-tracker/)

# Setup

## Configuration

In the root of the repo create a files `config.py` with the settings for your display. For example:

```
ZONE_HOME = {
    "tl_y": 56.06403, # Top-Left Latitude (deg)
    "tl_x": -4.51589, # Top-Left Longitude (deg)
    "br_y": 55.89088, # Bottom-Right Latitude (deg)
    "br_x": -4.19694 # Bottom-Right Longitude (deg)
}
LOCATION_HOME = [
    55.9074356, # Latitude (deg)
    -4.3331678, # Longitude (deg)
    0.01781 # Altitude (km)
]
TEMPERATURE_LOCATION = "Glasgow"
```
