# ADR-003: Uso de PostgreSQL como base de datos principal

## Contexto

La plataforma requiere almacenar información estructurada relacionada con:

* Usuarios.
* Roles y permisos.
* Dispositivos.
* Paneles solares.
* Mediciones eléctricas.
* Mediciones climáticas.
* Estados de conexión.
* Alertas.
* Configuraciones.
* Predicciones futuras.
* Resultados del modelo de aprendizaje continuo.

Los datos presentan relaciones claras. Por ejemplo:

* Un dispositivo puede generar muchas mediciones.
* Un usuario puede tener uno o varios roles.
* Una alerta pertenece a un dispositivo.
* Una predicción puede asociarse a una variable y un intervalo temporal.
* Las mediciones deben conservar integridad y trazabilidad.

La plataforma también deberá realizar consultas históricas por:

* Dispositivo.
* Variable.
* Rango de fechas.
* Estado.
* Calidad del dato.
* Tipo de medición.

La tecnología seleccionada debe integrarse adecuadamente con Spring Boot, permitir el uso de transacciones, restricciones, índices, migraciones y consultas agregadas.

## Opciones consideradas

### Opción 1: MySQL

MySQL es una base de datos relacional ampliamente utilizada y compatible con Spring Boot.

#### Ventajas

* Amplia adopción.
* Buena documentación.
* Integración con Java.
* Facilidad de uso.
* Experiencia previa del desarrollador con esta tecnología.

#### Desventajas

* PostgreSQL ofrece características más amplias para ciertos tipos de datos, consultas analíticas y extensiones.
* Algunas capacidades avanzadas pueden requerir tratamientos diferentes.
* La selección de PostgreSQL se adapta mejor al crecimiento previsto del proyecto.

### Opción 2: MongoDB

MongoDB permitiría almacenar los mensajes de telemetría como documentos JSON.

#### Ventajas

* Flexibilidad del esquema.
* Inserción directa de estructuras similares a los mensajes MQTT.
* Facilidad para almacenar documentos con campos variables.
* Escalabilidad horizontal.

#### Desventajas

* Los datos principales del sistema tienen relaciones bien definidas.
* La autenticación, los dispositivos, las alertas y las mediciones requieren integridad referencial.
* La flexibilidad excesiva puede permitir inconsistencias en nombres y tipos de campos.
* El proyecto requiere consultas relacionales y agregaciones estructuradas.
* Sería necesario gestionar manualmente algunas relaciones.

### Opción 3: Base de datos especializada en series temporales

Se consideró utilizar una base de datos orientada específicamente a series temporales.

#### Ventajas

* Alto rendimiento para grandes volúmenes de mediciones.
* Funciones especializadas para agregaciones temporales.
* Retención y compresión de datos.
* Consultas optimizadas por intervalos.

#### Desventajas

* Introduce una tecnología adicional.
* Puede aumentar la complejidad del proyecto.
* El volumen inicial del MVP no justifica necesariamente una plataforma independiente.
* También se necesita almacenar información transaccional y relacional.

### Opción 4: PostgreSQL

PostgreSQL es un sistema de gestión de bases de datos relacional de código abierto con soporte para transacciones, restricciones, índices, tipos avanzados y consultas complejas.

#### Ventajas

* Integridad referencial.
* Transacciones ACID.
* Integración con Spring Data JPA.
* Soporte para consultas agregadas.
* Soporte para índices.
* Buen manejo de fechas y zonas horarias.
* Tipos de datos numéricos adecuados.
* Compatibilidad con JSON cuando sea necesario.
* Capacidad de incorporar extensiones.
* Posibilidad futura de utilizar TimescaleDB.
* Ejecución local mediante Docker.
* Amplio soporte en plataformas de despliegue.

#### Desventajas

* Requiere diseñar un esquema y migraciones.
* El crecimiento de las mediciones exige una estrategia de índices.
* Grandes volúmenes pueden requerir particionamiento.
* El uso incorrecto de JPA puede producir consultas ineficientes.

## Decisión

