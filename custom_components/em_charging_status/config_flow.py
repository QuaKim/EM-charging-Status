import re
import aiohttp
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "em_charging_status"

def extract_location_id(user_input: str) -> str:
    match = re.search(r'(\d+)', user_input)
    return match.group(1) if match else user_input

async def async_get_location_name(location_id: str) -> str:
    url = f"https://www.electromaps.com/mapi/v2/locations/{location_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    # Coge el campo 'name' principal del cargador
                    return data.get("name") or f"Cargador EM {location_id}"
    except Exception:
        pass
    return f"Cargador EM {location_id}"

class EMChargingStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            raw_input = user_input.get("location_input", "").strip()
            location_id = extract_location_id(raw_input)

            if location_id.isdigit():
                await self.async_set_unique_id(f"em_charging_{location_id}")
                self._abort_if_unique_id_configured()

                # Obtenemos el nombre real desde la API
                location_name = await async_get_location_name(location_id)

                return self.async_create_entry(
                    title=location_name,
                    data={
                        "location_id": location_id,
                        "location_name": location_name
                    }
                )
            else:
                errors["base"] = "invalid_id"

        data_schema = vol.Schema({
            vol.Required("location_input"): str
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
