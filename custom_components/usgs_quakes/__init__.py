"""USGS Quakes integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    PLATFORMS,
)

from .options_flow import UsgsQuakesOptionsFlow

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the USGS Quakes integration (legacy config)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up USGS Quakes from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Forward config to the platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload config entry if options are updated
    entry.async_on_unload(entry.add_update_listener(_update_listener))

    # Registrar el servicio para forzar update del feed
    async def handle_force_update(call: ServiceCall) -> None:
        """Servicio: Forzar actualización del feed USGS Quakes."""
        _LOGGER.debug("Llamado al servicio force_feed_update (manual)")
        entity_data = hass.data[DOMAIN].get(entry.entry_id)
        if not entity_data:
            _LOGGER.warning("USGS Quakes entry not initialized, cannot force update")
            return
        manager = entity_data.get("manager")
        if manager:
            _LOGGER.info("Forzando actualización manual del feed USGS Quakes…")
            await manager.async_update()
        else:
            _LOGGER.warning("USGS Quakes: No feed manager found to update")

    # Registrar el servicio sólo una vez
    if not hass.services.has_service(DOMAIN, "force_feed_update"):
        hass.services.async_register(DOMAIN, "force_feed_update", handle_force_update)

    return True


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    _LOGGER.debug("Reloading config entry %s due to options update", entry.entry_id)
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok

def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
    """Return the options flow handler for USGS Quakes."""
    return UsgsQuakesOptionsFlow(config_entry)