Se utilizará PostgreSQL como base de datos principal de la plataforma.

PostgreSQL almacenará tanto la información transaccional como las mediciones históricas durante el MVP.

El backend accederá a la base de datos mediante:

* Spring Data JPA.
* Hibernate.
* Driver JDBC de PostgreSQL.

Las modificaciones del esquema deberán realizarse mediante migraciones versionadas. Se recomienda utilizar Flyway.

No se dependerá de la creación automática de tablas de Hibernate en entornos productivos.

## Justificación

PostgreSQL fue seleccionado porque:

* El modelo de datos contiene relaciones claras.
* Se necesita integridad referencial.
* Se requieren transacciones.
* Las consultas se realizarán principalmente por dispositivo y tiempo.
* Se necesita almacenar información histórica.
* Se integra adecuadamente con Spring Boot.
* Permite implementar restricciones de unicidad.
* Permite almacenar fechas en UTC.
* Facilita el análisis y la agregación de datos.
* Puede evolucionar hacia una solución especializada mediante extensiones.
* Es una alternativa de código abierto.

## Alcance de la decisión

PostgreSQL será responsable de almacenar:

* Usuarios.
* Roles.
* Dispositivos.
* Configuración de dispositivos.
* Mediciones.
* Estados.
* Alertas.
* Predicciones.
* Información de calidad de los datos.
* Datos necesarios para entrenamiento o evaluación del modelo.

Los logs técnicos de la aplicación no deberán almacenarse obligatoriamente en PostgreSQL durante el MVP. Podrán mantenerse en archivos o en la salida estándar de los contenedores.

## Modelo de datos inicial

Se proponen las siguientes entidades:

```text
user_account
role
user_role
device
measurement
device_status
alert
prediction
```

Durante el MVP podrán implementarse inicialmente:

```text
device
measurement
```

Las demás entidades se incorporarán en las historias correspondientes.

## Tabla de dispositivos

La tabla `device` representa una fuente de datos física o simulada.

### Campos iniciales sugeridos

| Campo         | Tipo        | Restricción    |
| ------------- | ----------- | -------------- |
| `id`          | UUID        | Clave primaria |
| `device_code` | VARCHAR     | Único, no nulo |
| `name`        | VARCHAR     | No nulo        |
| `description` | TEXT        | Opcional       |
| `device_type` | VARCHAR     | No nulo        |
| `status`      | VARCHAR     | No nulo        |
| `location`    | VARCHAR     | Opcional       |
| `created_at`  | TIMESTAMPTZ | No nulo        |
| `updated_at`  | TIMESTAMPTZ | No nulo        |

### Ejemplo conceptual

```sql
CREATE TABLE device (
    id UUID PRIMARY KEY,
    device_code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    device_type VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL,
    location VARCHAR(200),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
```

## Tabla de mediciones

Durante el MVP se utilizará inicialmente una tabla que agrupe las variables recibidas en cada instante.

### Campos iniciales sugeridos

| Campo                 | Tipo             | Restricción            |
| --------------------- | ---------------- | ---------------------- |
| `id`                  | UUID             | Clave primaria         |
| `message_id`          | UUID             | Único, no nulo         |
| `device_id`           | UUID             | Clave foránea, no nulo |
| `schema_version`      | VARCHAR          | No nulo                |
| `measured_at`         | TIMESTAMPTZ      | No nulo                |
| `received_at`         | TIMESTAMPTZ      | No nulo                |
| `voltage`             | DOUBLE PRECISION | No negativo            |
| `current`             | DOUBLE PRECISION | No negativo            |
| `power`               | DOUBLE PRECISION | No negativo            |
| `irradiance`          | DOUBLE PRECISION | No negativo            |
| `ambient_temperature` | DOUBLE PRECISION | Validación definida    |
| `panel_temperature`   | DOUBLE PRECISION | Validación definida    |
| `relative_humidity`   | DOUBLE PRECISION | Entre 0 y 100          |
| `quality`             | VARCHAR          | No nulo                |
| `created_at`          | TIMESTAMPTZ      | No nulo                |

