"""
Módulo de Modelos de Datos
=========================

Define las operaciones CRUD (Create, Read, Update, Delete)
para la tabla de empleados en la base de datos.

Funciones:
    - crear_empleado(): Registra un nuevo empleado
    - obtener_empleados(): Lista todos los empleados activos
    - obtener_empleado_por_id(): Busca un empleado por ID
    - obtener_empleado_por_email(): Busca un empleado por email
    - actualizar_empleado(): Modifica datos de un empleado
    - eliminar_empleado(): "Elimina" un empleado (soft delete)
    - buscar_empleados(): Busca por nombre, apellido o email
"""

from typing import Optional, List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import execute_query, execute_insert, execute_update, execute_delete
import bcrypt


def crear_empleado(
    nombre: str,
    apellido: str,
    email: str,
    password_plana: str,
    telefono: Optional[str] = None,
    puesto: Optional[str] = None
) -> Optional[int]:
    """
    Registra un nuevo empleado en la base de datos.
    
    La contraseña es hasheada con bcrypt antes de almacenarse.
    
    Args:
        nombre (str): Nombre del empleado
        apellido (str): Apellido del empleado
        email (str): Correo electrónico único
        password_plana (str): Contraseña en texto plano
        telefono (str, optional): Número de teléfono
        puesto (str, optional): Cargo del empleado
        
    Returns:
        int: ID del empleado creado
        None: Si hay error (email duplicado, etc)
    """
    # Hashear la contraseña con bcrypt
    password_hash = bcrypt.hashpw(
        password_plana.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    query = """
        INSERT INTO empleados 
        (nombre, apellido, email, password_hash, telefono, puesto) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    params = (nombre, apellido, email, password_hash, telefono, puesto)
    
    nuevo_id = execute_insert(query, params)
    
    if nuevo_id:
        print(f"[OK] Empleado creado con ID: {nuevo_id}")
    else:
        print(f"[Error] Error al crear empleado (¿email duplicado?)")
    
    return nuevo_id


def obtener_empleados(activos_solo: bool = True) -> List[Dict[str, Any]]:
    """
    Obtiene la lista de empleados de la base de datos.
    
    Args:
        activos_solo (bool): Si True, solo empleados activos
        
    Returns:
        list: Lista de diccionarios con datos de empleados
    """
    if activos_solo:
        query = """
            SELECT id, nombre, apellido, email, telefono, puesto, 
                   activo, created_at, updated_at
            FROM empleados 
            WHERE activo = %s
            ORDER BY apellido, nombre
        """
        params = (True,)
    else:
        query = """
            SELECT id, nombre, apellido, email, telefono, puesto, 
                   activo, created_at, updated_at
            FROM empleados 
            ORDER BY apellido, nombre
        """
        params = ()
    
    return execute_query(query, params) or []


def obtener_empleado_por_id(empleado_id: int) -> Optional[Dict[str, Any]]:
    """
    Busca un empleado específico por su ID.
    
    Args:
        empleado_id (int): ID único del empleado
        
    Returns:
        dict: Datos del empleado
        None: Si no se encuentra
    """
    query = """
        SELECT id, nombre, apellido, email, telefono, puesto, 
               activo, created_at, updated_at
        FROM empleados 
        WHERE id = %s
    """
    
    resultados = execute_query(query, (empleado_id,))
    return resultados[0] if resultados else None


def obtener_empleado_por_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Busca un empleado específico por su email.
    
    Args:
        email (str): Correo electrónico del empleado
        
    Returns:
        dict: Datos del empleado (incluye password_hash)
        None: Si no se encuentra
    """
    query = """
        SELECT id, nombre, apellido, email, password_hash, telefono, 
               puesto, activo, created_at, updated_at
        FROM empleados 
        WHERE email = %s
    """
    
    resultados = execute_query(query, (email,))
    return resultados[0] if resultados else None


def actualizar_empleado(
    empleado_id: int,
    nombre: Optional[str] = None,
    apellido: Optional[str] = None,
    telefono: Optional[str] = None,
    puesto: Optional[str] = None
) -> bool:
    """
    Actualiza los datos de un empleado existente.
    
    Args:
        empleado_id (int): ID del empleado a actualizar
        nombre (str, optional): Nuevo nombre
        apellido (str, optional): Nuevo apellido
        telefono (str, optional): Nuevo teléfono
        puesto (str, optional): Nuevo puesto
        
    Returns:
        bool: True si se actualizó correctamente
    """
    # Construir query dinámico según campos a actualizar
    campos = []
    valores = []
    
    if nombre is not None:
        campos.append("nombre = %s")
        valores.append(nombre)
    if apellido is not None:
        campos.append("apellido = %s")
        valores.append(apellido)
    if telefono is not None:
        campos.append("telefono = %s")
        valores.append(telefono)
    if puesto is not None:
        campos.append("puesto = %s")
        valores.append(puesto)
    
    if not campos:
        print("[Aviso]️  No hay campos para actualizar")
        return False
    
    # Agregar ID al final de los valores
    valores.append(empleado_id)
    
    query = f"UPDATE empleados SET {', '.join(campos)} WHERE id = %s"
    
    return execute_update(query, tuple(valores))


def eliminar_empleado(empleado_id: int, hard_delete: bool = False) -> bool:
    """
    Elimina un empleado (soft delete por defecto).
    
    Args:
        empleado_id (int): ID del empleado a eliminar
        hard_delete (bool): Si True, elimina físicamente el registro
        
    Returns:
        bool: True si se eliminó correctamente
    """
    if hard_delete:
        # Eliminación física (no recomendada)
        query = "DELETE FROM empleados WHERE id = %s"
    else:
        # Soft delete - marcar como inactivo (recomendado)
        query = "UPDATE empleados SET activo = FALSE WHERE id = %s"
    
    return execute_delete(query, (empleado_id,))


def buscar_empleados(termino: str) -> List[Dict[str, Any]]:
    """
    Busca empleados por nombre, apellido o email.
    
    Args:
        termino (str): Texto a buscar
        
    Returns:
        list: Lista de empleados que coinciden
    """
    termino_busqueda = f"%{termino}%"
    
    query = """
        SELECT id, nombre, apellido, email, telefono, puesto, 
               activo, created_at, updated_at
        FROM empleados 
        WHERE activo = %s 
          AND (nombre LIKE %s 
               OR apellido LIKE %s 
               OR email LIKE %s)
        ORDER BY apellido, nombre
    """
    
    params = (True, termino_busqueda, termino_busqueda, termino_busqueda)
    
    return execute_query(query, params) or []


def contar_empleados(activos_solo: bool = True) -> int:
    """
    Cuenta el número de empleados en la base de datos.
    
    Args:
        activos_solo (bool): Si True, solo cuenta empleados activos
        
    Returns:
        int: Número de empleados
    """
    if activos_solo:
        query = "SELECT COUNT(*) as total FROM empleados WHERE activo = %s"
        params = (True,)
    else:
        query = "SELECT COUNT(*) as total FROM empleados"
        params = ()
    
    resultados = execute_query(query, params)
    return resultados[0]['total'] if resultados else 0


# ============================================================
# Funciones de Actividades
# ============================================================

def crear_actividad(
    empleado_id: int,
    nombre_actividad: str,
    fecha: str,
    hora: str,
    descripcion: Optional[str] = None
) -> Optional[int]:
    """
    Registra una nueva actividad para un empleado.
    
    Args:
        empleado_id (int): ID del empleado
        nombre_actividad (str): Nombre de la actividad
        fecha (str): Fecha de la actividad (formato YYYY-MM-DD)
        hora (str): Hora de la actividad (formato HH:MM:SS)
        descripcion (str, optional): Descripción adicional
        
    Returns:
        int: ID de la actividad creada
        None: Si hay error
    """
    query = """
        INSERT INTO actividades 
        (empleado_id, nombre_actividad, fecha, hora, descripcion) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    params = (empleado_id, nombre_actividad, fecha, hora, descripcion)
    
    return execute_insert(query, params)


def obtener_actividades_por_empleado(empleado_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todas las actividades de un empleado.
    
    Args:
        empleado_id (int): ID del empleado
        
    Returns:
        list: Lista de actividades del empleado
    """
    query = """
        SELECT id, empleado_id, nombre_actividad, fecha, hora, 
               descripcion, created_at
        FROM actividades 
        WHERE empleado_id = %s
        ORDER BY fecha DESC, hora DESC
    """
    
    return execute_query(query, (empleado_id,)) or []


def obtener_todas_actividades() -> List[Dict[str, Any]]:
    """
    Obtiene todas las actividades de todos los empleados.
    
    Returns:
        list: Lista de todas las actividades con datos del empleado
    """
    query = """
        SELECT a.id, a.empleado_id, a.nombre_actividad, a.fecha, a.hora, 
               a.descripcion, a.created_at,
               e.nombre, e.apellido
        FROM actividades a
        INNER JOIN empleados e ON a.empleado_id = e.id
        ORDER BY a.fecha DESC, a.hora DESC
    """
    
    return execute_query(query) or []


def actualizar_actividad(
    actividad_id: int,
    nombre_actividad: Optional[str] = None,
    fecha: Optional[str] = None,
    hora: Optional[str] = None,
    descripcion: Optional[str] = None
) -> bool:
    """
    Actualiza los datos de una actividad.
    
    Args:
        actividad_id (int): ID de la actividad a actualizar
        nombre_actividad (str, optional): Nuevo nombre
        fecha (str, optional): Nueva fecha
        hora (str, optional): Nueva hora
        descripcion (str, optional): Nueva descripción
        
    Returns:
        bool: True si se actualizó correctamente
    """
    campos = []
    valores = []
    
    if nombre_actividad is not None:
        campos.append("nombre_actividad = %s")
        valores.append(nombre_actividad)
    if fecha is not None:
        campos.append("fecha = %s")
        valores.append(fecha)
    if hora is not None:
        campos.append("hora = %s")
        valores.append(hora)
    if descripcion is not None:
        campos.append("descripcion = %s")
        valores.append(descripcion)
    
    if not campos:
        return False
    
    valores.append(actividad_id)
    
    query = f"UPDATE actividades SET {', '.join(campos)} WHERE id = %s"
    
    return execute_update(query, tuple(valores))


def eliminar_actividad(actividad_id: int) -> bool:
    """
    Elimina una actividad.
    
    Args:
        actividad_id (int): ID de la actividad a eliminar
        
    Returns:
        bool: True si se eliminó correctamente
    """
    query = "DELETE FROM actividades WHERE id = %s"
    return execute_delete(query, (actividad_id,))


# ============================================================
# Funciones de Registro de Actividades (Log)
# ============================================================

def registrar_actividad(
    empleado_id: Optional[int],
    nombre_empleado: Optional[str],
    tipo_accion: str,
    descripcion: Optional[str] = None
) -> Optional[int]:
    """
    Registra una actividad en el log global.
    
    Args:
        empleado_id (int): ID del empleado (puede ser None si no hay sesión)
        nombre_empleado (str): Nombre del empleado
        tipo_accion (str): Tipo de acción (login, logout, agregar_actividad, etc.)
        descripcion (str): Descripción adicional
        
    Returns:
        int: ID del registro
        None: Si hay error
    """
    query = """
        INSERT INTO registro_actividades 
        (empleado_id, nombre_empleado, tipo_accion, descripcion) 
        VALUES (%s, %s, %s, %s)
    """
    
    params = (empleado_id, nombre_empleado, tipo_accion, descripcion)
    
    return execute_insert(query, params)


def obtener_registro_actividades(limite: int = 100) -> List[Dict[str, Any]]:
    """
    Obtiene el registro de actividades global.
    
    Args:
        limite: Número máximo de registros a obtener
        
    Returns:
        list: Lista de registros de actividades
    """
    query = """
        SELECT id, empleado_id, nombre_empleado, tipo_accion, descripcion, fecha_hora
        FROM registro_actividades
        ORDER BY fecha_hora DESC
        LIMIT %s
    """
    
    return execute_query(query, (limite,)) or []
