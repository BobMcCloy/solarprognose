"""Sensor platform for Solarprognose."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfPower, UnitOfEnergy

from .const import DOMAIN, CONF_NAME, CONF_ITEM_ID

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    name_prefix = entry.data[CONF_NAME]
    item_id = entry.data[CONF_ITEM_ID]

    sensors = [
        SolarprognoseSensor(coordinator, name_prefix, item_id, "current_hour", "Aktuelle Stunde", SensorDeviceClass.POWER, UnitOfPower.WATT, "mdi:sun-clock"),
        SolarprognoseSensor(coordinator, name_prefix, item_id, "next_hour", "Nächste Stunde", SensorDeviceClass.POWER, UnitOfPower.WATT, "mdi:sun-clock-outline"),
        SolarprognoseSensor(coordinator, name_prefix, item_id, "today", "Heute", SensorDeviceClass.ENERGY, UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power"),
        SolarprognoseSensor(coordinator, name_prefix, item_id, "remaining_today", "Rest Heute", SensorDeviceClass.ENERGY, UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power-variant"),
        SolarprognoseSensor(coordinator, name_prefix, item_id, "tomorrow", "Morgen", SensorDeviceClass.ENERGY, UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power"),
        SolarprognoseSensor(coordinator, name_prefix, item_id, "day_after_tomorrow", "Übermorgen", SensorDeviceClass.ENERGY, UnitOfEnergy.KILO_WATT_HOUR, "mdi:solar-power"),
    ]
    async_add_entities(sensors)

class SolarprognoseSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Solarprognose Sensor."""

    def __init__(self, coordinator, name_prefix, item_id, data_key, suffix_name, device_class, unit, icon):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._data_key = data_key
        self._attr_name = f"{name_prefix} Prognose {suffix_name}"
        self._attr_unique_id = f"solar_{item_id}_{data_key}"
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = unit
        self._attr_icon = icon

        # Damit alle Sensoren einer Anlage im Dashboard gruppiert werden:
        self._attr_device_info = {
            "identifiers": {(DOMAIN, item_id)},
            "name": f"Solarprognose {name_prefix}",
            "manufacturer": "Solarprognose.de",
            "model": "API V1",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data is not None:
            return self.coordinator.data.get(self._data_key)
        return None
