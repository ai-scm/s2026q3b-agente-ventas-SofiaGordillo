# 📊 Sales AI Agent

## 1. Descripción del proyecto

**Sales AI Agent** es un agente inteligente que permite analizar datos de ventas mediante preguntas formuladas en lenguaje natural, sin necesidad de que el usuario conozca SQL.

La aplicación utiliza inteligencia artificial generativa para interpretar las preguntas, generar consultas SQL y obtener información almacenada en una base de datos MySQL.

Los resultados se presentan mediante una interfaz web que permite visualizar tablas, explorar gráficos interactivos y descargar los datos en formatos CSV y Excel.

El objetivo es facilitar el análisis de información comercial, reducir la necesidad de escribir consultas SQL manualmente y permitir que los usuarios obtengan respuestas a sus preguntas de negocio de una manera sencilla e intuitiva.

### Ejemplo de uso

Un usuario puede preguntar:

- ¿Cuáles son los productos más vendidos en Medellín?
- ¿Cuántas unidades se vendieron en total?
- ¿Qué sede generó mayores ingresos?
- ¿Cuáles son las ventas de cada vendedor?

El agente interpreta la pregunta, genera una consulta SQL, valida la consulta antes de ejecutarla y presenta los resultados obtenidos.

---

## 2. Objetivos del proyecto

### Objetivo general

Desarrollar un agente inteligente capaz de consultar y analizar información comercial mediante lenguaje natural, integrando inteligencia artificial generativa, una base de datos relacional y herramientas de visualización de datos.

### Objetivos específicos

- Permitir consultas de ventas mediante preguntas en lenguaje natural.
- Utilizar Amazon Bedrock para generar consultas SQL.
- Validar las consultas antes de ejecutarlas en la base de datos.
- Implementar el protocolo MCP para acceder a los datos mediante una herramienta especializada.
- Organizar el flujo de ejecución utilizando LangGraph.
- Almacenar la información comercial en MySQL.
- Presentar los resultados mediante tablas y gráficos interactivos.
- Permitir la descarga de resultados en formatos CSV y Excel.
- Separar las responsabilidades de los componentes para facilitar el mantenimiento y la evolución del proyecto.

---

## 3. Funcionalidades principales

### 3.1. Consultas en lenguaje natural

El usuario puede formular preguntas sobre la información comercial sin escribir instrucciones SQL directamente.

Por ejemplo:

> ¿Cuáles son los productos más vendidos en Medellín?

El agente interpreta la intención de la pregunta y genera una consulta que permita obtener los productos y sus unidades vendidas en esa sede.

### 3.2. Generación de SQL mediante inteligencia artificial

Amazon Bedrock permite utilizar un modelo de lenguaje para transformar una pregunta en lenguaje natural en una consulta SQL.

La aplicación proporciona instrucciones al modelo para orientar la generación de consultas compatibles con la estructura de la base de datos.

### 3.3. Validación de consultas

Antes de ejecutar una consulta, el proyecto utiliza SQLGlot para analizar su estructura y aplicar reglas de validación.

Entre las restricciones implementadas se encuentran:

- Rechazar operaciones de modificación de datos, como `UPDATE` y `DELETE`.
- Rechazar operaciones de estructura, como `DROP TABLE`.
- Evitar la ejecución de múltiples sentencias en una misma solicitud.
- Restringir las consultas a la tabla `ventas`.
- Aplicar límites al número de filas devueltas.

Estas medidas constituyen una capa de protección de la aplicación, pero deben complementarse con permisos de solo lectura en MySQL y otras medidas de seguridad.

### 3.4. Acceso a los datos mediante MCP

El proyecto utiliza el protocolo Model Context Protocol (MCP) para exponer una herramienta que permite consultar la base de datos.

El cliente MCP invoca la herramienta del servidor, que valida la consulta y obtiene los resultados desde MySQL.

### 3.5. Visualización de resultados

Los resultados se muestran en una tabla dentro de la interfaz de Streamlit.

