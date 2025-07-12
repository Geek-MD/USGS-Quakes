"""Constants for USGS Quakes integration."""

from homeassistant.const import UnitOfLength

DOMAIN = "usgs_quakes"

DEFAULT_RADIUS_IN_KM = 50.0
DEFAULT_MINIMUM_MAGNITUDE = 0.0
DEFAULT_UNIT_OF_MEASUREMENT = UnitOfLength.KILOMETERS

CONF_FEED_TYPE = "feed_type"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"

# Mapping of USGS feed types to friendly names
FEED_FRIENDLY_NAMES = {
    "past_hour_significant_earthquakes": "Significant Earthquakes (Past Hour)",
    "past_hour_m45_earthquakes": "Magnitude ≥4.5 (Past Hour)",
    "past_hour_m25_earthquakes": "Magnitude ≥2.5 (Past Hour)",
    "past_hour_m10_earthquakes": "Magnitude ≥1.0 (Past Hour)",
    "past_hour_all_earthquakes": "All Earthquakes (Past Hour)",
    "past_day_significant_earthquakes": "Significant Earthquakes (Past Day)",
    "past_day_m45_earthquakes": "Magnitude ≥4.5 (Past Day)",
    "past_day_m25_earthquakes": "Magnitude ≥2.5 (Past Day)",
    "past_day_m10_earthquakes": "Magnitude ≥1.0 (Past Day)",
    "past_day_all_earthquakes": "All Earthquakes (Past Day)",
    "past_week_significant_earthquakes": "Significant Earthquakes (Past Week)",
    "past_week_m45_earthquakes": "Magnitude ≥4.5 (Past Week)",
    "past_week_m25_earthquakes": "Magnitude ≥2.5 (Past Week)",
    "past_week_m10_earthquakes": "Magnitude ≥1.0 (Past Week)",
    "past_week_all_earthquakes": "All Earthquakes (Past Week)",
    "past_month_significant_earthquakes": "Significant Earthquakes (Past Month)",
    "past_month_m45_earthquakes": "Magnitude ≥4.5 (Past Month)",
    "past_month_m25_earthquakes": "Magnitude ≥2.5 (Past Month)",
    "past_month_m10_earthquakes": "Magnitude ≥1.0 (Past Month)",
    "past_month_all_earthquakes": "All Earthquakes (Past Month)",
}

# Reverse mapping for UI input translation
FRIENDLY_NAME_TO_FEED_TYPE = {v: k for k, v in FEED_FRIENDLY_NAMES.items()}
