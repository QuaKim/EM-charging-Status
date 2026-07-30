# ⚡ Electromaps Public Charger Tracker for Home Assistant

Una integración ligera y eficiente para Home Assistant que te permite monitorizar en tiempo real la disponibilidad, potencia y estado de tus puntos de carga públicos favoritos de **Electromaps**, sin necesidad de abrir la aplicación móvil ni depender de interfaces externas.

Diseñada especialmente para propietarios de vehículos eléctricos sin punto de carga propio en garaje que dependen 100% de la infraestructura pública.

---

## ✨ Características

* **Monitoreo en tiempo real:** Muestra el estado actualizado (`AVAILABLE`, `OCCUPIED`, `OUT_OF_SERVICE`, etc.) de cada conector individual.
* **Potencia visible en el nombre:** Identifica de un vistazo las tomas según su velocidad de carga (ej. `000126 (180 kW)`, `000127 (50 kW)` o `000132 (22 kW)`).
* **Iconos dinámicos (MDI):** Mapeo automático de conectores locales (CCS2, Type 2 / Mennekes, CHAdeMO, Schuko, Tesla) para una identificación visual rápida en el Dashboard.
* **Atributos enriquecidos:** Extrae la fecha y hora de la última actualización de estado (`status_updated_at`) para poder calcular el tiempo exacto que lleva ocupada una toma mediante sensores de plantilla o lanzar automatizaciones cuando esté a punto de liberarse.
* **Filosofía KISS (Keep It Simple, Stupid):** Sin dependencias pesadas ni configuraciones complejas. Utiliza `DataUpdateCoordinator` nativo para minimizar las llamadas a la API y el consumo de recursos.

---

## 🛠️ Instalación

### Opción 1: A través de HACS (Recomendado)

1. Abre **HACS** en tu instancia de Home Assistant.
2. Ve al menú superior derecho (tres puntos) y selecciona **Repositorios personalizados**.
3. Añade la URL de este repositorio: `https://github.com/QuaKim/EM-charging-Status`
4. En **Categoría**, selecciona **Integración**.
5. Haz clic en **Añadir**, busca *Electromaps Public Charging* e instala la integración.
6. Reinicia Home Assistant.

### Opción 2: Instalación Manual

1. Descarga el código de este repositorio.
2. Copia la carpeta `custom_components/em_charging_status` dentro del directorio `custom_components/` de tu configuración de Home Assistant.
3. Reinicia Home Assistant.

---

## 📊 Vista previa en Dashboard

La integración expone cada toma como un sensor individual, permitiendo crear tarjetas limpias y combinarlas con los datos de tu vehículo (batería, autonomía, climatización):

- **Estado directo:** Disponible / Ocupado / Fuera de servicio.
- **Formato de nombre:** `[Ref/Nombre Conector] ([Potencia] kW)`.