Cuando la estructura de los datos lo permite, la aplicación también genera gráficos interactivos utilizando Plotly.

### 3.6. Exportación de resultados

El usuario puede descargar los resultados de una consulta en dos formatos:

- **CSV:** adecuado para intercambiar datos y utilizarlos en otras herramientas.
- **Excel:** adecuado para revisar, organizar y analizar información en hojas de cálculo.

### 3.7. Visualización del SQL generado

La interfaz permite consultar la sentencia SQL generada por el agente, lo que facilita comprender cómo se obtuvo el resultado y revisar la consulta cuando sea necesario.

---

## 4. Arquitectura del sistema

El proyecto utiliza una arquitectura modular en la que cada componente tiene una responsabilidad específica.

```text
                       USUARIO
                          |
                          v
                  INTERFAZ STREAMLIT
                          |
                          v
                    AGENTE LANGGRAPH
                          |
                          v
                   AMAZON BEDROCK
                Generación de consultas SQL
                          |
                          v
                    VALIDACIÓN SQL
                       SQLGLOT
                          |
                          v
                     CLIENTE MCP
                          |
                          v
                    SERVIDOR MCP
                          |
                          v
                     BASE DE DATOS
                        MYSQL
                          |
                          v
                  RESULTADOS DE CONSULTA
                          |
               +----------+----------+
               |          |          |
               v          v          v
             TABLA      GRÁFICO    EXPORTACIÓN
             PANDAS     PLOTLY     CSV / EXCEL
```

### Descripción de los componentes

| Componente | Responsabilidad |
|---|---|
| Streamlit | Proporciona la interfaz web y recibe las preguntas del usuario. |
| Amazon Bedrock | Genera consultas SQL a partir de preguntas en lenguaje natural. |
| LangGraph | Organiza y coordina las etapas del agente. |
| SQLGlot | Analiza la sintaxis SQL y permite aplicar reglas de validación. |
| Cliente MCP | Se comunica con el servidor MCP para invocar la herramienta de consulta. |
| Servidor MCP | Expone la herramienta que permite consultar las ventas. |
| MySQL | Almacena los registros comerciales. |
| Pandas | Organiza los resultados para su presentación y exportación. |
| Plotly | Genera gráficos interactivos. |
| OpenPyXL | Proporciona soporte para la generación de archivos Excel. |
| Docker Compose | Facilita la ejecución del servicio MySQL en un contenedor. |

---

## 5. Tecnologías utilizadas

### Python 3.12

Es el lenguaje de programación principal. Se utiliza para implementar el agente, gestionar las conexiones, procesar resultados y construir la interfaz.

### Amazon Bedrock

Servicio de AWS que permite acceder a modelos de inteligencia artificial generativa.

En este proyecto se utiliza para interpretar preguntas y generar consultas SQL.

### Boto3

SDK de AWS para Python. Permite que la aplicación se comunique con los servicios de AWS, incluido Amazon Bedrock Runtime.

### LangGraph

Framework utilizado para organizar el flujo de ejecución del agente mediante nodos y estados.

En el proyecto coordina principalmente la generación de la consulta y su ejecución.

### Model Context Protocol (MCP)

Protocolo que permite exponer herramientas que pueden ser invocadas por un cliente compatible.

En este proyecto conecta el agente con una herramienta especializada para consultar los datos de ventas.

### SQLGlot

Biblioteca de Python que permite analizar, interpretar y transformar consultas SQL.

Se utiliza para inspeccionar las consultas generadas y aplicar reglas antes de ejecutarlas.

### MySQL 8.4

Sistema de gestión de bases de datos relacionales que almacena los datos comerciales.

### PyMySQL

Biblioteca utilizada para conectar Python con MySQL.

### Streamlit

Framework que permite construir aplicaciones web de datos utilizando Python.

Se utiliza para recibir preguntas y presentar tablas, gráficos y descargas.

### Pandas

Biblioteca utilizada para trabajar con datos tabulares y preparar los resultados de las consultas.

### Plotly

Biblioteca de visualización que permite crear gráficos interactivos.

