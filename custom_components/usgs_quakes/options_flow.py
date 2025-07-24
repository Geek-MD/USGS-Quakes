"""Options flow for USGS Quakes integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_RADIUS,
    CONF_MINIMUM_MAGNITUDE,
    CONF_FEED_TYPE,
    DEFAULT_RADIUS,
    DEFAULT_MINIMUM_MAGNITUDE,
    VALID_FEED_TYPES,
    FEED_TYPE_FRIENDLY_NAMES,
)

from typing import Any

FRIENDLY_NAME_TO_FEED_TYPE = {v: k for k, v in FEED_TYPE_FRIENDLY_NAMES.items()}
FRIENDLY_NAMES = list(FRIENDLY_NAME_TO_FEED_TYPE.keys())

import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.error("USGS Quakes options_flow.py loaded")

class UsgsQuakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle USGS Quakes options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        errors: dict[str, str] = {}

        data = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            try:
                radius = float(user_input.get(CONF_RADIUS, DEFAULT_RADIUS))
                minimum_magnitude = float(user_input.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE))
                feed_type = FRIENDLY_NAME_TO_FEED_TYPE[str(user_input[CONF_FEED_TYPE])]
            except (ValueError, TypeError, KeyError):
                errors["base"] = "invalid_input"
            else:
                return self.async_create_entry(
                    title="USGS Quakes Options",
                    data={
                        CONF_RADIUS: radius,
                        CONF_MINIMUM_MAGNITUDE: minimum_magnitude,
                        CONF_FEED_TYPE: feed_type,
                    },
                )

        selected_feed_type = FEED_TYPE_FRIENDLY_NAMES.get(
            data.get(CONF_FEED_TYPE, VALID_FEED_TYPES[0]),
            FEED_TYPE_FRIENDLY_NAMES[VALID_FEED_TYPES[0]],
        )

        options_schema = vol.Schema(
            {
                vol.Required(CONF_RADIUS, default=data.get(CONF_RADIUS, DEFAULT_RADIUS)): vol.Coerce(float),
                vol.Required(CONF_MINIMUM_MAGNITUDE, default=data.get(CONF_MINIMUM_MAGNITUDE, DEFAULT_MINIMUM_MAGNITUDE)): vol.Coerce(float),
                vol.Required(CONF_FEED_TYPE, default=selected_feed_type): vol.In(FRIENDLY_NAMES),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
        )
