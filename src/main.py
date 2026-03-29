"""
Punto de Entrada - Menú Principal
=================================

Interfaz de línea de comandos (CLI) para el Sistema
de Gestión de Empleados.

Opciones:
    1. Iniciar sesión (login)
    2. Registrarse como nuevo empleado
    3. Ver lista de empleados (requiere login)
    4. Buscar empleado
    5. Salir

Usage:
    python src/main.py
"""

import sys
import os
from typing import Tuple

# Agregar ruta actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import test_connection
from auth import iniciar_sesion
from models import (
    crear_empleado,
    obtener_empleados,
    buscar_empleados,
    actualizar_empleado,
    eliminar_empleado
)


# Variable global para almacenar el usuario logueado
USUARIO_LOGUEADO = None


def mostrar_banner():
    """Muestra el banner de bienvenida del sistema."""
    print("\n" + "="*50)
    print("   [Sistema de Gestion de Empleados]   ")
    print("="*50)


def validar_email(email: str) -> bool:
    """
    Valida el formato básico de un email.
    
    Args:
        email (str): Correo electrónico a validar
        
    Returns:
        bool: True si el formato es válido
    """
    return '@' in email and '.' in email.split('@')[1]


def validar_password(password: str) -> Tuple[bool, str]:
    """
    Valida que la contraseña cumpla los requisitos mínimos.
    
    Args:
        password (str): Contraseña a validar
        
    Returns:
        tuple: (es_valida, mensaje)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe tener al menos un número."
    
    if not any(c.isalpha() for c in password):
        return False, "La contraseña debe tener al menos una letra."
    
    return True, "OK"


def opcion_login():
    """Pantalla de inicio de sesión."""
    print("\n--- [Iniciar] Iniciar Sesión ---")
    
    email = input("Email: ").strip()
    password = input("Contraseña: ").strip()
    
    if not email or not password:
        print("[Error] Error: Email y contraseña son obligatorios.")
        return
    
    exito, mensaje, datos = iniciar_sesion(email, password)
    
    if exito:
        print(f"[OK] {mensaje}")
        global USUARIO_LOGUEADO
        USUARIO_LOGUEADO = datos
        print(f"   Hola, {datos['nombre']} {datos['apellido']}!")
    else:
        print(f"[Error] {mensaje}")


def opcion_registro():
    """Pantalla de registro de nuevo empleado."""
    print("\n--- [Registrar] Registrarse ---")
    
    # Solicitar datos
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email: ").strip()
    password = input("Contraseña: ").strip()
    telefono = input("Teléfono (opcional): ").strip()
    puesto = input("Puesto (opcional): ").strip()
    
    # Validaciones
    if not nombre or not apellido or not email or not password:
        print("[Error] Error: Nombre, apellido, email y contraseña son obligatorios.")
        return
    
    if not validar_email(email):
        print("[Error] Error: Formato de email inválido.")
        return
    
    valida_pass, msg = validar_password(password)
    if not valida_pass:
        print(f"[Error] Error: {msg}")
        return
    
    # Crear empleado
    nuevo_id = crear_empleado(
        nombre=nombre,
        apellido=apellido,
        email=email,
        password_plana=password,
        telefono=telefono or None,
        puesto=puesto or None
    )
    
    if nuevo_id:
        print(f"[OK] ¡Registro exitoso! Tu ID de empleado es: {nuevo_id}")
    else:
        print("[Error] Error al registrar. ¿El email ya existe?")


def opcion_ver_empleados():
    """Pantalla para listar empleados (requiere login)."""
    if not USUARIO_LOGUEADO:
        print("[Aviso]  Debes iniciar sesión primero.")
        return
    
    print("\n--- [Ver] Lista de Empleados ---")
    
    empleados = obtener_empleados(activos_solo=True)
    
    if not empleados:
        print("📭 No hay empleados registrados.")
        return
    
    print(f"\nTotal: {len(empleados)} empleado(s)\n")
    print("-" * 60)
    
    for emp in empleados:
        print(f"ID: {emp['id']}")
        print(f"  Nombre: {emp['nombre']} {emp['apellido']}")
        print(f"  Email: {emp['email']}")
        print(f"  Puesto: {emp.get('puesto', 'No especificado')}")
        print("-" * 60)


def opcion_buscar_empleado():
    """Pantalla para buscar empleados."""
    if not USUARIO_LOGUEADO:
        print("[Aviso]  Debes iniciar sesión primero.")
        return
    
    print("\n--- [Buscar] Buscar Empleado ---")
    
    termino = input("Ingresa nombre, apellido o email: ").strip()
    
    if not termino:
        print("[Error] Error: Debes ingresar un término de búsqueda.")
        return
    
    resultados = buscar_empleados(termino)
    
    if not resultados:
        print(f"📭 No se encontraron empleados con: '{termino}'")
        return
    
    print(f"\nSe encontraron {len(resultados)} resultado(s):\n")
    
    for emp in resultados:
        print(f"ID: {emp['id']}")
        print(f"  Nombre: {emp['nombre']} {emp['apellido']}")
        print(f"  Email: {emp['email']}")
        print(f"  Puesto: {emp.get('puesto', 'No especificado')}")
        print("-" * 40)


def opcion_editar_empleado():
    """Pantalla para editar un empleado (solo admin o propio registro)."""
    if not USUARIO_LOGUEADO:
        print("[Aviso]  Debes iniciar sesión primero.")
        return
    
    print("\n--- [Editar]  Editar Empleado ---")
    
    try:
        empleado_id = int(input("ID del empleado a editar: "))
    except ValueError:
        print("[Error] Error: Debes ingresar un número válido.")
        return
    
    print("\nCampos a editar (deja en blanco para no modificar):")
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_apellido = input("Nuevo apellido: ").strip()
    nuevo_telefono = input("Nuevo teléfono: ").strip()
    nuevo_puesto = input("Nuevo puesto: ").strip()
    
    exito = actualizar_empleado(
        empleado_id=empleado_id,
        nombre=nuevo_nombre or None,
        apellido=nuevo_apellido or None,
        telefono=nuevo_telefono or None,
        puesto=nuevo_puesto or None
    )
    
    if exito:
        print("[OK] Empleado actualizado correctamente.")
    else:
        print("[Error] Error al actualizar. ¿El ID existe?")


def opcion_eliminar_empleado():
    """Pantalla para eliminar (soft delete) un empleado."""
    if not USUARIO_LOGUEADO:
        print("[Aviso]  Debes iniciar sesión primero.")
        return
    
    print("\n--- [Eliminar]  Eliminar Empleado ---")
    
    try:
        empleado_id = int(input("ID del empleado a eliminar: "))
    except ValueError:
        print("[Error] Error: Debes ingresar un número válido.")
        return
    
    confirmacion = input(f"¿Confirmas eliminar el empleado ID {empleado_id}? (s/n): ").strip().lower()
    
    if confirmacion != 's':
        print("[Error] Operación cancelada.")
        return
    
    exito = eliminar_empleado(empleado_id)
    
    if exito:
        print("[OK] Empleado eliminado correctamente (soft delete).")
    else:
        print("[Error] Error al eliminar. ¿El ID existe?")


def cerrar_sesion():
    """Cierra la sesión del usuario."""
    global USUARIO_LOGUEADO
    if USUARIO_LOGUEADO:
        print(f"[Salir] Hasta luego, {USUARIO_LOGUEADO['nombre']}!")
        USUARIO_LOGUEADO = None
    else:
        print("No hay sesión activa.")


def mostrar_menu():
    """Muestra el menú principal según el estado de autenticación."""
    if USUARIO_LOGUEADO:
        print(f"\n--- Menú ([Usuario] {USUARIO_LOGUEADO['nombre']} {USUARIO_LOGUEADO['apellido']}) ---")
        print("1. Ver lista de empleados")
        print("2. Buscar empleado")
        print("3. Editar empleado")
        print("4. Eliminar empleado")
        print("5. Cerrar sesión")
        print("6. Salir")
    else:
        print("\n--- Menú Principal ---")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Ver lista de empleados")
        print("4. Buscar empleado")
        print("5. Salir")


def main():
    """Función principal del programa."""
    # Mostrar banner
    mostrar_banner()
    
    # Probar conexión a la base de datos
    print("\n[Conexion] Conectando a la base de datos...")
    
    if not test_connection():
        print("\n[Error] No se pudo conectar a la base de datos.")
        print("   Verifica que:")
        print("   1. MariaDB esté ejecutándose")
        print("   2. El archivo .env tenga las credenciales correctas")
        print("   3. La base de datos 'empleados_db' exista")
        print("\n   Para crear la base de datos, ejecuta:")
        print("   mysql -u root -p < context/employees_schema.sql")
        sys.exit(1)
    
    # Menú principal
    while True:
        mostrar_menu()
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if not opcion:
            continue
        
        # Opciones sin login
        if not USUARIO_LOGUEADO:
            if opcion == "1":
                opcion_login()
            elif opcion == "2":
                opcion_registro()
            elif opcion == "3":
                opcion_ver_empleados()
            elif opcion == "4":
                opcion_buscar_empleado()
            elif opcion == "5":
                print("\n[Salir] ¡Gracias por usar el sistema!")
                break
            else:
                print("[Error] Opción inválida.")
        
        # Opciones con login
        else:
            if opcion == "1":
                opcion_ver_empleados()
            elif opcion == "2":
                opcion_buscar_empleado()
            elif opcion == "3":
                opcion_editar_empleado()
            elif opcion == "4":
                opcion_eliminar_empleado()
            elif opcion == "5":
                cerrar_sesion()
            elif opcion == "6":
                print("\n[Salir] ¡Gracias por usar el sistema!")
                break
            else:
                print("[Error] Opción inválida.")


# Punto de entrada
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido.")
        sys.exit(0)
