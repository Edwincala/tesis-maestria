# Variables de monitoreo

## 1. Objetivo

Definir las variables mínimas necesarias para evaluar el comportamiento
eléctrico del panel fotovoltaico y su relación con las condiciones climáticas.

## 2. Variables eléctricas

### Voltaje DC

- Campo: `voltage`
- Unidad: voltios, V.
- Tipo: número decimal.
- Descripción: diferencia de potencial medida en la salida del panel.
- Validación inicial: valor mayor o igual que cero.

### Corriente DC

- Campo: `current`
- Unidad: amperios, A.
- Tipo: número decimal.
- Descripción: corriente suministrada por el panel.
- Validación inicial: valor mayor o igual que cero.

### Potencia DC

- Campo: `power`
- Unidad: vatios, W.
- Tipo: número decimal.
- Descripción: potencia instantánea generada por el panel.

Puede recibirse directamente desde el dispositivo o calcularse como:

$P = V × I$

### Energía acumulada

- Campo: `energy`
- Unidad: Wh o kWh.
- Tipo: número decimal.
- Descripción: energía producida durante un intervalo de tiempo.
- Naturaleza: variable calculada a partir de la potencia.

## 3. Variables climáticas

### Irradiancia solar

- Campo: `irradiance`
- Unidad: $\text{W}/\text{m}^2$.
- Tipo: número decimal.
- Descripción: radiación solar recibida por unidad de superficie.
- Validación inicial: valor mayor o igual que cero.

### Temperatura ambiente

- Campo: `ambientTemperature`
- Unidad: °C.
- Tipo: número decimal.
- Descripción: temperatura del aire alrededor del sistema.

### Temperatura del panel

- Campo: `panelTemperature`
- Unidad: °C.
- Tipo: número decimal.
- Descripción: temperatura superficial o posterior del módulo fotovoltaico.

### Humedad relativa

- Campo: `relativeHumidity`
- Unidad: porcentaje.
- Tipo: número decimal.
- Rango válido: entre 0 y 100.

## 4. Variables de identificación y control

### Identificador del dispositivo

- Campo: `deviceId`
- Tipo: texto.
- Ejemplo: `panel-001`.

### Marca de tiempo

- Campo: `timestamp`
- Tipo: fecha y hora.
- Formato: ISO 8601.
- Zona horaria recomendada para almacenamiento: UTC.

### Estado del dispositivo

- Campo: `status`
- Tipo: texto.
- Valores iniciales:
  - `ONLINE`
  - `OFFLINE`
  - `WARNING`
  - `ERROR`

### Calidad del dato

- Campo: `quality`
- Tipo: texto.
- Valores iniciales:
  - `VALID`
  - `ESTIMATED`
  - `INVALID`
  - `MISSING`

## 5. Frecuencia de muestreo

Durante la simulación inicial se propone:

- Generación de una medición cada 5 segundos.
- Frecuencia configurable mediante variable de entorno.
- Almacenamiento de todas las mediciones durante las pruebas.
- Posibilidad futura de agregar procesos de agregación por minuto, hora y día.

La frecuencia final dependerá de las capacidades de los sensores, del medio de
comunicación y de los requerimientos del estudio.

## 6. Reglas iniciales de validación

- `deviceId` no puede ser nulo ni vacío.
- `timestamp` debe tener un formato válido.
- El voltaje no puede ser negativo.
- La corriente no puede ser negativa.
- La potencia no puede ser negativa.
- La irradiancia no puede ser negativa.
- La humedad debe estar entre 0 y 100.
- Los valores fuera de rango deben registrarse sin provocar la caída del
  consumidor MQTT.
- Los mensajes incompletos deben quedar registrados en los logs.