# Topics MQTT

## 1. Estructura general

La estructura de topics MQTT del proyecto será:

```text
solar/{deviceId}/{messageType}
```
Donde:

- `solar`: dominio general del sistema.
- `{deviceId}`: identificador técnico del panel, sensor o fuente de datos.
- `{messageType}`: tipo de mensaje publicado.

## 2. Topics iniciales
| Topic	| Descripción |	Publicador | Suscriptor|
|-------|-------------|------------|-----------|
| `solar/{deviceId}/telemetry` | Mediciones eléctricas y climáticas | Simulador Python / sensores | Backend Spring Boot |
| `solar/{deviceId}/status` |	Estado de conexión del dispositivo | Simulador Python / sensores | Backend Spring Boot |
| `solar/{deviceId}/alerts` | Eventos o alertas generadas en campo | Simulador Python / sensores | Backend Spring Boot |

## 3. Ejemplos
```text
solar/panel-001/telemetry
solar/panel-001/status
solar/panel-001/alerts
```

## 4. Suscripciones del backend
```text
solar/+/telemetry
solar/+/status
solar/+/alerts
```

## 5. Reglas
- Usar minúsculas.
- No usar espacios.
- No incluir unidades de medida.
- No incluir datos sensibles.
- El `deviceId` del topic debe coincidir con el `deviceId` del mensaje JSON.
- No usar `solar/#` salvo para diagnóstico local.