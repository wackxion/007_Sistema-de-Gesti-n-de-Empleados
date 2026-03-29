"""
Sistema de Gestión de Empleados
================================

Paquete principal del proyecto. Gestiona empleados con conexión
a base de datos MariaDB y autenticación segura.

Módulos:
    - config: Carga de configuración desde variables de entorno
    - database: Conexión y operaciones con MariaDB
    - models: Modelos de datos y entidades
    - auth: Autenticación y seguridad (hash, fuerza bruta)
    - main: Punto de entrada de la aplicación
"""

__version__ = "1.0.0"
__author__ = "wackxion"
