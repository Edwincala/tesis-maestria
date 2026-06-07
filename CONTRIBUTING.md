# Guía de contribución

## 1. Introducción

Este documento establece el flujo de trabajo para contribuir al desarrollo de la plataforma de monitoreo de un sistema solar fotovoltaico.

El proyecto está compuesto por los siguientes módulos:

* Backend desarrollado con Java y Spring Boot.
* Simulador de datos desarrollado con Python.
* Futuro módulo de aprendizaje continuo desarrollado con Python.
* Frontend desarrollado con Angular.
* Base de datos PostgreSQL.
* Broker MQTT Eclipse Mosquitto.
* Infraestructura local administrada mediante Docker Compose.

Las contribuciones deben mantener la trazabilidad con las épicas, historias de usuario e issues definidos en GitHub Projects.

## 2. Estructura general del repositorio

```text
tesis-maestria/
├── backend/
├── database/
├── docker/
├── docs/
├── frontend/
├── simulador/
├── CONTRIBUTING.md
└── README.md
```

Cada directorio contiene un componente independiente del sistema.

### `backend`

Contiene la aplicación Java con Spring Boot encargada de:

* Consumir mensajes MQTT.
* Validar mediciones.
* Persistir información.
* Exponer la API REST.
* Gestionar autenticación y autorización.
* Integrar posteriormente los resultados del modelo predictivo.

### `simulador`

Contiene la aplicación Python encargada de:

* Generar datos eléctricos y climáticos.
* Simular condiciones normales y anómalas.
* Publicar mensajes mediante MQTT.

### `frontend`

Contiene la aplicación Angular encargada de:

* Presentar la interfaz web.
* Consumir la API REST.
* Mostrar indicadores, gráficas y datos históricos.
* Gestionar la interacción del usuario.

### `database`

Contiene recursos relacionados con:

* Modelo de datos.
* Scripts auxiliares.
* Documentación de la base de datos.
* Datos de prueba cuando sean necesarios.

Las migraciones definitivas de PostgreSQL se almacenarán dentro del backend para ser administradas mediante Flyway.

### `docker`

Contiene la configuración necesaria para ejecutar localmente:

* PostgreSQL.
* Eclipse Mosquitto.
* Otros servicios que se incorporen posteriormente.

### `docs`

Contiene la documentación técnica y académica del proyecto:

* Alcance del MVP.
* Arquitectura.
* Variables de monitoreo.
* Estándares de desarrollo.
* Decisiones arquitectónicas.
* Diagramas y especificaciones.

## 3. Requisitos generales

Antes de contribuir se debe contar, según el componente, con:

* Git.
* Java en la versión definida por el proyecto.
* Maven o Maven Wrapper.
* Python 3.
* Node.js.
* Angular CLI.
* Docker Engine.
* Docker Compose.
* Un editor o entorno de desarrollo compatible.

Las versiones específicas deberán estar documentadas en los archivos README de cada componente.

## 4. Configuración inicial del repositorio

Clonar el repositorio:

```bash
git clone https://github.com/Edwincala/tesis-maestria.git
cd tesis-maestria
```

Consultar las ramas disponibles:

```bash
git branch -a
```

Cambiar a la rama de integración:

```bash
git checkout develop
```

Actualizar la rama local:

```bash
git pull origin develop
```

No se debe desarrollar directamente sobre las ramas `main` o `develop`.

## 5. Estrategia de ramas

El proyecto utilizará las siguientes ramas:

| Rama         | Propósito                                   |
| ------------ | ------------------------------------------- |
| `main`       | Contiene versiones estables y demostrables  |
| `develop`    | Integra el trabajo en desarrollo            |
| `feature/*`  | Implementación de nuevas funcionalidades    |
| `fix/*`      | Corrección de errores                       |
| `docs/*`     | Creación o actualización de documentación   |
| `refactor/*` | Refactorizaciones sin cambios funcionales   |
| `test/*`     | Incorporación o modificación de pruebas     |
| `chore/*`    | Configuración, dependencias o mantenimiento |

## 6. Convención para nombres de ramas

Los nombres de ramas deben:

* Estar escritos en minúsculas.
* Utilizar guiones para separar palabras.
* Ser breves y descriptivos.
* Evitar espacios y caracteres especiales.
* Hacer referencia al issue cuando sea conveniente.

Formato recomendado:

```text
tipo/numero-issue-descripcion
```

Ejemplos:

```text
feature/15-mqtt-simulator
feature/21-telemetry-consumer
feature/34-measurement-api
fix/42-invalid-timestamp-validation
docs/8-system-architecture
refactor/51-measurement-service
test/55-mqtt-consumer-integration
chore/60-configure-flyway
```

Si todavía no existe un número de issue, puede utilizarse:

```text
docs/development-standards
```

## 7. Creación de una rama de trabajo

Actualizar primero la rama `develop`:

```bash
git checkout develop
git pull origin develop
```

Crear una rama nueva:

```bash
git checkout -b feature/15-mqtt-simulator
```

Verificar la rama activa:

```bash
git branch
```

## 8. Convención de commits

El proyecto utilizará Conventional Commits.

Formato:

```text
tipo(alcance): descripción
```

Tipos permitidos:

| Tipo       | Uso                                            |
| ---------- | ---------------------------------------------- |
| `feat`     | Nueva funcionalidad                            |
| `fix`      | Corrección de error                            |
| `docs`     | Cambios de documentación                       |
| `test`     | Creación o modificación de pruebas             |
| `refactor` | Cambio interno sin modificar el comportamiento |
| `chore`    | Mantenimiento y configuración                  |
| `build`    | Cambios en compilación o dependencias          |
| `ci`       | Cambios de integración continua                |
| `perf`     | Mejora de rendimiento                          |
| `style`    | Formato sin cambio funcional                   |

Alcances sugeridos:

```text
backend
frontend
simulator
mqtt
database
docker
security
telemetry
prediction
architecture
docs
```

Ejemplos:

```text
feat(simulator): add solar telemetry generator
feat(mqtt): publish measurements with qos one
feat(backend): add telemetry consumer
feat(database): create measurement migration
feat(frontend): add monitoring dashboard
fix(backend): handle invalid mqtt timestamps
fix(simulator): prevent negative irradiance values
docs(architecture): document mqtt data flow
test(backend): add measurement service tests
refactor(frontend): extract chart data service
chore(docker): update postgres configuration
```

## 9. Reglas para los mensajes de commit

Los mensajes deben:

* Describir un cambio concreto.
* Utilizar verbo en presente.
* Evitar textos genéricos como `cambios`, `ajustes` o `actualización`.
* Mantener una longitud razonable.
* No terminar con punto.
* Ser coherentes con el contenido del commit.

Ejemplo no recomendado:

```text
cambios varios
```

Ejemplo recomendado:

```text
feat(backend): validate required telemetry fields
```

Cada commit debe representar una unidad lógica de trabajo.

No se deben mezclar en un mismo commit:

* Refactorizaciones no relacionadas.
* Cambios de formato masivos.
* Nuevas funcionalidades.
* Correcciones de errores diferentes.
* Archivos generados innecesarios.

## 10. Asociación con historias de usuario e issues

Toda contribución funcional debe estar relacionada con:

* Una épica.
* Una historia de usuario.
* Un issue técnico.
* Una corrección identificada.

El Pull Request deberá incluir una referencia al issue.

Ejemplo:

```text
Closes #15
```

También pueden utilizarse:

```text
Fixes #15
Resolves #15
```

GitHub cerrará automáticamente el issue cuando el Pull Request sea integrado.

## 11. Desarrollo de los cambios

Durante el desarrollo se debe:

1. Mantener el cambio dentro del alcance del issue.
2. Seguir los estándares definidos en `docs/estandares-desarrollo.md`.
3. No incluir credenciales.
4. No incluir archivos temporales.
5. Agregar o actualizar pruebas.
6. Actualizar documentación cuando sea necesario.
7. Verificar que el componente compile o se ejecute.
8. Evitar modificar archivos no relacionados.

## 12. Gestión de configuraciones y credenciales

No se deben subir al repositorio:

* Contraseñas.
* Tokens.
* Claves privadas.
* Certificados privados.
* Credenciales de bases de datos.
* Direcciones sensibles.
* Archivos `.env` reales.
* Copias de bases de datos con información sensible.

Se deben utilizar variables de entorno.

Los módulos podrán contener un archivo:

```text
.env.example
```

Este archivo debe:

* Documentar las variables requeridas.
* Utilizar valores de ejemplo.
* No contener información secreta.

Ejemplo:

```env
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
DEVICE_ID=panel-001
```

Los archivos sensibles deberán incluirse en `.gitignore`.

## 13. Archivos que no deben incluirse

