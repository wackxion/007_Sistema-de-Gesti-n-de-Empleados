"""
Módulo de Base de Datos
=======================

Gestiona la conexión con MariaDB y proporciona funciones
utilitarias para ejecutar queries de forma segura.

Funciones:
    - get_connection(): Obtiene una conexión a la base de datos
    - execute_query(): Ejecuta una query con parámetros (seguro)
    - execute_insert(): Inserta un registro y retorna el ID
    - execute_many(): Ejecuta múltiples operaciones
"""

import pymysql
from pymysql import Error
from typing import Optional, List, Tuple, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import get_mysql_connection_params


def get_connection():
    """
    Establece y retorna una conexión a la base de datos MariaDB.
    
    Returns:
        pymysql.connection: Objeto de conexión a la BD
        None: Si hay error al conectar
        
    Raises:
        Error: Si no se puede conectar (la excepción es propagada)
    """
    try:
        connection = pymysql.connect(
            **get_mysql_connection_params(),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Error as e:
        print(f"Error al conectar con MariaDB: {e}")
        raise


def execute_query(query: str, params: Optional[Tuple] = None, fetch: bool = True):
    """
    Ejecuta una consulta SELECT y retorna los resultados.
    
    Args:
        query (str): Query SQL con marcadores %s (no usar f-strings!)
        params (tuple): Parámetros para la query (previene SQL injection)
        fetch (bool): Si True, retorna resultados; si False, solo ejecuta
        
    Returns:
        list: Lista de resultados (si fetch=True)
        bool: True si la query se ejecutó exitosamente
        
    Example:
        >>> resultados = execute_query(
        ...     "SELECT * FROM empleados WHERE activo = %s",
        ...     (True,)
        ... )
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Ejecutar con parámetros (previene SQL injection)
        cursor.execute(query, params or ())
        
        if fetch:
            resultados = cursor.fetchall()
            return resultados
        else:
            connection.commit()
            return True
            
    except Error as e:
        print(f"Error en la query: {e}")
        print(f"   Query: {query}")
        print(f"   Params: {params}")
        if connection:
            connection.rollback()
        return None if fetch else False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def execute_insert(query: str, params: Tuple) -> Optional[int]:
    """
    Ejecuta una consulta INSERT y retorna el ID del registro insertado.
    
    Args:
        query (str): Query INSERT con marcadores %s
        params (tuple): Valores a insertar
        
    Returns:
        int: ID del registro insertado
        None: Si hay error
        
    Example:
        >>> nuevo_id = execute_insert(
        ...     "INSERT INTO empleados (nombre, email) VALUES (%s, %s)",
        ...     ("Juan", "juan@email.com")
        ... )
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Ejecutar con parámetros (previene SQL injection)
        cursor.execute(query, params)
        connection.commit()
        
        # Retornar el ID del registro insertado
        return cursor.lastrowid
        
    except Error as e:
        print(f"Error al insertar: {e}")
        if connection:
            connection.rollback()
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def execute_update(query: str, params: Tuple) -> bool:
    """
    Ejecuta una consulta UPDATE y confirma los cambios.
    
    Args:
        query (str): Query UPDATE con marcadores %s
        params (tuple): Valores a actualizar
        
    Returns:
        bool: True si se actualizó correctamente
        
    Example:
        >>> exito = execute_update(
        ...     "UPDATE empleados SET nombre = %s WHERE id = %s",
        ...     ("Juan Carlos", 1)
        ... )
    """
    return execute_query(query, params, fetch=False)


def execute_delete(query: str, params: Tuple) -> bool:
    """
    Ejecuta una consulta DELETE y confirma los cambios.
    
    Args:
        query (str): Query DELETE con marcadores %s
        params (tuple): Condición de eliminación
        
    Returns:
        bool: True si se eliminó correctamente
        
    Note:
        Se recomienda usar soft delete (UPDATE activo = False)
        en lugar de DELETE físico para mantener auditoría.
    """
    return execute_query(query, params, fetch=False)


def test_connection() -> bool:
    """
    Prueba la conexión a la base de datos.
    
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        connection = get_connection()
        if connection:
            print("Conexion a MariaDB exitosa!")
            connection.close()
            return True
    except Error as e:
        print(f"Error de conexion: {e}")
    return False
