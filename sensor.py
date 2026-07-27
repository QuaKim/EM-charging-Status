import logging
from datetime import timedelta
import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)
DOMAIN = "em_charging_status"
SCAN_INTERVAL = timedelta(seconds=60)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    location_id = entry.data["location_id"]
    fallback_name = entry.data.get("location_name") or f"Punto EM {location_id}"

    coordinator = EMChargingCoordinator(hass, location_id, fallback_name)
    # Realiza la primera consulta a la API de forma sincrónica ANTES de crear los sensores
    await coordinator.async_config_entry_first_refresh()

    entities = []
    connectors = coordinator.data.get("connectors", [])

    for idx, conn in enumerate(connectors):
        conn_label = conn.get("visualRef") or conn.get("name") or f"Toma {idx + 1}"
        
        entities.append(EMChargingStatusSensor(coordinator, idx, location_id, conn_label, entry.entry_id))
        entities.append(EMChargingTimeSensor(coordinator, idx, location_id, conn_label, entry.entry_id))

    async_add_entities(entities)


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


class EMChargingStatusSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, index, location_id, conn_label, entry_id):
        super().__init__(coordinator)
        self._index = index
        self._conn_label = conn_label
        self._location_id = location_id
        self._attr_unique_id = f"{entry_id}_{index}_status"
#        self._attr_icon = "mdi:ev-station"

    @property #linea afegida canvi icon
    def icon(self):
        if not self.coordinator.data:
            return "mdi:ev-station"
            
        connectors = self.coordinator.data.get("connectors", [])
        if self._index < len(connectors):
            conn = connectors[self._index]
            
            conn_type = str(conn.get("type", "")).upper()
            if "CCS1" in conn_type or "T1_COMBO" in conn_type:
                return "mdi:ev-plug-ccs1"
            elif "CCS2" in conn_type or "T2_COMBO" in conn_type:
                return "mdi:ev-plug-ccs2"
            elif "TYPE 2" in conn_type or "MENNEKES" in conn_type or "IEC_62196_T2" in conn_type:
                return "mdi:ev-plug-type2"    
            elif "CHADEMO" in conn_type:
                return "mdi:ev-plug-chademo"
            elif "DOMESTIC" in conn_type or "SCHUKO" in conn_type:
                return "mdi:power-socket-eu"
            elif "TESLA" in conn_type:
                return "mdi:ev-plug-tesla"
            elif "T1" in conn_type or "TYPE 1" in conn_type or "J1772" in conn_type:
                return "mdi:ev-plug-type1"    

        return "mdi:ev-station"

    @property # linea afegida potencia a llista
    def name(self):
        """Devuelve el nombre del sensor en la UI incluyendo la potencia en kW."""
        connectors = self.coordinator.data.get("connectors", [])
        
        if self._index < len(connectors):
            conn = connectors[self._index]
            # Cogemos el nombre o referencia del conector
            ref = conn.get("name") or conn.get("visualRef") or f"Toma {self._index + 1}"
            kw = conn.get("kw")
            
            # Si hay kW, los juntamos con el nombre
            if kw:
                return f"{ref} ({kw} kW)"
            return str(ref)

        return f"Toma {self._index + 1}"
        
    @property # linea afegida potencia a detalls
    def extra_state_attributes(self):
        connectors = self.coordinator.data.get("connectors", [])
        if self._index < len(connectors):
            conn = connectors[self._index]
            return {
                "location_name": self.coordinator.location_name,
                "kw": conn.get("kw"),  # <-- Aquí ya se extrae el valor devuelto por la API
                "type": conn.get("type"),
                "status_updated_at": conn.get("status_updated_at"),
                "connector_name": conn.get("name") or conn.get("visualRef")
            }
        return {}

 #   @property  #linea afegida
 #   def name(self):
 #       return f"Estado {self._conn_label}"

#    @property
#    def name(self):
#        return f"{self.coordinator.location_name} - {self._conn_label}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, f"em_location_{self._location_id}")},
            name=self.coordinator.location_name,
            manufacturer="Electromaps",
            model=f"Location {self._location_id}",
        )

    @property
    def native_value(self):
        connectors = self.coordinator.data.get("connectors", [])
        if self._index < len(connectors):
            return connectors[self._index].get("status", "UNKNOWN")
        return "UNKNOWN"

    @property
    def extra_state_attributes(self):
        connectors = self.coordinator.data.get("connectors", [])
        if self._index < len(connectors):
            conn = connectors[self._index]
            return {
                "location_name": self.coordinator.location_name,
                "kw": conn.get("kw"),
                "type": conn.get("type"),
                "status_updated_at": conn.get("status_updated_at"),
                "connector_name": conn.get("name") or conn.get("visualRef")
            }
        return {}


class EMChargingTimeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, index, location_id, conn_label, entry_id):
        super().__init__(coordinator)
        self._index = index
        self._conn_label = conn_label
        self._location_id = location_id
        self._attr_unique_id = f"{entry_id}_{index}_time"
        self._attr_icon = "mdi:timer-outline"
        self._attr_native_unit_of_measurement = "min"

    @property
    def name(self):
        return f"Tiempo ocupado {self.coordinator.location_name} - {self._conn_label}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, f"em_location_{self._location_id}")},
            name=self.coordinator.location_name,
            manufacturer="Electromaps",
            model=f"Location {self._location_id}",
        )

    @property
    def native_value(self):
        connectors = self.coordinator.data.get("connectors", [])
        if self._index < len(connectors):
            conn = connectors[self._index]
            status = conn.get("status")
            updated_str = conn.get("status_updated_at")

            if status in ["OCCUPIED", "CHARGING"] and updated_str:
                try:
                    updated_dt = dt_util.parse_datetime(updated_str)
                    if updated_dt:
                        diff = abs((dt_util.now() - updated_dt).total_seconds())
                        return int(diff / 60)
                except Exception:
                    pass
        return 0