No se deberán versionar archivos generados o locales como:

```text
.env
.idea/
.vscode/
target/
node_modules/
dist/
__pycache__/
.pytest_cache/
*.pyc
*.log
coverage/
.DS_Store
```

Podrán incluirse configuraciones compartidas del editor únicamente cuando hayan sido acordadas por el equipo y no contengan información personal.

## 14. Ejecución de pruebas

Antes de enviar un Pull Request se deben ejecutar las pruebas del componente modificado.

### Backend

Desde `backend`:

```bash
./mvnw test
```

En sistemas donde no se utilice Maven Wrapper:

```bash
mvn test
```

Para verificar compilación:

```bash
./mvnw clean verify
```

### Simulador Python

Desde `simulador`:

```bash
python -m pytest
```

Para validar estilo y formato, según las herramientas configuradas:

```bash
ruff check .
black --check .
```

### Frontend Angular

Desde `frontend`:

```bash
npm test
```

Para compilar:

```bash
npm run build
```

Para ejecutar análisis estático, cuando esté configurado:

```bash
npm run lint
```

### Infraestructura

Para validar Docker Compose:

```bash
docker compose -f docker/docker-compose.yml config
```

Para iniciar los servicios:

```bash
docker compose -f docker/docker-compose.yml up -d
```

Para consultar su estado:

```bash
docker compose -f docker/docker-compose.yml ps
```

## 15. Pruebas de integración

Cuando el cambio afecte varios componentes, se deberá validar el flujo correspondiente.

Para la adquisición de telemetría:

```text
Simulador Python
        ↓
Eclipse Mosquitto
        ↓
Spring Boot
        ↓
PostgreSQL
```

Se deberá comprobar como mínimo:

* El simulador publica el mensaje.
* Mosquitto recibe la publicación.
* Spring Boot consume el mensaje.
* El mensaje es validado.
* La medición se almacena.
* No se generan errores inesperados.

Cuando la funcionalidad incluya la interfaz:

```text
PostgreSQL
        ↓
Spring Boot
        ↓
API REST
        ↓
Angular
```

## 16. Actualización de la rama antes del Pull Request

Antes de publicar los cambios:

```bash
git checkout develop
git pull origin develop
git checkout feature/15-mqtt-simulator
git merge develop
```

Resolver los conflictos y ejecutar nuevamente las pruebas.

También puede utilizarse `rebase` cuando el equipo lo acuerde:

```bash
git rebase develop
```

No se debe realizar un rebase sobre ramas compartidas sin coordinación.

## 17. Publicación de la rama

Agregar archivos:

```bash
git add .
```

Revisar los cambios:

```bash
git status
git diff --staged
```

Crear el commit:

```bash
git commit -m "feat(simulator): add mqtt telemetry publisher"
```

Publicar la rama:

```bash
git push -u origin feature/15-mqtt-simulator
```

## 18. Pull Requests

Los cambios hacia `develop` y `main` deberán realizarse mediante Pull Request.

Un Pull Request debe incluir:

* Título claro.
* Descripción del cambio.
* Issue relacionado.
* Tipo de modificación.
* Evidencia de las pruebas.
* Consideraciones técnicas.
* Capturas cuando exista un cambio visual.
* Cambios de configuración necesarios.
* Riesgos o limitaciones conocidas.

### Título recomendado

El título podrá seguir la convención de commits:

```text
feat(backend): add mqtt telemetry consumer
```

### Plantilla sugerida

```markdown
## Descripción

Describa brevemente los cambios realizados.

## Issue relacionado

Closes #

## Tipo de cambio

- [ ] Nueva funcionalidad
- [ ] Corrección de error
- [ ] Documentación
- [ ] Refactorización
- [ ] Pruebas
- [ ] Configuración

## Cambios principales

- 
- 
- 

## Pruebas realizadas

Describa los comandos ejecutados y los resultados obtenidos.

## Evidencias

Agregue capturas, registros o ejemplos cuando correspondan.

## Lista de verificación

- [ ] El código compila o se ejecuta correctamente.
- [ ] Las pruebas existentes pasan.
- [ ] Se agregaron o actualizaron pruebas.
- [ ] Se actualizó la documentación.
- [ ] No se incluyeron credenciales.
- [ ] No se incluyeron archivos generados innecesarios.
- [ ] El cambio está asociado a un issue.
```

La plantilla podrá almacenarse en:

```text
.github/pull_request_template.md
```

