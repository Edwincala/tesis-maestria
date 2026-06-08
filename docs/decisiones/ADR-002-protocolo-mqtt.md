# ADR-002: Uso de MQTT para la adquisición de datos

## Contexto

La plataforma debe recibir periódicamente mediciones eléctricas y climáticas provenientes inicialmente de un simulador desarrollado en Python y, posteriormente, de sensores conectados al sistema fotovoltaico.

Las mediciones incluyen, entre otras:

* Voltaje.
* Corriente.
* Potencia.
* Irradiancia solar.
* Temperatura ambiente.
* Temperatura del panel.
* Humedad relativa.

La adquisición de datos debe estar desacoplada del backend, de forma que los dispositivos puedan publicar información sin conocer directamente la ubicación, implementación o estado interno del servicio que procesará las mediciones.

También se requiere:

* Comunicación ligera.
* Bajo consumo de recursos.
* Capacidad de manejar publicaciones periódicas.
* Facilidad para incorporar múltiples dispositivos.
* Posibilidad de trabajar con conexiones inestables.
* Soporte para diferentes niveles de garantía de entrega.
* Compatibilidad con Python y Java.
* Posibilidad de ejecución local mediante Docker.

## Opciones consideradas

### Opción 1: Solicitudes HTTP desde cada dispositivo

Cada dispositivo o simulador enviaría una solicitud HTTP directamente al backend por cada medición.

#### Ventajas

* Implementación conocida y ampliamente soportada.
* Integración directa con Spring Boot.
* Facilidad para probar las solicitudes con herramientas HTTP.
* Respuestas inmediatas del servidor.

#### Desventajas

* Mayor acoplamiento entre los dispositivos y el backend.
* Los dispositivos deben conocer la dirección del backend.
* Cada publicación requiere establecer o mantener una comunicación HTTP.
* Menor tolerancia cuando el backend no está disponible.
* Mayor sobrecarga para mensajes pequeños y frecuentes.
* La incorporación de nuevos consumidores requiere modificaciones adicionales.

### Opción 2: WebSocket

Se podría mantener una conexión bidireccional persistente entre los dispositivos y el backend.

#### Ventajas

* Comunicación bidireccional.
* Baja latencia.
* Conexión persistente.
* Adecuado para actualización de interfaces en tiempo real.

#### Desventajas

* No está orientado específicamente a dispositivos IoT.
* Requiere gestionar directamente las conexiones activas.
* No ofrece por sí solo un modelo de publicación y suscripción.
* La gestión de reconexión y entrega debe implementarse en mayor medida.
* No desacopla completamente productores y consumidores.

### Opción 3: MQTT

Los productores publican mensajes en tópicos administrados por un broker. Los consumidores reciben los mensajes al suscribirse a dichos tópicos.

#### Ventajas

* Protocolo ligero.
* Modelo de publicación y suscripción.
* Bajo acoplamiento entre productores y consumidores.
* Adecuado para telemetría e IoT.
* Soporta diferentes niveles de calidad de servicio.
* Permite múltiples publicadores y suscriptores.
* Facilita la incorporación de nuevos dispositivos.
* Cuenta con bibliotecas para Python y Java.
* Puede utilizarse con Eclipse Mosquitto.
* Puede desplegarse localmente mediante Docker.

#### Desventajas

* Introduce un componente adicional: el broker.
* Requiere definir una estructura de tópicos.
* Requiere configurar autenticación y seguridad.
* Dependiendo del nivel de calidad de servicio, pueden presentarse mensajes duplicados.
* Los mensajes deben validarse en el consumidor.

## Decisión

Se utilizará MQTT como protocolo principal para la adquisición de datos eléctricos y climáticos.

Eclipse Mosquitto será utilizado como broker durante el desarrollo y las pruebas locales.

El simulador desarrollado en Python y los futuros dispositivos físicos actuarán como publicadores. El backend desarrollado con Spring Boot actuará como consumidor de telemetría.

MQTT se utilizará únicamente para adquisición de datos, estado de dispositivos y posibles eventos de campo. La comunicación entre Angular y Spring Boot continuará realizándose mediante HTTP o HTTPS y una API REST.

## Broker seleccionado

Se selecciona Eclipse Mosquitto debido a que:

* Es de código abierto.
* Tiene bajo consumo de recursos.
* Es ampliamente utilizado en soluciones MQTT.
* Puede ejecutarse mediante Docker.
* Permite configurar autenticación.
* Permite persistencia de mensajes.
* Soporta conexiones sin cifrar y cifradas.
* Facilita el desarrollo y las pruebas locales.

## Versión del protocolo

Se utilizará inicialmente MQTT 3.1.1 por su compatibilidad con bibliotecas comunes de Python y Java.

La adopción de MQTT 5 podrá evaluarse posteriormente si se requieren características como:

* Propiedades adicionales en los mensajes.
* Códigos de razón más detallados.
* Expiración de mensajes.
* Mejor control de sesiones.
* Metadatos avanzados.

## Estructura de tópicos

La estructura general será:

```text
solar/{deviceId}/{messageType}
```

Donde:

* `solar` identifica el dominio del proyecto.
* `{deviceId}` identifica el dispositivo.
* `{messageType}` identifica el tipo de mensaje.

### Tópicos iniciales

```text
solar/{deviceId}/telemetry
solar/{deviceId}/status
solar/{deviceId}/alerts
```

### Ejemplos

```text
solar/panel-001/telemetry
solar/panel-001/status
solar/panel-001/alerts
```

### Suscripción general del backend

Durante el MVP, el backend podrá suscribirse mediante comodines:

```text
solar/+/telemetry
solar/+/status
solar/+/alerts
```

El símbolo `+` representa un único nivel variable correspondiente al identificador del dispositivo.

No se recomienda utilizar inicialmente una suscripción completamente abierta como:

```text
solar/#
```

excepto durante pruebas controladas o tareas de diagnóstico.

## Convenciones para tópicos

Los tópicos deberán seguir estas reglas:

* Utilizar letras minúsculas.
* No incluir espacios.
* No incluir datos sensibles.
* No incluir la unidad de medida.
* Mantener una estructura consistente.
* Evitar nombres excesivamente largos.
* No utilizar identificadores que puedan cambiar frecuentemente.
* Usar el identificador técnico del dispositivo y no su nombre visual.

Ejemplo correcto:

```text
solar/panel-001/telemetry
```

Ejemplo no recomendado:

```text
Solar/Panel Principal Facultad/Mediciones en Tiempo Real
```

## Formato de los mensajes

Los mensajes serán enviados en formato JSON codificado en UTF-8.

