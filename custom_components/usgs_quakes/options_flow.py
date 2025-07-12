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


class UsgsQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            user_input[CONF_FEED_TYPE] = FRIENDLY_NAME_TO_FEED_TYPE[user_input[CONF_FEED_TYPE]]
            return self.async_create_entry(title="", data=user_input)

        current_feed = self.config_entry.data.get(CONF_FEED_TYPE)
        friendly_feed = FEED_FRIENDLY_NAMES.get(current_feed, current_feed)

        schema = vol.Schema({
            vol.Required(CONF_FEED_TYPE, default=friendly_feed): vol.In(list(FEED_FRIENDLY_NAMES.values())),
            vol.Required(CONF_LATITUDE, default=self.config_entry.data.get(CONF_LATITUDE)): vol.Coerce(float),
            vol.Required(CONF_LONGITUDE, default=self.config_entry.data.get(CONF_LONGITUDE)): vol.Coerce(float),
            vol.Required(CONF_RADIUS, default=self.config_entry.data.get(CONF_RADIUS, DEFAULT_RADIUS_IN_KM)): vol.Coerce(float),
            vol.Required(CONF_MINIMUM_MAGNITUDE, default=self.config_entry.data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)): vol.Coerce(float),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={},
        )
