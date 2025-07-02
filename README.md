# devweb_1_udc_u4a1
Repositorio para la actividad 4 de desarrollo de software web

Actividad 4: Desarrollo Web con Flask y MySQL

Este proyecto es un ejercicio de aprendizaje para una aplicación web básica desarrollada con Flask en Python y utilizando MySQL como base de datos. Permite gestionar usuarios y computadoras.

🚀 Configuración Mínima

Antes de empezar, validar que están instalados los siguientes componentes en el sistema:

    Python 3.8+: Se recomienda usar una versión reciente de Python 3.

    MySQL Server: Necesita una instalación de MySQL para la base de datos.

⚙️ Pasos de Instalación y Ejecución

1. Obtener el Código Fuente

Descarga el proyecto como un archivo .zip y descomprímelo en la ubicación deseada.

2. Configurar el Entorno Virtual (Recomendado)

Abre tu terminal, navega hasta la carpeta raíz del proyecto (donde descomprimiste el .zip) y crea y activa un entorno virtual para aislar las dependencias:
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

3. Instalar Dependencias

Con el entorno virtual activado, instala las bibliotecas de Python necesarias.
pip install -r requirements.txt

4. Configurar la Base de Datos MySQL

a.  Crea la base de datos act4_devweb en MySQL.
Abrir el cliente MySQL (MySQL Workbench, línea de comandos, etc.) y ejecutar:
sql CREATE DATABASE act4_devweb;

b. luego hacer una restauración de la db adjunta en el proyecto y asignar/crear un usuario con permisos de lectura/escritura
mysqldump ruta_de_la_db_fuente.sql > act4_devweb;

c. Configurar las credenciales de la base de datos.
Dentro de tu proyecto, ve a la carpeta src/config/. Abre el archivo config.py y actualiza la variable DATABASE_CONNECTION con tus credenciales de MySQL.

# src/config/config.py
DATABASE_CONNECTION = "mysql+mysqlconnector://USUARIO:CONTRASEÑA@HOST:PUERTO/act4_devweb"
# Ejemplo: "mysql+mysqlconnector://root:my_password@localhost:3306/act4_devweb"

*(Asegúrar de que el usuario MySQL tenga permisos para crear tablas y manipular datos en `act4_devweb`.)*



5. Ejecutar la Aplicación Flask

Desde la raíz del proyecto y con tu entorno virtual activado (importante esto), ejecutar la aplicación:

python main.py (o python3 main.py)

Una vez que la aplicación se inicie, verás un mensaje en la terminal indicando la URL donde está corriendo (ej. http://127.0.0.1:5000/).

🔐 Credenciales de Administrador

Para propósitos de este ejercicio y facilitar las pruebas, la aplicación incluye un acceso rápido de administrador con las siguientes credenciales:

    Usuario: admin

    Contraseña: admin

