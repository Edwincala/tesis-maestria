# Alcance del producto mínimo viable

## 1. Descripción general

El producto mínimo viable consiste en una plataforma web para la adquisición,
almacenamiento, consulta y visualización de variables eléctricas y climáticas
asociadas al funcionamiento de un sistema solar fotovoltaico.

Durante la primera etapa del proyecto, los datos serán generados mediante un
simulador desarrollado en Python y transmitidos mediante el protocolo MQTT.

El backend, desarrollado con Java y Spring Boot, recibirá los datos enviados
al broker MQTT, realizará su validación y los almacenará en una base de datos
PostgreSQL.

El frontend, desarrollado con Angular, permitirá consultar las mediciones y
visualizar su comportamiento mediante indicadores y gráficas.

## 2. Objetivo del MVP

Validar el flujo completo de información desde la generación o adquisición de
las mediciones hasta su visualización en la plataforma web:

Simulador Python → MQTT → Spring Boot → PostgreSQL → Angular.

## 3. Usuarios iniciales

### Investigador

Podrá:

- Iniciar sesión en la plataforma.
- Consultar las variables monitoreadas.
- Visualizar las mediciones más recientes.
- Consultar datos históricos.
- Identificar valores fuera de los rangos esperados.
- Consultar el estado de conexión de los dispositivos o fuentes de datos.

### Administrador

En una etapa posterior podrá:

- Crear y administrar usuarios.
- Registrar dispositivos.
- Configurar rangos de operación.
- Consultar registros de actividad.

La administración avanzada de usuarios y dispositivos podrá quedar fuera de
la primera versión del MVP.

## 4. Funcionalidades incluidas

El MVP incluirá:

1. Simulación de datos eléctricos y climáticos con Python.
2. Publicación periódica de datos en un broker MQTT.
3. Suscripción del backend a los tópicos MQTT.
4. Validación de los mensajes recibidos.
5. Persistencia de datos en PostgreSQL.
6. API REST para consultar mediciones.
7. Autenticación básica de usuarios.
8. Visualización de la última medición disponible.
9. Visualización de datos históricos mediante gráficas.
10. Filtrado de información por variable y rango de fechas.
11. Identificación básica de valores fuera de rango.
12. Ejecución local de los servicios mediante Docker Compose.

## 5. Funcionalidades excluidas de la primera versión

Inicialmente no se incluirán:

- Aplicación móvil nativa.
- Notificaciones por SMS o WhatsApp.
- Integración con pagos.
- Control remoto de los paneles solares.
- Mantenimiento predictivo avanzado.
- Integración simultánea con múltiples plantas solares.
- Procesamiento de imágenes térmicas.
- Despliegue definitivo en infraestructura productiva.
- Entrenamiento definitivo del modelo de aprendizaje continuo.
- Pronósticos de largo plazo.
- Administración avanzada de roles y permisos.

## 6. Restricciones iniciales

- El sistema se desarrollará inicialmente en un entorno local.
- Los datos serán simulados mientras se implementa la instrumentación física.
- La comunicación entre el simulador y el backend utilizará MQTT.
- PostgreSQL será el sistema principal de persistencia.
- El backend se desarrollará con Java y Spring Boot.
- El frontend se desarrollará con Angular.
- El simulador y los futuros modelos predictivos se desarrollarán con Python.

## 7. Criterios de éxito del MVP

El MVP se considerará funcional cuando:

- El simulador publique mediciones válidas en MQTT.
- Spring Boot reciba y valide los mensajes.
- Las mediciones se almacenen correctamente en PostgreSQL.
- La API permita consultar datos históricos y recientes.
- Angular muestre las mediciones en indicadores y gráficas.
- El sistema pueda ejecutarse localmente siguiendo la documentación del
  repositorio.