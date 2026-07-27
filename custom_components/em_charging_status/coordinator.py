import logging
from datetime import timedelta
import aiohttp

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)


class EMChargingCoordinator(DataUpdateCoordinator):
    """Gestor centralizado de actualizaciones para evitar peticiones redundantes."""

    def __init__(self, hass, location_id, fallback_name):
        super().__init__(
            hass,
            _LOGGER,
            name=f"EM Charging {location_id}",
            update_interval=SCAN_INTERVAL,
        )
        self.location_id = location_id
        self.location_name = fallback_name
        self.url = f"https://www.electromaps.com/mapi/v2/locations/{location_id}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("name"):
                            self.location_name = data.get("name").strip()
                        return data
        except Exception as err:
            _LOGGER.error("Error consultando Electromaps (%s): %s", self.location_id, err)

        return {"connectors": []}