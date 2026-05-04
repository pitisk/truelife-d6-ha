from datetime import timedelta
import logging
from typing import Any

import tinytuya

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, TUYA_PROTOCOL_VERSION, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class TrueLifeD6Coordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Manages polling and command sending for TrueLife AIR Diffuser D6."""

    def __init__(
        self,
        hass: HomeAssistant,
        device_id: str,
        host: str,
        local_key: str,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._device_id = device_id
        self._host = host
        self._local_key = local_key
        self._device: tinytuya.Device | None = None

    def _get_device(self) -> tinytuya.Device:
        if self._device is None:
            self._device = tinytuya.Device(
                dev_id=self._device_id,
                address=self._host,
                local_key=self._local_key,
                version=TUYA_PROTOCOL_VERSION,
            )
            self._device.set_socketTimeout(8)
            self._device.set_socketRetryLimit(2)
        return self._device

    def _reset_device(self) -> None:
        self._device = None

    def _fetch_status(self) -> dict[str, Any]:
        dev = self._get_device()
        result = dev.status()
        if "Error" in result:
            self._reset_device()
            raise UpdateFailed(f"Device error: {result['Error']} (code {result.get('Err')})")
        return result.get("dps", {})

    def _send_value(self, dps: str, value: Any) -> None:
        dev = self._get_device()
        result = dev.set_value(int(dps), value)
        if result and "Error" in result:
            self._reset_device()
            raise RuntimeError(f"Failed to set DPS {dps}: {result['Error']}")

    def _send_values(self, payload: dict[str, Any]) -> None:
        """Send multiple DPS values in one command."""
        dev = self._get_device()
        int_payload = {int(k): v for k, v in payload.items()}
        result = dev.set_multiple_values(int_payload)
        if result and "Error" in result:
            self._reset_device()
            raise RuntimeError(f"Failed to set multiple DPS: {result['Error']}")

    async def async_send_value(self, dps: str, value: Any) -> None:
        await self.hass.async_add_executor_job(self._send_value, dps, value)

    async def async_send_values(self, payload: dict[str, Any]) -> None:
        await self.hass.async_add_executor_job(self._send_values, payload)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self._fetch_status)
        except UpdateFailed:
            raise
        except Exception as err:
            self._reset_device()
            raise UpdateFailed(f"Unexpected error: {err}") from err
