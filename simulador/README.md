# Simulador Python de sensores fotovoltaicos

Módulo responsable de generar mediciones eléctricas y climáticas simuladas y publicarlas en un broker MQTT para validar el flujo de adquisición de datos de la plataforma de monitoreo solar.

## Funcionalidades

- Generación de voltaje, corriente y potencia.
- Generación de irradiancia solar.
- Generación de temperatura ambiente y del panel.
- Generación de humedad relativa.
- Construcción de mensajes JSON versionados.
- Identificadores únicos mediante `messageId`.
- Marcas de tiempo ISO 8601 en UTC.
- Publicación MQTT con QoS configurable.
- Publicación de estado `ONLINE` y `OFFLINE`.
- Last Will and Testament para desconexiones inesperadas.
- Escenarios normales y anómalos.
- Pruebas unitarias con `pytest`.

## Estructura

```text
simulador/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── generator.py
│   ├── main.py
│   ├── mqtt_client.py
│   ├── scenarios.py
│   └── schemas.py
├── tests/
│   ├── __init__.py
│   ├── test_generator.py
│   ├── test_scenarios.py
│   └── test_schemas.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.12 o compatible.
- Broker MQTT accesible.
- `pip`.
- `venv`.

En Ubuntu o WSL:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mosquitto-clients jq
```

## Instalación desde WSL o Linux

Ubícate en la carpeta del simulador:

```bash
cd ~/tesis-maestria/tesis-maestria/simulador
```

Crea el entorno virtual:

```bash
python3 -m venv .venv
```

Actívalo:

```bash
source .venv/bin/activate
```

Actualiza `pip` e instala las dependencias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para salir del entorno virtual:

```bash
deactivate
```

## Configuración

Crea el archivo local de variables de entorno:

```bash
cp .env.example .env
```

Configuración recomendada cuando Python se ejecuta directamente desde WSL y Mosquitto está en Docker con el puerto `1884` publicado:

```env
DEVICE_ID=panel-001

MQTT_HOST=localhost
MQTT_PORT=1884
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_CLIENT_ID=solar-simulator-panel-001
MQTT_QOS=1
MQTT_KEEPALIVE_SECONDS=60

SIMULATION_INTERVAL_SECONDS=5
SIMULATION_SCENARIO=NORMAL
SIMULATION_RANDOM_SEED=42

PANEL_RATED_POWER_W=350
PANEL_REFERENCE_VOLTAGE_V=36
PANEL_TEMPERATURE_COEFFICIENT=-0.004
```

No se debe subir `.env` al repositorio. Solo debe versionarse `.env.example`.

## Variables de entorno

| Variable | Descripción | Valor inicial |
|---|---|---|
| `DEVICE_ID` | Identificador del dispositivo | `panel-001` |
| `MQTT_HOST` | Host del broker MQTT | `localhost` |
| `MQTT_PORT` | Puerto MQTT | `1884` desde WSL |
| `MQTT_CLIENT_ID` | Identificador único del cliente | `solar-simulator-panel-001` |
| `MQTT_QOS` | Calidad de servicio MQTT | `1` |
| `MQTT_KEEPALIVE_SECONDS` | Intervalo keep-alive | `60` |
| `SIMULATION_INTERVAL_SECONDS` | Intervalo entre publicaciones | `5` |
| `SIMULATION_SCENARIO` | Escenario por defecto | `NORMAL` |
| `SIMULATION_RANDOM_SEED` | Semilla opcional para reproducibilidad | `42` |
| `PANEL_RATED_POWER_W` | Potencia nominal del panel | `350` |
| `PANEL_REFERENCE_VOLTAGE_V` | Voltaje de referencia | `36` |
| `PANEL_TEMPERATURE_COEFFICIENT` | Coeficiente térmico | `-0.004` |

## Iniciar el broker MQTT

Desde la raíz del repositorio:

```bash
cd docker
docker compose up -d
docker compose ps
```

La configuración actual publica Mosquitto así:

```text
localhost:1884 → contenedor mosquitto:1883
```

## Escuchar mensajes MQTT

Desde WSL:

```bash
mosquitto_sub \
  -h localhost \
  -p 1884 \
  -t "solar/#" \
  -q 1 \
  -v
```

Solo telemetría:

```bash
mosquitto_sub \
  -h localhost \
  -p 1884 \
  -t "solar/+/telemetry" \
  -q 1 \
  -v
```

Solo estado:

```bash
mosquitto_sub \
  -h localhost \
  -p 1884 \
  -t "solar/+/status" \
  -q 1 \
  -v
```

Usando el cliente del contenedor:

