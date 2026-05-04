from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DPS_BRIGHTNESS, DPS_LIGHT
from .coordinator import TrueLifeD6Coordinator

# Tuya uses 0-1000, HA uses 0-255
TUYA_MAX_BRIGHTNESS = 1000


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: TrueLifeD6Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TrueLifeD6Light(coordinator, entry)])


class TrueLifeD6Light(CoordinatorEntity[TrueLifeD6Coordinator], LightEntity):
    _attr_has_entity_name = True
    _attr_name = "LED"
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(self, coordinator: TrueLifeD6Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_light"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="TrueLife AIR Diffuser D6",
            manufacturer="TrueLife",
            model="AIR Diffuser D6",
        )

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get(DPS_LIGHT, False))

    @property
    def brightness(self) -> int | None:
        raw = self.coordinator.data.get(DPS_BRIGHTNESS)
        if raw is None:
            return None
        return round(int(raw) / TUYA_MAX_BRIGHTNESS * 255)

    async def async_turn_on(self, **kwargs: Any) -> None:
        payload: dict[str, Any] = {DPS_LIGHT: True}
        if ATTR_BRIGHTNESS in kwargs:
            tuya_brightness = round(kwargs[ATTR_BRIGHTNESS] / 255 * TUYA_MAX_BRIGHTNESS)
            tuya_brightness = max(1, min(TUYA_MAX_BRIGHTNESS, tuya_brightness))
            payload[DPS_BRIGHTNESS] = tuya_brightness
        await self.coordinator.async_send_values(payload)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.coordinator.async_send_value(DPS_LIGHT, False)
        await self.coordinator.async_request_refresh()