### Ejemplo conceptual

```sql
CREATE TABLE measurement (
    id UUID PRIMARY KEY,
    message_id UUID NOT NULL UNIQUE,
    device_id UUID NOT NULL,
    schema_version VARCHAR(20) NOT NULL,
    measured_at TIMESTAMPTZ NOT NULL,
    received_at TIMESTAMPTZ NOT NULL,
    voltage DOUBLE PRECISION,
    current DOUBLE PRECISION,
    power DOUBLE PRECISION,
    irradiance DOUBLE PRECISION,
    ambient_temperature DOUBLE PRECISION,
    panel_temperature DOUBLE PRECISION,
    relative_humidity DOUBLE PRECISION,
    quality VARCHAR(30) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_measurement_device
        FOREIGN KEY (device_id)
        REFERENCES device(id),

    CONSTRAINT chk_measurement_voltage
        CHECK (voltage IS NULL OR voltage >= 0),

    CONSTRAINT chk_measurement_current
        CHECK (current IS NULL OR current >= 0),

    CONSTRAINT chk_measurement_power
        CHECK (power IS NULL OR power >= 0),

    CONSTRAINT chk_measurement_irradiance
        CHECK (irradiance IS NULL OR irradiance >= 0),

    CONSTRAINT chk_measurement_humidity
        CHECK (
            relative_humidity IS NULL
            OR relative_humidity BETWEEN 0 AND 100
        )
);
```

Este script es conceptual. La implementación definitiva deberá realizarse mediante una migración versionada.

## Decisión sobre la estructura de mediciones

Durante el MVP se almacenará una medición completa por fila, agrupando las variables generadas en el mismo instante.

### Alternativa considerada

Otra opción era utilizar una estructura genérica:

```text
measurement:
- device_id
- variable_name
- value
- unit
- measured_at
```

### Motivo para no seleccionarla inicialmente

Aunque la estructura genérica facilita incorporar nuevas variables, también presenta desventajas:

* Mayor cantidad de filas.
* Consultas más complejas para reconstruir una medición.
* Mayor dificultad para aplicar restricciones específicas.
* Mayor complejidad para Spring Data JPA.
* Menor claridad durante el MVP.

La decisión podrá revisarse si los dispositivos futuros generan conjuntos de variables muy diferentes.

## Identificadores

Se utilizarán UUID para las claves primarias principales.

### Justificación

* Evitan depender de secuencias globales.
* Facilitan la generación de identificadores desde diferentes componentes.
* Son adecuados para una futura arquitectura distribuida.
* Reducen conflictos al combinar datos provenientes de distintos entornos.

El identificador funcional del dispositivo se almacenará adicionalmente en `device_code`.

Ejemplo:

```text
panel-001
```

## Manejo de mensajes duplicados

El campo `message_id` será único.

Esto permitirá que el backend procese los mensajes MQTT con QoS 1 sin insertar dos veces la misma medición.

Ante una violación de unicidad:

* El mensaje deberá considerarse previamente procesado.
* El backend no deberá finalizar inesperadamente.
* El evento podrá registrarse a nivel de depuración o advertencia.
* No deberá generarse una segunda medición.

## Manejo del tiempo

Se utilizará `TIMESTAMPTZ` para fechas y horas relevantes.

Los componentes deberán enviar y almacenar las marcas de tiempo en UTC.

Se diferenciarán al menos:

### `measured_at`

Momento en el que el dispositivo o simulador generó la medición.

### `received_at`

Momento en el que el backend recibió o procesó el mensaje.

### `created_at`

Momento en el que el registro fue creado en la base de datos.

Esta separación permitirá analizar retrasos de transmisión y procesamiento.

Ejemplo de marca de tiempo:

```text
2026-06-07T14:30:00Z
```

La conversión a la zona horaria local deberá realizarse principalmente en la capa de presentación.

## Tipos numéricos

Para las mediciones se utilizará inicialmente `DOUBLE PRECISION`.

Esta decisión facilita:

