from typing import Any

import voluptuous as vol
import tinytuya

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_DEVICE_ID, CONF_LOCAL_KEY, DEFAULT_NAME, DOMAIN, TUYA_PROTOCOL_VERSION


def _test_connection(host: str, device_id: str, local_key: str) -> bool:
    d = tinytuya.Device(device_id, host, local_key, version=TUYA_PROTOCOL_VERSION)
    d.set_socketTimeout(8)
    d.set_socketRetryLimit(1)
    result = d.status()
    return "Error" not in result


class TrueLifeD6ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                ok = await self.hass.async_add_executor_job(
                    _test_connection,
                    user_input[CONF_HOST],
                    user_input[CONF_DEVICE_ID],
                    user_input[CONF_LOCAL_KEY],
                )
                if ok:
                    await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title=DEFAULT_NAME, data=user_input)
                errors["base"] = "cannot_connect"
            except config_entries.data_entry_flow.AbortFlow:
                raise
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default="10.20.101.164"): str,
                    vol.Required(CONF_DEVICE_ID, default="bf339ed9db804ab0adaeco"): str,
                    vol.Required(CONF_LOCAL_KEY): str,
                }
            ),
            errors=errors,
        )
