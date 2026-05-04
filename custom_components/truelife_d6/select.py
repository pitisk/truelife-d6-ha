from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import COLOR_MODES, DOMAIN, DPS_COLOR_MODE
from .coordinator import TrueLifeD6Coordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: TrueLifeD6Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TrueLifeD6ColorModeSelect(coordinator, entry)])


class TrueLifeD6ColorModeSelect(CoordinatorEntity[TrueLifeD6Coordinator], SelectEntity):
    _attr_has_entity_name = True
    _attr_name = "LED Color Mode"
    _attr_icon = "mdi:palette"
    _attr_options = COLOR_MODES

    def __init__(self, coordinator: TrueLifeD6Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_color_mode"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="TrueLife AIR Diffuser D6",
            manufacturer="TrueLife",
            model="AIR Diffuser D6",
        )

    @property
    def current_option(self) -> str | None:
        value = self.coordinator.data.get(DPS_COLOR_MODE)
        # Device may report values not in our static list (e.g. "colourful2").
        # Return as-is so HA shows it; select options list acts as the write-only picker.
        return value if value in COLOR_MODES else value

    async def async_select_option(self, option: str) -> None:
        await self.coordinator.async_send_value(DPS_COLOR_MODE, option)
        await self.coordinator.async_request_refresh()