* Operaciones matemáticas.
* Compatibilidad con Java `Double`.
* Almacenamiento de datos simulados y de sensores.
* Cálculos estadísticos.

Para valores monetarios o variables que requieran precisión decimal exacta se utilizaría `NUMERIC`, pero no es el caso principal de la telemetría del MVP.

## Convenciones de nombres

Se utilizará `snake_case` en la base de datos.

Ejemplos:

```text
device_code
measured_at
ambient_temperature
relative_humidity
```

Las tablas se nombrarán en singular para mantener consistencia:

```text
device
measurement
alert
prediction
```

No se utilizarán palabras reservadas como nombres de tablas o columnas.

Por esta razón se recomienda `user_account` en lugar de `user`.

## Índices iniciales

Se crearán índices para los campos utilizados con frecuencia en las consultas.

### Índice por dispositivo y fecha

```sql
CREATE INDEX idx_measurement_device_measured_at
    ON measurement (device_id, measured_at DESC);
```

Este índice apoyará consultas como:

* Últimas mediciones de un dispositivo.
* Mediciones de un dispositivo en un rango de fechas.
* Gráficas históricas.

### Índice por fecha

```sql
CREATE INDEX idx_measurement_measured_at
    ON measurement (measured_at DESC);
```

Su necesidad definitiva deberá evaluarse mediante el análisis de consultas, ya que un exceso de índices aumenta el costo de inserción y almacenamiento.

### Unicidad de mensajes

La restricción única sobre `message_id` creará un índice para detectar duplicados.

## Estrategia de consultas

Las consultas más frecuentes previstas son:

* Obtener la última medición de un dispositivo.
* Obtener mediciones por rango de fechas.
* Obtener mediciones ordenadas por fecha.
* Calcular promedios por intervalo.
* Obtener máximos y mínimos.
* Filtrar datos por calidad.
* Consultar alertas de un dispositivo.
* Obtener datos para entrenamiento del modelo.

Las consultas deberán utilizar paginación cuando puedan retornar una cantidad significativa de registros.

No se deberá retornar toda la tabla de mediciones desde la API.

## Migraciones

Se utilizará Flyway para administrar el esquema.

Las migraciones se almacenarán en:

```text
backend/src/main/resources/db/migration/
```

Ejemplos:

```text
V1__create_device_table.sql
V2__create_measurement_table.sql
V3__create_measurement_indexes.sql
V4__create_user_tables.sql
```

Reglas:

* Una migración aplicada no deberá modificarse.
* Los cambios posteriores deberán agregarse en una nueva migración.
* Cada migración deberá tener un propósito claro.
* Las migraciones deberán formar parte del control de versiones.
* El esquema deberá poder reconstruirse desde cero.
* Los datos sensibles no deberán incluirse en migraciones públicas.

## Configuración de Hibernate

Durante el desarrollo se recomienda:

```properties
spring.jpa.hibernate.ddl-auto=validate
```

Hibernate deberá validar que las entidades coincidan con el esquema creado por Flyway.

No se recomienda utilizar:

```properties
spring.jpa.hibernate.ddl-auto=create
```

o:

```properties
spring.jpa.hibernate.ddl-auto=update
```

como estrategia definitiva, debido a que los cambios no quedarían controlados mediante migraciones.

## Configuración mediante variables de entorno

La conexión deberá configurarse mediante variables de entorno.

Ejemplo:

```env
POSTGRES_DB=solar_monitoring
POSTGRES_USER=solar_user
POSTGRES_PASSWORD=change_me

SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/solar_monitoring
SPRING_DATASOURCE_USERNAME=solar_user
SPRING_DATASOURCE_PASSWORD=change_me
```

Cuando Spring Boot se ejecute en el sistema anfitrión y PostgreSQL se encuentre en Docker, la URL podrá utilizar:

```env
SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/solar_monitoring
```

Cuando ambos componentes se encuentren dentro de Docker Compose, deberá utilizarse el nombre del servicio:

```env
SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/solar_monitoring
```

