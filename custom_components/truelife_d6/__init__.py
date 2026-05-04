from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DEVICE_ID, CONF_LOCAL_KEY, DOMAIN
from .coordinator import TrueLifeD6Coordinator

PLATFORMS = [Platform.HUMIDIFIER, Platform.LIGHT, Platform.SWITCH, Platform.SELECT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = TrueLifeD6Coordinator(
        hass,
        device_id=entry.data[CONF_DEVICE_ID],
        host=entry.data[CONF_HOST],
        local_key=entry.data[CONF_LOCAL_KEY],
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
