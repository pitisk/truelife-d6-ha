from typing import Any

from homeassistant.components.humidifier import HumidifierEntity, HumidifierEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DPS_MIST_LEVEL, DPS_POWER, MIST_LEVELS
from .coordinator import TrueLifeD6Coordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: TrueLifeD6Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TrueLifeD6Humidifier(coordinator, entry)])


class TrueLifeD6Humidifier(CoordinatorEntity[TrueLifeD6Coordinator], HumidifierEntity):
    _attr_has_entity_name = True
    _attr_name = None  # uses device name as entity name
    _attr_supported_features = HumidifierEntityFeature.MODES
    _attr_available_modes = MIST_LEVELS
    _attr_min_humidity = 0
    _attr_max_humidity = 100

    def __init__(self, coordinator: TrueLifeD6Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_humidifier"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="TrueLife AIR Diffuser D6",
            manufacturer="TrueLife",
            model="AIR Diffuser D6",
        )

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DPS_POWER, False))

    @property
    def mode(self) -> str | None:
        return self.coordinator.data.get(DPS_MIST_LEVEL)

    @property
    def current_humidity(self) -> int | None:
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(DPS_POWER, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(DPS_POWER, False)
        await self.coordinator.async_request_refresh()

    async def async_set_mode(self, mode: str) -> None:
        await self.coordinator.async_send_value(DPS_MIST_LEVEL, mode)
        await self.coordinator.async_request_refresh()