```bash
docker exec -it solar-mosquitto \
  mosquitto_sub \
  -h localhost \
  -p 1883 \
  -t "solar/#" \
  -q 1 \
  -v
```

## Ejecutar el simulador

Activa primero el entorno virtual:

```bash
source .venv/bin/activate
```

Ejecutar una sola publicación:

```bash
python -m src.main --scenario NORMAL --once
```

Ejecutar publicaciones continuas:

```bash
python -m src.main --scenario NORMAL
```

Detener la ejecución:

```text
Ctrl + C
```

## Escenarios disponibles

| Escenario | Comportamiento esperado |
|---|---|
| `NORMAL` | Operación normal del panel |
| `CLOUDY` | Menor irradiancia y potencia; mayor humedad |
| `SHADING` | Reducción de corriente y potencia por sombreado |
| `OVERHEATING` | Temperatura del panel elevada y menor rendimiento |
| `ELECTRICAL_FAULT` | Caída significativa de voltaje, corriente y potencia |
| `COMMUNICATION_LOSS` | Omisión temporal de publicaciones de telemetría |

Ejemplos:

```bash
python -m src.main --scenario CLOUDY
python -m src.main --scenario SHADING
python -m src.main --scenario OVERHEATING
python -m src.main --scenario ELECTRICAL_FAULT
python -m src.main --scenario COMMUNICATION_LOSS
```

## Contrato MQTT

Tópico de telemetría:

```text
solar/{deviceId}/telemetry
```

Tópico de estado:

```text
solar/{deviceId}/status
```

Ejemplo de mensaje:

```json
{
  "schemaVersion": "1.0",
  "messageId": "3b28a30b-1d27-49c7-974d-d1936ca3203e",
  "deviceId": "panel-001",
  "timestamp": "2026-06-07T14:30:00Z",
  "voltage": 32.5,
  "current": 7.8,
  "power": 253.5,
  "irradiance": 780.0,
  "ambientTemperature": 19.2,
  "panelTemperature": 35.4,
  "relativeHumidity": 67.0,
  "quality": "VALID",
  "scenario": "NORMAL"
}
```

## Pruebas

Ejecutar todas las pruebas:

```bash
pytest
```

Modo detallado:

```bash
pytest -v
```

Ejecutar solo las pruebas de escenarios:

```bash
pytest tests/test_scenarios.py -v
```

Validar sintaxis de todos los módulos:

```bash
python -m compileall -q src
```

## Ejecución con Docker

Para ejecutar el simulador dentro de Docker se requiere un `Dockerfile` y un servicio `simulator` en `docker/docker-compose.yml`.

Dentro de Docker Compose, el broker debe configurarse con el nombre del servicio y el puerto interno:

```env
MQTT_HOST=mosquitto
MQTT_PORT=1883
```

No debe utilizarse `localhost`, ya que dentro del contenedor ese nombre apunta al propio simulador.

Ejemplo de ejecución, una vez configurado el servicio:

```bash
cd docker
docker compose up -d mosquitto postgres simulator
```

Ver logs:

```bash
docker compose logs -f simulator
```

Ejecutar una publicación puntual:

```bash
docker compose run --rm simulator \
  python -m src.main --scenario NORMAL --once
```

## Prueba de varios dispositivos

Terminal 1:

```bash
DEVICE_ID=panel-001 \
MQTT_CLIENT_ID=solar-simulator-panel-001 \
python -m src.main --scenario NORMAL
```

Terminal 2:

```bash
DEVICE_ID=panel-002 \
MQTT_CLIENT_ID=solar-simulator-panel-002 \
python -m src.main --scenario CLOUDY
```

Cada instancia debe utilizar un `MQTT_CLIENT_ID` único.

## Problemas frecuentes

### Conexión rechazada

Verifica que el broker esté activo:

```bash
cd ../docker
docker compose ps
docker compose logs mosquitto
```

Comprueba el puerto publicado:

```bash
nc -vz localhost 1884
```

### No aparecen mensajes

Verifica que el suscriptor escuche el tópico correcto:

```text
solar/#
```

Confirma además que `.env` use:

```env
MQTT_HOST=localhost
MQTT_PORT=1884
```

### Un simulador desconecta a otro

Esto ocurre cuando ambos usan el mismo `MQTT_CLIENT_ID`. Configura un identificador diferente para cada instancia.

## Limitaciones actuales

- El modelo climático es una aproximación para pruebas de integración.
- No representa una estación meteorológica real ni todos los microclimas de Bogotá.
- Los rangos deberán ajustarse cuando se conozcan las especificaciones definitivas de los sensores y del panel.
- La persistencia y validación definitiva serán responsabilidad del backend Spring Boot.