## 19. Revisión de código

Toda revisión deberá verificar:

* Cumplimiento de los criterios de aceptación.
* Claridad y mantenibilidad.
* Separación de responsabilidades.
* Manejo de errores.
* Validación de entradas.
* Ausencia de credenciales.
* Cobertura de pruebas.
* Compatibilidad con la arquitectura.
* Actualización de documentación.
* Impacto sobre otros componentes.

Los comentarios deben ser técnicos, claros y respetuosos.

Cuando se soliciten cambios, el autor deberá:

1. Realizar los ajustes.
2. Crear nuevos commits.
3. Responder los comentarios.
4. Ejecutar nuevamente las pruebas.
5. Solicitar una nueva revisión.

## 20. Integración de cambios

Las ramas de funcionalidades y correcciones se integrarán normalmente en:

```text
develop
```

La rama `main` contendrá únicamente versiones estables.

Flujo general:

```text
feature/* ─┐
fix/* ─────┼──> develop ───> main
docs/* ────┘
```

No se debe hacer `push` directo a `main`.

Se recomienda proteger `main` y `develop` mediante reglas del repositorio.

## 21. Eliminación de ramas

Después de integrar un Pull Request, la rama podrá eliminarse.

Remotamente:

```bash
git push origin --delete feature/15-mqtt-simulator
```

Localmente:

```bash
git branch -d feature/15-mqtt-simulator
```

Actualizar referencias:

```bash
git fetch --prune
```

## 22. Reporte de errores

Un issue de error debe incluir:

* Descripción del problema.
* Comportamiento esperado.
* Comportamiento observado.
* Pasos para reproducirlo.
* Componente afectado.
* Entorno de ejecución.
* Mensajes de error.
* Evidencias.
* Posible causa, cuando se conozca.

Ejemplo:

```markdown
## Descripción

El backend rechaza mensajes MQTT con una marca de tiempo válida.

## Pasos para reproducir

1. Iniciar Mosquitto.
2. Iniciar el backend.
3. Publicar un mensaje con `timestamp` en formato ISO 8601.
4. Revisar los logs.

## Resultado esperado

La medición debe almacenarse.

## Resultado actual

El backend registra un error de conversión.

## Entorno

- Java:
- Spring Boot:
- PostgreSQL:
- Mosquitto:
- Sistema operativo:
```

## 23. Propuesta de nuevas funcionalidades

Una propuesta debe incluir:

* Problema que busca resolver.
* Beneficio para el proyecto.
* Alcance inicial.
* Componentes afectados.
* Criterios de aceptación.
* Dependencias.
* Riesgos técnicos.
* Relación con los objetivos de la tesis.

No se deberá iniciar una funcionalidad fuera del alcance sin registrarla y revisarla previamente.

## 24. Documentación

Los cambios que modifiquen alguno de los siguientes elementos deberán actualizar la documentación:

* Arquitectura.
* Contratos JSON.
* Tópicos MQTT.
* Variables de entorno.
* Endpoints.
* Esquema de base de datos.
* Procedimientos de ejecución.
* Dependencias.
* Configuración de Docker.
* Reglas de negocio.
* Variables eléctricas o climáticas.

Las decisiones relevantes deberán registrarse en:

```text
docs/decisiones/
```

mediante un Architecture Decision Record.

## 25. Definición de terminado

Una contribución se considera terminada cuando:

* Cumple los criterios de aceptación.
* El código sigue los estándares del proyecto.
* Compila o se ejecuta correctamente.
* Las pruebas pasan.
* Se agregaron pruebas cuando correspondía.
* La documentación está actualizada.
* No contiene información sensible.
* Fue revisada.
* Fue integrada mediante Pull Request.
* El issue relacionado fue actualizado o cerrado.

## 26. Conducta y colaboración

Las contribuciones deberán realizarse de forma respetuosa y profesional.

Se espera que los participantes:

* Comuniquen bloqueos oportunamente.
* Documenten decisiones importantes.
* Eviten cambios no coordinados.
* Fundamenten las decisiones técnicas.
* Mantengan el alcance de las historias.
* Prioricen la calidad y reproducibilidad.
* Reconozcan las contribuciones de otros integrantes.

## 27. Referencias internas

Antes de contribuir se deben consultar:

```text
README.md
docs/alcance-mvp.md
docs/arquitectura.md
docs/variables-monitoreo.md
docs/estandares-desarrollo.md
docs/decisiones/
```
