"""Options flow for USGS Quakes integration."""

from __future__ import annotations

import voluptuous as vol
import logging

from homeassistant.config_entries import OptionsFlow, ConfigEntry
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

_LOGGER = logging.getLogger(__name__)
_LOGGER.debug("USGS Quakes options_flow.py loaded")

FRIENDLY_NAME_TO_FEED_TYPE = {v: k for k, v in FEED_TYPE_FRIENDLY_NAMES.items()}
FRIENDLY_NAMES = list(FRIENDLY_NAME_TO_FEED_TYPE.keys())


class UsgsQuakesOptionsFlow(config_entries.OptionsFlow):
    """Handle USGS Quakes options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(data={
                CONF_RADIUS: float(user_input[CONF_RADIUS]),
                CONF_MINIMUM_MAGNITUDE: float(user_input[CONF_MINIMUM_MAGNITUDE]),
                CONF_FEED_TYPE: FRIENDLY_NAME_TO_FEED_TYPE[str(user_input[CONF_FEED_TYPE])],
            })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors={}
        )