Las credenciales reales no deberán almacenarse en el repositorio.

## Configuración de Docker

PostgreSQL se ejecutará inicialmente como un servicio de Docker Compose.

La configuración deberá incluir:

* Imagen versionada.
* Volumen persistente.
* Variables de entorno.
* Comprobación de salud.
* Red compartida con el backend.
* Reinicio controlado.

Ejemplo conceptual:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: solar-postgres
    environment:
      POSTGRES_DB: solar_monitoring
      POSTGRES_USER: solar_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - solar_postgres_data:/var/lib/postgresql/data
    healthcheck:
      test:
        - CMD-SHELL
        - pg_isready -U solar_user -d solar_monitoring
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  solar_postgres_data:
```

El contenido definitivo deberá mantenerse en el archivo `docker/docker-compose.yml`.

## Persistencia de datos

Se utilizará un volumen de Docker para evitar la pérdida de información al reiniciar el contenedor.

El comando:

```bash
docker compose down
```

no deberá eliminar el volumen.

El comando:

```bash
docker compose down -v
```

sí eliminará los datos persistidos y deberá utilizarse únicamente cuando se quiera reiniciar completamente el entorno.

## Respaldo y recuperación

Durante el MVP se deberán documentar procedimientos básicos de respaldo.

Ejemplo:

```bash
docker exec solar-postgres pg_dump \
  -U solar_user \
  -d solar_monitoring \
  > backup_solar_monitoring.sql
```

Ejemplo de restauración:

```bash
cat backup_solar_monitoring.sql | docker exec -i solar-postgres \
  psql \
  -U solar_user \
  -d solar_monitoring
