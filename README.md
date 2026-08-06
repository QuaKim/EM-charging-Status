[![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg?style=flat-square)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/QuaKim/EM-charging-Status?style=flat-square)](https://github.com/QuaKim/EM-charging-Status/releases)
[![License](https://img.shields.io/github/license/QuaKim/EM-charging-Status?style=flat-square)](https://github.com/QuaKim/EM-charging-Status/blob/main/LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/QuaKim/EM-charging-Status?style=flat-square)](https://github.com/QuaKim/EM-charging-Status/commits/main)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-brightgreen?style=flat-square)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Donate-ff5e5b?style=flat-square&logo=ko-fi)](https://ko-fi.com/QuaKim)

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

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=QuaKim&repository=EM-charging-Status&category=integration)

### Opción 1: A través de HACS (Recomendado)

1. Abre **HACS** en el menú lateral de Home Assistant.
2. Haz clic en **Integraciones**.
3. Pulsa el menú de tres puntos `⋮` (arriba a la derecha) y selecciona **Repositorios personalizados**.
4. En **URL**, pega la dirección de tu repositorio en GitHub: `https://github.com/QuaKim/EM-charging-Status`
5. En **Categoría**, selecciona **Integración**.
6. Haz clic en **Añadir**.
7. Busca **EM Charging Status** en la lista de HACS y pulsa **Descargar**.
8. **Reinicia Home Assistant**.

### Opción 2: Instalación Manual

1. Descarga la última versión comprimida desde: https://github.com/QuaKim/evcharge_etecnic/  
2. Extrae el contenido y copia la carpeta `evcharge` en el directorio `custom_components` de tu servidor de Home Assistant:
   ```text
   config/
   └── custom_components/
       └── em_charing_status/
           ├── __init__.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           └── ...
3. En **Categoría**, selecciona **Integración**.
4. Haz clic en **Añadir**.
5. Busca **EM Charging Status** en la lista de HACS y pulsa **Descargar**.
6. **Reinicia Home Assistant**.

##  ⚙️ Pasos para añadir y configurar Puntos de Carga

Una vez instalada la integración y reiniciado Home Assistant, sigue estos pasos para vincular tu cuenta y añadir tus estaciones:

1. Ve a Ajustes → Dispositivos y servicios.
2. Haz clic en el botón Añadir integración (abajo a la derecha).
3. Busca EM Charging Status y selecciónala.

Añadir un punto de carga: 

1. Copia el enlace del punto de carga. o escribe su ID de estación, que aparece en la aplicación de Android/iOS, en el campo correspondiente para localizar el punto que deseas vincular.
2. Pulsa Enviar. La integración conectará con la API de Electromaps para añadir la estación.

El cargador aparecerá registrado como un nuevo Dispositivo, identificado con su Nombre, Calle e ID, e incluirá los sensores de sus tomas (Toma A, Toma B, etc.).

## 📊 Vista previa en Dashboard

La integración expone cada toma como un sensor individual, permitiendo crear tarjetas limpias y combinarlas con los datos de tu vehículo (batería, autonomía, climatización):

- **Estado directo:** Disponible / Ocupado / Fuera de servicio.
- **Formato de nombre:** `[Ref/Nombre Conector] ([Potencia] kW)`.

## 🤝 Contribuciones y Soporte

¡Cualquier reporte de errores, ideas o mejoras son bienvenidos!
Reportar un fallo o sugerencia: Abre un Issue en GitHub.
Aportar código: Envía una Pull Request.

## ☕ Apoya el proyecto
Si la integración te resulta útil y quieres apoyar su mantenimiento, ¡puedes invitarme a un café en [Ko-fi](https://ko-fi.com/QuaKim)!

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más información