### OpenPyXL

Biblioteca utilizada como soporte para generar archivos Excel.

### Docker y Docker Compose

Permiten ejecutar MySQL en un contenedor, facilitando la preparación y reproducción del entorno de desarrollo.

### pytest

Framework utilizado para ejecutar pruebas automatizadas del proyecto.

---

## 6. Estructura del proyecto

La organización de referencia del proyecto es la siguiente:

```text
sales-agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── graph.py
│   ├── prompts.py
│   ├── visualizations.py
│   ├── exports.py
│   ├── bedrock.py
│   └── mcp_client.py
│
├── mcp_server/
│   ├── __init__.py
│   └── server.py
│
├── database/
│   ├── init.sql
│   ├── db.py
│   └── test_connection.py
│
├── data/
│   └── ventas.csv
│
├── tests/
│   └── test_agent.py
│
├── .env
├── .env.example
├── .gitignore
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

Esta estructura representa la organización de referencia. Los archivos y directorios definitivos deben corresponder con los que existan en el repositorio.

### Responsabilidad de los archivos principales

| Archivo | Descripción |
|---|---|
| `app/main.py` | Contiene la interfaz de Streamlit. |
| `app/agent.py` | Implementa la generación y validación de consultas SQL. |
| `app/graph.py` | Define el flujo del agente utilizando LangGraph. |
| `app/prompts.py` | Contiene las instrucciones utilizadas para orientar al modelo. |
| `app/bedrock.py` | Configura el cliente de Amazon Bedrock y realiza las solicitudes al modelo. |
| `app/mcp_client.py` | Implementa el cliente que invoca la herramienta MCP. |
| `app/visualizations.py` | Contiene la lógica para generar gráficos. |
| `app/exports.py` | Implementa la exportación de resultados a CSV y Excel. |
| `mcp_server/server.py` | Define la herramienta MCP que consulta los datos de ventas. |
| `database/db.py` | Gestiona la conexión con MySQL y el acceso a los registros. |
| `database/init.sql` | Contiene el esquema y los datos iniciales de la base de datos. |
| `compose.yaml` | Define los servicios Docker del proyecto. |
| `requirements.txt` | Contiene las dependencias de Python. |
| `.env.example` | Proporciona una plantilla de configuración sin credenciales reales. |
| `.env` | Almacena la configuración privada del entorno local. |
| `tests/` | Contiene las pruebas automatizadas disponibles. |

---

## 7. Modelo de datos

La aplicación consulta una tabla denominada `ventas`, almacenada en MySQL.

### Estructura de la tabla

| Campo | Descripción |
|---|---|
| `id` | Identificador del registro de venta. |
| `vendedor` | Nombre del vendedor responsable de la operación. |
| `sede` | Ubicación donde se registró la venta. |
| `producto` | Producto vendido. |
| `cantidad` | Número de unidades vendidas. |
| `precio` | Precio unitario registrado. |
| `fecha` | Fecha de la venta. |

### Datos de ejemplo

El conjunto de datos de demostración contiene registros asociados con tres sedes:

- Bogotá.
- Medellín.
- Cali.

Estos datos permiten probar consultas agrupadas por sede, producto y vendedor, así como cálculos de unidades e ingresos.

Los datos utilizados durante el desarrollo son datos de ejemplo y no deben interpretarse como cifras comerciales reales.

---

## 8. Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.12.
- Docker.
- Docker Compose.
- AWS CLI v2.
- Un perfil AWS configurado con los permisos necesarios.
- Acceso al modelo de Amazon Bedrock configurado.
- Las dependencias indicadas en `requirements.txt`.
- Una configuración válida de MySQL.

En Ubuntu se pueden comprobar las versiones mediante:

```bash
python3.12 --version
docker --version
docker compose version
aws --version
```

---

## 9. Configuración del entorno

### 9.1. Ubicarse en el proyecto

```bash
cd ~/Descargas/sales-agent
```

### 9.2. Crear el entorno virtual

```bash
uv venv --python 3.12 .venv
```

### 9.3. Activar el entorno virtual

```bash
source .venv/bin/activate
```

### 9.4. Verificar Python

```bash
python --version
which python
```

El intérprete debe corresponder al entorno virtual del proyecto.

### 9.5. Instalar las dependencias

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

Este comando instala las bibliotecas declaradas en `requirements.txt` dentro del entorno virtual.

### 9.6. Preparar el archivo de configuración

Si todavía no existe `.env`, se puede crear a partir de la plantilla:

```bash
cp .env.example .env
```

Edita el archivo y completa los valores requeridos por la aplicación.

**Importante:** no publiques el archivo `.env` en GitHub porque puede contener información sensible.

---

## 10. Configuración de AWS Bedrock

El proyecto utiliza Amazon Bedrock Runtime para invocar el modelo de lenguaje.

La configuración de desarrollo descrita utiliza:

| Parámetro | Valor de referencia |
|---|---|
| Región AWS | `us-east-1` |
| Perfil AWS | `sofia` |
| Modelo | `openai.gpt-oss-120b-1:0` |

La disponibilidad del modelo y los permisos dependen de la cuenta y de la configuración de AWS.

### Iniciar sesión en AWS

Si se utiliza AWS IAM Identity Center, ejecuta:

```bash
aws sso login --profile sofia
```

### Verificar la identidad

```bash
aws sts get-caller-identity --profile sofia
```

Si el inicio de sesión funciona, AWS mostrará información de la identidad autenticada.

Si aparece un error relacionado con un token vencido, vuelve a iniciar sesión mediante AWS SSO.

### Permisos necesarios

La identidad de AWS debe tener los permisos necesarios para invocar el modelo de Bedrock configurado.

Si la solicitud falla, verifica:

- El perfil seleccionado.
- La región configurada.
- El identificador del modelo.
- Los permisos IAM.
- Las políticas de la organización.
- La disponibilidad del modelo para la cuenta.

No incluyas claves de acceso ni tokens de AWS en el README.

---

## 11. Configuración de MySQL

La base de datos se ejecuta mediante Docker.

En la configuración de desarrollo utilizada, el contenedor MySQL publica el puerto `3306` internamente mediante el puerto `3307` del equipo anfitrión.

Los parámetros de conexión deben coincidir con los valores configurados en `.env`, `compose.yaml` y el código Python.

Ejemplo ilustrativo:

```dotenv
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_DATABASE=ventas
MYSQL_USER=usuario_de_aplicacion
MYSQL_PASSWORD=CAMBIAR_POR_UNA_CLAVE_LOCAL
```

Los nombres exactos de las variables deben coincidir con los que utiliza el código del proyecto.

### Iniciar MySQL

Desde la raíz del proyecto:

```bash
docker compose up -d
```

### Comprobar el estado de los contenedores

```bash
docker compose ps
```

### Consultar los registros del contenedor

Si el contenedor se llama `sales-agent-mysql`:

```bash
docker logs sales-agent-mysql
```

Los datos iniciales se cargan de acuerdo con la configuración y los scripts de inicialización del proyecto.

En las imágenes oficiales de MySQL, los scripts de inicialización normalmente se ejecutan al preparar por primera vez un directorio de datos vacío. Reiniciar un contenedor no implica necesariamente volver a ejecutar esos scripts.

---

## 12. Ejecución de la aplicación

Antes de iniciar la interfaz, verifica que:

1. El entorno virtual esté activado.
2. Las dependencias estén instaladas.
3. Las variables de entorno estén configuradas.
4. MySQL esté funcionando.
5. AWS tenga una sesión válida.
6. El modelo de Bedrock esté disponible para la cuenta.

### Iniciar la base de datos

```bash
docker compose up -d
```

### Activar el entorno virtual

```bash
source .venv/bin/activate
```

### Iniciar Streamlit

```bash
python -m streamlit run app/main.py
```

La aplicación se ejecuta normalmente en:

```text
http://localhost:8501
```

Abre esa dirección en el navegador.

Para detener Streamlit, vuelve a la terminal donde se ejecuta y presiona:

```text
Ctrl + C
```

### Detener los servicios Docker

```bash
docker compose down
```

Este comando detiene y elimina los contenedores administrados por Compose.

Normalmente conserva los datos almacenados en volúmenes persistentes.

**Precaución:** no ejecutes `docker compose down -v` si deseas conservar los datos del volumen.

---

## 13. Ejemplos de consultas

Una vez iniciada la aplicación, se pueden formular preguntas como las siguientes:

### Análisis por producto

```text
¿Cuáles son los productos más vendidos en Medellín?
```

Permite identificar los productos con mayor cantidad de unidades vendidas en la sede seleccionada.

### Análisis general

```text
¿Cuántas unidades se vendieron en total?
```

Permite calcular la cantidad total de unidades registradas.

### Comparación entre sedes

```text
¿Qué sede generó mayores ingresos?
```

Permite comparar el valor de las ventas agrupadas por sede.

Para calcular ingresos, la consulta debe considerar tanto la cantidad como el precio unitario, según las reglas de negocio definidas.

### Análisis por vendedor

```text
¿Cuáles son las ventas de cada vendedor?
```

Permite agrupar la información por vendedor y comparar sus resultados.

### Análisis por ubicación

```text
¿Cuánto se vendió por sede?
```

Permite comparar los registros comerciales entre Bogotá, Medellín y Cali.

Los resultados dependen de los datos almacenados y de la consulta SQL que genere el modelo.

---

## 14. Flujo de funcionamiento del agente

El procesamiento de una pregunta sigue estas etapas:

### Paso 1. Recepción de la pregunta

El usuario introduce una pregunta en lenguaje natural desde la interfaz de Streamlit.

### Paso 2. Interpretación mediante inteligencia artificial

El agente envía la pregunta a Amazon Bedrock junto con instrucciones para generar una consulta SQL.

### Paso 3. Generación de SQL

El modelo produce una consulta que intenta responder la pregunta del usuario utilizando la tabla de ventas.

### Paso 4. Validación de la consulta

SQLGlot analiza la consulta y la aplicación verifica las reglas de acceso establecidas.

Si la consulta incumple las reglas, debe rechazarse antes de ejecutarse.

### Paso 5. Invocación de la herramienta MCP

El cliente MCP solicita al servidor la ejecución de la herramienta `consultar_ventas`.

### Paso 6. Ejecución en MySQL

El servidor consulta la base de datos y obtiene los registros correspondientes.

### Paso 7. Retorno de resultados

Las filas obtenidas regresan al agente para continuar el procesamiento.

### Paso 8. Presentación

Streamlit presenta los resultados en una tabla y, cuando es apropiado, genera un gráfico interactivo.

### Paso 9. Exportación

El usuario puede descargar los resultados en CSV o Excel.

---

## 15. Validación y seguridad SQL

El agente utiliza SQLGlot como parte de la validación de consultas generadas por inteligencia artificial.

Las reglas implementadas incluyen restricciones para evitar operaciones de escritura y limitar el acceso a la tabla permitida.

### Ejemplos de validación

| Consulta | Resultado esperado |
|---|---|
| `SELECT * FROM ventas` | Aceptada y limitada por la aplicación. |
| `DELETE FROM ventas` | Rechazada. |
| `DROP TABLE ventas` | Rechazada. |
| `UPDATE ventas SET cantidad = 0` | Rechazada. |
| `SELECT * FROM ventas; DROP TABLE ventas` | Rechazada por contener múltiples sentencias. |
| `SELECT * FROM clientes` | Rechazada por consultar una tabla no permitida. |

### Recomendaciones de seguridad

La validación SQL no debe considerarse una protección absoluta.

Antes de utilizar el proyecto con datos reales, se recomienda:

1. Crear un usuario MySQL exclusivo para la aplicación.
2. Conceder únicamente permisos de lectura sobre los datos necesarios.
3. Evitar ejecutar la aplicación con una cuenta administradora.
4. Revisar las consultas generadas por el modelo.
5. Probar casos de SQL malicioso y consultas complejas.
6. Mantener las credenciales fuera del código fuente.
7. Restringir el acceso de red a MySQL.
8. Incorporar autenticación si la aplicación estará disponible para otros usuarios.
9. Evitar mostrar información sensible en mensajes de error.
10. Registrar las operaciones relevantes sin almacenar secretos.

La seguridad debe aplicarse en varias capas. La validación de la aplicación complementa, pero no reemplaza, los permisos de la base de datos.

---

## 16. Uso del protocolo MCP

Model Context Protocol (MCP) es un protocolo que permite a las aplicaciones exponer herramientas mediante una interfaz estandarizada.

En este proyecto, el servidor MCP ofrece la herramienta:

```text
consultar_ventas(sql)
```

Esta herramienta recibe una consulta SQL, aplica las validaciones definidas y accede a MySQL para devolver los resultados.

El cliente MCP inicia una sesión con el servidor y solicita la ejecución de la herramienta.

### Beneficios de MCP en el proyecto

- Separa la lógica del agente de la lógica de acceso a los datos.
- Permite exponer las consultas como una herramienta especializada.
- Facilita mantener responsabilidades independientes.
- Permite utilizar el protocolo MCP para la comunicación entre el cliente y el servidor.
- Hace más clara la integración entre inteligencia artificial y servicios externos.

### Prueba manual del cliente MCP

Con el entorno virtual activado, desde la raíz del proyecto:

```bash
python -c "import asyncio; from app.mcp_client import consultar_ventas_mcp; print(asyncio.run(consultar_ventas_mcp('SELECT sede, COUNT(*) AS total_ventas FROM ventas GROUP BY sede ORDER BY total_ventas DESC LIMIT 100')))"
```

La salida dependerá de los registros presentes en MySQL.

---

## 17. Pruebas

El proyecto puede verificarse mediante pruebas automatizadas y pruebas de integración.

### Ejecutar pytest

Desde la raíz del proyecto:

```bash
pytest -v
```

Las pruebas que dependan de MySQL o de Amazon Bedrock requieren que esos servicios estén configurados y disponibles.

### Probar la conexión con MySQL

Si el archivo `database/test_connection.py` está presente:

```bash
python database/test_connection.py
```

### Probar el flujo del agente

```bash
python -c "from app.graph import ask_sales_agent; resultado = ask_sales_agent('¿Cuáles son los productos más vendidos en Medellín?'); print('PREGUNTA:', resultado['question']); print('SQL GENERADO:', resultado['sql']); print('RESPUESTA:', resultado['response']); print('RESULTADOS:', resultado['results'])"
```

Esta prueba ejecuta el flujo del agente y permite inspeccionar la pregunta, el SQL generado y los resultados obtenidos.

Para ejecutarla correctamente se necesita una sesión AWS válida, acceso al modelo configurado y una base de datos disponible.

---

## 18. Solución de problemas

### Error: token de AWS vencido

Ejecuta:

```bash
aws sso login --profile sofia
```

Después verifica la identidad:

```bash
aws sts get-caller-identity --profile sofia
```

### Error al invocar Amazon Bedrock

Comprueba la región, el perfil, el identificador del modelo y los permisos IAM.

También verifica que la cuenta tenga acceso al modelo configurado.

### Error de conexión con MySQL

Comprueba el estado de los contenedores:

```bash
docker compose ps
```

Consulta los registros:

```bash
docker logs sales-agent-mysql
```

Verifica que el host, el puerto y las credenciales coincidan con la configuración real.

Cuando Python se ejecuta directamente en el equipo, normalmente se utiliza `127.0.0.1:3307`. Si la aplicación se ejecuta en otro contenedor de la misma red de Compose, puede necesitar el nombre del servicio y el puerto interno `3306`.

### Error: módulo de Python no encontrado

Activa el entorno virtual:

```bash
source .venv/bin/activate
```

Reinstala las dependencias:

```bash
uv pip install --python .venv/bin/python -r requirements.txt
```

Inicia Streamlit mediante el intérprete del entorno:

```bash
python -m streamlit run app/main.py
```

### La consulta SQL no responde correctamente

Revisa el SQL generado en la interfaz.

Comprueba que los nombres de las columnas coincidan con la tabla `ventas` y que la pregunta tenga una interpretación inequívoca.

Por ejemplo, «mayores ventas» podría referirse a ingresos, unidades vendidas o número de transacciones.

### No se muestra un gráfico

Los gráficos dependen de la estructura de los resultados. Una consulta con una categoría y una columna numérica suele ser apropiada para un gráfico de barras.

### No se genera un archivo Excel

Comprueba que `openpyxl` esté instalado y que los resultados puedan convertirse en un DataFrame de Pandas.

---

## 19. Variables de entorno

La configuración debe corresponder con las variables que lee realmente el código.

| Variable | Propósito |
|---|---|
| `AWS_PROFILE` | Perfil de AWS utilizado por Boto3. |
| `AWS_REGION` | Región en la que se invoca Bedrock. |
| `MODEL_ID` | Identificador del modelo de lenguaje. |
| `MYSQL_HOST` | Dirección del servidor MySQL. |
| `MYSQL_PORT` | Puerto de conexión a MySQL. |
| `MYSQL_DATABASE` | Base de datos que contiene las ventas. |
| `MYSQL_USER` | Usuario de MySQL. |
| `MYSQL_PASSWORD` | Contraseña del usuario de MySQL. |

Antes de añadir o cambiar variables, revisa el código de conexión, el cliente de Bedrock, `.env.example` y `compose.yaml`.

**Nunca publiques el contenido real de `.env`.**

---

## 20. Limitaciones actuales

El proyecto constituye una base funcional para explorar el análisis de datos asistido por inteligencia artificial.

Entre sus limitaciones se encuentran:

- La calidad de las respuestas depende de la interpretación del modelo.
- Una consulta SQL sintácticamente válida puede no representar correctamente la intención del usuario.
- La validación SQL necesita pruebas adicionales frente a consultas complejas y entradas maliciosas.
- Los gráficos dependen de la estructura de los datos devueltos.
- La disponibilidad del modelo depende de la configuración de AWS.
- El proyecto utiliza un conjunto de datos de demostración.
- El despliegue para múltiples usuarios requeriría controles adicionales de acceso y operación.

---

## 21. Mejoras futuras

Algunas mejoras que pueden incorporarse son:

- Fortalecer las reglas de validación SQL.
- Utilizar exclusivamente un usuario MySQL de solo lectura.
- Incorporar autenticación y autorización.
- Mejorar los mensajes de error.
- Añadir pruebas unitarias y de integración.
- Incorporar registros de auditoría.
- Mejorar la interpretación de preguntas ambiguas.
- Permitir seleccionar tipos de gráficos.
- Agregar filtros por fechas, sedes, productos y vendedores.
- Implementar límites de tiempo y de filas devueltas.
- Preparar un procedimiento de despliegue y monitorización.
- Añadir documentación de operación y mantenimiento.

---

## 22. Conclusión

Sales AI Agent demuestra cómo integrar inteligencia artificial generativa, bases de datos relacionales y herramientas de visualización para simplificar el análisis de información comercial.

El usuario puede formular preguntas en lenguaje natural y obtener resultados sin escribir SQL manualmente. Amazon Bedrock genera las consultas, SQLGlot participa en su validación, MCP proporciona la herramienta de acceso a los datos y LangGraph coordina el flujo de procesamiento.

Finalmente, Streamlit presenta los resultados en tablas y gráficos interactivos y permite descargarlos en formatos CSV y Excel.

La arquitectura modular facilita comprender las responsabilidades de cada componente y ofrece una base para ampliar el proyecto con nuevas consultas, visualizaciones y medidas de seguridad.

**Nota:** antes de utilizar el sistema con información comercial real, deben revisarse los permisos de la base de datos, las reglas de validación SQL y la configuración de seguridad del entorno.