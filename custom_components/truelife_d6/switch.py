from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

# NOTE: DPS 2 and DPS 7 tested as read-only status flags (mirror power state).
# No writable switches confirmed yet. Kept for future extension.


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    pass
