from homeassistant import config_entries
import voluptuous as vol

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_RADIUS
from .const import (
    DOMAIN,
    FEED_FRIENDLY_NAMES,
    FRIENDLY_NAME_TO_FEED_TYPE,
    DEFAULT_RADIUS_IN_KM,
    DEFAULT_MINIMUM_MAGNITUDE,
)

CONF_FEED_TYPE = "feed_type"
CONF_MINIMUM_MAGNITUDE = "minimum_magnitude"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for USGS Quakes."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            # Convert friendly name back to internal ID
            user_input[CONF_FEED_TYPE] = FRIENDLY_NAME_TO_FEED_TYPE[user_input[CONF_FEED_TYPE]]
            return self.async_create_entry(title="USGS Quakes", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_FEED_TYPE): vol.In(list(FEED_FRIENDLY_NAMES.values())),
            vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): vol.Coerce(float),
            vol.Required(CONF_RADIUS, default=DEFAULT_RADIUS_IN_KM): vol.Coerce(float),
            vol.Required(CONF_MINIMUM_MAGNITUDE, default=DEFAULT_MINIMUM_MAGNITUDE): vol.Coerce(float),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={},
        )