### Ejemplo de telemetría

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
  "quality": "VALID"
}
```

## Campos de control

### `schemaVersion`

Identifica la versión del contrato del mensaje.

Permitirá introducir modificaciones futuras sin afectar inmediatamente a los consumidores existentes.

Ejemplo:

```json
"schemaVersion": "1.0"
```

### `messageId`

Identificador único del mensaje.

Permitirá detectar mensajes duplicados cuando se utilice QoS 1 o cuando un publicador vuelva a enviar información después de una reconexión.

Se recomienda utilizar UUID.

### `deviceId`

Identificador del dispositivo que generó la medición.

Debe coincidir con el identificador utilizado en el tópico.

### `timestamp`

Fecha y hora en la que se generó la medición.

Debe utilizar formato ISO 8601 y almacenarse en UTC.

Ejemplo:

```text
2026-06-07T14:30:00Z
```

### `quality`

Indica la calidad inicial del dato.

Valores propuestos:

```text
VALID
ESTIMATED
INVALID
MISSING
```

## Calidad de servicio

Se utilizará inicialmente QoS 1 para los mensajes de telemetría.

QoS 1 significa que el mensaje será entregado al menos una vez.

### Justificación

* Reduce el riesgo de perder mediciones.
* Es adecuado para información que será almacenada.
* Tiene menor complejidad que QoS 2.
* Es soportado ampliamente.
* El posible envío duplicado puede manejarse con `messageId`.

### Consecuencia

Con QoS 1 un mensaje puede ser entregado más de una vez. El backend deberá aplicar mecanismos de idempotencia o detección de duplicados.

El campo `messageId` deberá tener una restricción de unicidad en la base de datos o ser validado antes de insertar una medición.

## Uso de QoS por tipo de mensaje

| Tipo de mensaje  | QoS inicial | Justificación                           |
| ---------------- | ----------: | --------------------------------------- |
| Telemetría       |           1 | Evitar pérdida de mediciones            |
| Estado           |           1 | Conocer cambios de conexión             |
| Alertas          |           1 | Reducir el riesgo de pérdida de eventos |
| Comandos futuros |       1 o 2 | Dependerá de la criticidad              |

QoS 2 no se utilizará inicialmente debido a su mayor sobrecarga y complejidad.

## Mensajes retenidos

Los mensajes retenidos podrán utilizarse para el tópico de estado:

```text
solar/{deviceId}/status
```

Esto permitirá que un nuevo consumidor conozca el último estado reportado por un dispositivo.

No se utilizarán mensajes retenidos para telemetría histórica, debido a que MQTT solo conserva el último mensaje retenido por tópico y PostgreSQL será responsable de almacenar el historial.

## Última voluntad y testamento

Los dispositivos podrán configurar un mensaje Last Will and Testament para informar que perdieron la conexión de manera inesperada.

### Tópico

```text
solar/{deviceId}/status
```

### Mensaje sugerido

```json
{
  "deviceId": "panel-001",
  "timestamp": "2026-06-07T14:30:00Z",
  "status": "OFFLINE"
}
```

Cuando el dispositivo se conecte correctamente deberá publicar:

```json
{
  "deviceId": "panel-001",
  "timestamp": "2026-06-07T14:30:00Z",
  "status": "ONLINE"
}
```

El mensaje de estado podrá publicarse con la opción de mensaje retenido.

## Sesiones y reconexión

Los clientes MQTT deberán:

* Implementar reconexión automática.
* Esperar progresivamente entre intentos de reconexión.
* Volver a suscribirse cuando la sesión no se conserve.
* Registrar los errores de conexión.
* Evitar ciclos de reconexión sin pausa.
* No detener la aplicación ante una desconexión temporal.

El intervalo exacto de reconexión será configurable.

## Frecuencia de publicación

Durante las pruebas iniciales se utilizará una publicación cada cinco segundos.

La frecuencia será configurable mediante una variable de entorno, por ejemplo:

```env
SIMULATION_INTERVAL_SECONDS=5
```

La frecuencia definitiva dependerá de:

* Las capacidades de los sensores.
* El propósito del análisis.
* El volumen de almacenamiento.
* La estabilidad de la red.
* Las necesidades del modelo de aprendizaje.
* Los requerimientos de visualización.

## Validación de mensajes

El backend deberá validar como mínimo:

* El formato JSON.
* La existencia de `schemaVersion`.
* La existencia de `messageId`.
* La existencia de `deviceId`.
* La coincidencia entre el dispositivo del tópico y el mensaje.
* La existencia y formato de `timestamp`.
* Los tipos numéricos.
* Los rangos físicos definidos.
* Los campos obligatorios.
* La versión del esquema.

Un mensaje inválido no deberá detener al consumidor MQTT.

El sistema deberá:

1. Registrar el error.
2. Identificar el tópico de origen.
3. Conservar información suficiente para diagnóstico.
4. Evitar insertar datos inválidos como mediciones válidas.
5. Continuar procesando los mensajes siguientes.

## Manejo de mensajes inválidos

Durante el MVP, los mensajes inválidos se registrarán en los logs.

Posteriormente se podrá implementar:

* Una tabla de mensajes rechazados.
* Un tópico de mensajes inválidos.
* Una cola de mensajes fallidos.
* Métricas de calidad de datos.
* Reprocesamiento de mensajes.

Un tópico futuro podría ser:

```text
solar/system/dead-letter
```

Esta funcionalidad no es obligatoria durante la primera versión.

## Seguridad durante el desarrollo

En el entorno local se podrá comenzar con una configuración simplificada para validar la comunicación.

Sin embargo, no deberán mantenerse conexiones anónimas en un despliegue productivo.

La configuración futura deberá incluir:

* Usuarios y contraseñas.
* Listas de control de acceso.
* Restricciones por tópico.
* TLS.
* Certificados válidos.
* Rotación de credenciales.
* Bloqueo del acceso público innecesario.
* Puerto seguro MQTT, normalmente 8883.

Las credenciales no deberán almacenarse en el repositorio.

## Variables de entorno sugeridas

### Simulador

```env
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_CLIENT_ID=solar-simulator-panel-001
MQTT_TOPIC=solar/panel-001/telemetry
MQTT_QOS=1
SIMULATION_INTERVAL_SECONDS=5
DEVICE_ID=panel-001
```

### Backend

```env
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_CLIENT_ID=solar-backend-consumer
MQTT_TELEMETRY_TOPIC=solar/+/telemetry
MQTT_STATUS_TOPIC=solar/+/status
MQTT_ALERTS_TOPIC=solar/+/alerts
MQTT_QOS=1
```

Cuando el backend se ejecute dentro de Docker Compose, el host deberá corresponder al nombre del servicio del broker, por ejemplo:

```env
MQTT_HOST=mosquitto
```

No deberá utilizarse `localhost` para comunicarse con otro contenedor.

## Puerto seleccionado

Durante el desarrollo local se utilizará inicialmente:

```text
1883
```

Este puerto corresponde a MQTT sin TLS.

Para un entorno productivo se deberá considerar:

```text
8883
```

correspondiente a MQTT con TLS.

## Consecuencias positivas

* Los productores y consumidores quedan desacoplados.
* El backend no necesita conocer la implementación de los sensores.
* Los sensores no necesitan conocer la implementación del backend.
* Pueden incorporarse nuevos dispositivos sin modificar los existentes.
* Pueden agregarse consumidores adicionales.
* Se reduce la sobrecarga frente a publicaciones HTTP frecuentes.
* Es posible controlar la garantía de entrega mediante QoS.
* Mosquitto puede ejecutarse localmente mediante Docker.
* El simulador y los sensores reales podrán utilizar el mismo contrato.

## Consecuencias negativas

* Se agrega la dependencia de un broker.
* Será necesario monitorear la disponibilidad de Mosquitto.
* QoS 1 puede producir mensajes duplicados.
* La seguridad requiere configuración adicional.
* Los errores de contrato pueden no ser visibles inmediatamente para el publicador.
* Se requiere coordinación sobre tópicos y esquemas.

## Riesgos

* Colisión entre identificadores de clientes MQTT.
* Mensajes duplicados.
* Pérdida de conexión.
* Acumulación de mensajes.
* Publicación en tópicos incorrectos.
* Inconsistencia entre `deviceId` y tópico.
* Uso de credenciales inseguras.
* Acceso no autorizado a tópicos.
* Incompatibilidad entre versiones del esquema.
* Diferencias en el tratamiento de fechas y números.

## Medidas de mitigación

* Utilizar identificadores de cliente únicos.
* Incluir `messageId`.
* Aplicar restricciones de unicidad.
* Configurar reconexión automática.
* Validar el tópico y el contenido.
* Versionar el esquema.
* Utilizar UTC.
* Definir pruebas de contrato.
* Implementar autenticación en entornos no locales.
* Utilizar TLS en producción.
* Documentar todos los tópicos.
* Registrar errores de procesamiento.

## Pruebas requeridas

La decisión deberá validarse mediante:

* Publicación manual con un cliente MQTT.
* Publicación desde Python.
* Suscripción desde Spring Boot.
* Prueba de mensajes con campos faltantes.
* Prueba de tipos de datos incorrectos.
* Prueba de mensajes duplicados.
* Prueba de desconexión y reconexión.
* Prueba de varios dispositivos.
* Prueba del mensaje de última voluntad.
* Prueba de persistencia en PostgreSQL.

## Criterios para revisar esta decisión

Esta decisión deberá revisarse si:

* MQTT no satisface los requisitos de seguridad del despliegue.
* Se requiere procesamiento de eventos a una escala considerablemente mayor.
* Se necesitan capacidades de retención y reproducción más avanzadas.
* Se requiere conservar todos los eventos directamente en la plataforma de mensajería.
* Se incorporan requisitos estrictos de orden global.
* Se cambia el entorno de infraestructura.
* Los sensores seleccionados no soportan MQTT.

## Resultado esperado

El simulador y los futuros sensores deberán publicar mensajes sin depender directamente del backend.

El backend deberá recibir las mediciones mediante una suscripción similar a:

```text
solar/+/telemetry
```

y procesarlas de manera segura, validada e idempotente antes de almacenarlas.