```

En un despliegue productivo deberán implementarse:

* Respaldos automáticos.
* Política de retención.
* Cifrado de respaldos.
* Pruebas periódicas de restauración.
* Almacenamiento externo de copias.

## Estrategia frente al crecimiento de datos

Las mediciones producirán un crecimiento continuo de la base de datos.

Por ejemplo, con una medición cada cinco segundos:

```text
12 mediciones por minuto
720 mediciones por hora
17 280 mediciones por día
aproximadamente 6,3 millones de mediciones por año y dispositivo
```

Por este motivo se deberán considerar posteriormente:

* Agregaciones por minuto, hora y día.
* Políticas de retención.
* Archivado de datos.
* Particionamiento por tiempo.
* Compresión.
* Revisión de índices.
* Extensiones como TimescaleDB.
* Separación entre datos recientes e históricos.

Estas optimizaciones no son obligatorias para el MVP, pero el diseño deberá permitir su incorporación.

## Consideración futura de TimescaleDB

Si el volumen de mediciones aumenta considerablemente, se evaluará instalar TimescaleDB como extensión de PostgreSQL.

Esta opción permitiría:

* Convertir mediciones en una hypertable.
* Implementar compresión.
* Crear agregados continuos.
* Mejorar consultas por tiempo.
* Mantener compatibilidad con SQL y PostgreSQL.

No se utilizará inicialmente para evitar complejidad prematura.

## Integridad de los datos

La base de datos deberá aplicar restricciones además de las validaciones del backend.

Esto proporciona una segunda capa de protección.

Ejemplos:

* `message_id` único.
* `device_id` existente.
* Humedad entre 0 y 100.
* Voltaje no negativo.
* Corriente no negativa.
* Irradiancia no negativa.
* Campos obligatorios no nulos.

Las restricciones físicas definitivas deberán ajustarse cuando se conozcan los sensores y rangos reales.

## Calidad de los datos

La columna `quality` almacenará el estado inicial de calidad.

Valores propuestos:

```text
VALID
ESTIMATED
INVALID
MISSING
```

Durante el MVP se podrán almacenar únicamente datos considerados válidos y registrar los mensajes inválidos en los logs.

Posteriormente se podrá conservar información inválida o estimada para análisis de calidad, siempre que se distinga claramente de las mediciones confiables.

## Seguridad

La configuración deberá cumplir como mínimo:

* Usuario específico para la aplicación.
* Contraseña mediante variable de entorno.
* No utilizar el usuario administrador desde el backend.
* No publicar PostgreSQL directamente en internet.
* Limitar la red a los servicios necesarios.
* Utilizar conexiones cifradas en entornos remotos.
* Aplicar privilegios mínimos.
* No incluir copias de bases de datos con datos sensibles en Git.
* Mantener `.env` dentro de `.gitignore`.

En etapas posteriores podrán utilizarse usuarios separados para:

* Migraciones.
* Lectura y escritura de la aplicación.
* Lectura del modelo de aprendizaje.
* Administración.

## Consecuencias positivas

* Se mantiene integridad referencial.
* Se pueden realizar transacciones.
* La información relacional y temporal puede almacenarse en un único sistema.
* Spring Boot cuenta con integración madura.
* Las migraciones permiten trazabilidad.
* Los índices facilitan consultas históricas.
* El esquema puede evolucionar.
* Existe posibilidad de incorporar capacidades de series temporales.
* PostgreSQL puede ejecutarse localmente con Docker.
* La base de datos puede desplegarse en múltiples proveedores.

## Consecuencias negativas

* El crecimiento de telemetría deberá administrarse.
* Las migraciones requieren disciplina.
* Los índices afectan el rendimiento de inserción.
* JPA puede generar consultas ineficientes si no se configura adecuadamente.
* Las consultas agregadas complejas pueden requerir SQL nativo.
* El almacenamiento de todas las mediciones sin retención puede crecer significativamente.

## Riesgos

* Pérdida de datos por eliminación accidental de volúmenes.
* Duplicación de mediciones.
* Consultas lentas por falta de índices.
* Crecimiento excesivo.
* Diferencias de zona horaria.
* Modificaciones no controladas del esquema.
* Exposición de credenciales.
* Uso de tipos numéricos inadecuados.
* Problemas de rendimiento por cargar entidades relacionadas innecesariamente.

## Medidas de mitigación

* Usar volúmenes persistentes.
* Implementar respaldos.
* Aplicar unicidad sobre `message_id`.
* Utilizar `TIMESTAMPTZ` y UTC.
* Administrar el esquema con Flyway.
* Crear índices basados en consultas reales.
* Utilizar paginación.
* Revisar periódicamente el tamaño de las tablas.
* Evitar relaciones JPA innecesariamente ansiosas.
* Proteger credenciales.
* Agregar pruebas de repositorio e integración.

## Pruebas requeridas

La decisión deberá validarse mediante:

* Inicio de PostgreSQL con Docker Compose.
* Verificación de persistencia después de reiniciar.
* Ejecución de migraciones desde cero.
* Inserción de un dispositivo.
* Inserción de una medición.
* Rechazo de un `message_id` duplicado.
* Rechazo de una medición con humedad fuera de rango.
* Consulta de mediciones por dispositivo y fecha.
* Obtención de la última medición.
* Prueba de paginación.
* Prueba de respaldo y restauración.

## Criterios para revisar esta decisión

La decisión deberá revisarse si:

* El volumen supera la capacidad de la instancia seleccionada.
* Las consultas históricas presentan degradación significativa.
* Se incorporan cientos o miles de dispositivos.
* Se requiere procesamiento analítico en tiempo real.
* Se necesitan políticas avanzadas de compresión y retención.
* Se requiere separar datos transaccionales y telemetría.
* El modelo de aprendizaje necesita una plataforma de datos diferente.

## Resultado esperado

PostgreSQL deberá permitir almacenar de manera consistente las mediciones recibidas desde MQTT y consultarlas eficientemente desde Spring Boot.

Durante el MVP deberá ser posible completar el flujo:

```text
Mensaje MQTT
      ↓
Validación en Spring Boot
      ↓
Persistencia en PostgreSQL
      ↓
Consulta mediante API REST
      ↓
Visualización en Angular
```

La base de datos deberá conservar la trazabilidad de cada medición mediante el dispositivo, el identificador del mensaje y las marcas de tiempo correspondientes.
