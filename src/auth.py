"""
Módulo de Autenticación
=======================

Gestiona la seguridad del sistema:
- Verificación de contraseñas con bcrypt
- Control de intentos de login (prevención de fuerza bruta)
- Bloqueo temporal de cuentas

Funciones:
    - verificar_password(): Compara password con hash
    - intentos_login(): Registra y controla intentos fallidos
    - esta_bloqueado(): Verifica si una cuenta está bloqueada
    - iniciar_sesion(): Valida credenciales y bloquea si es necesario
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import bcrypt
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import execute_query, execute_insert, execute_update
from config import MAX_LOGIN_ATTEMPTS, BLOCK_TIME_MINUTES
from models import obtener_empleado_por_email


def verificar_password(password_plana: str, password_hash: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password_plana (str): Contraseña ingresada por el usuario
        password_hash (str): Hash almacenado en la base de datos
        
    Returns:
        bool: True si la contraseña es correcta
    """
    try:
        return bcrypt.checkpw(
            password_plana.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception as e:
        print(f"[Error] Error al verificar contraseña: {e}")
        return False


def obtener_intentos_login(email: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene el registro de intentos de login para un email.
    
    Args:
        email (str): Correo electrónico del usuario
        
    Returns:
        dict: Datos de intentos o None si no existe registro
    """
    query = """
        SELECT id, email, intentos_fallidos, ultimo_intento, bloqueado_hasta
        FROM intentos_login 
        WHERE email = %s
    """
    
    resultados = execute_query(query, (email,))
    return resultados[0] if resultados else None


def actualizar_intentos_fallidos(email: str) -> bool:
    """
    Incrementa el contador de intentos fallidos.
    
    Args:
        email (str): Correo electrónico del usuario
        
    Returns:
        bool: True si se actualizó correctamente
    """
    intentos = obtener_intentos_login(email)
    ahora = datetime.now()
    
    if intentos:
        # Ya existe registro, actualizar
        nuevos_intentos = intentos['intentos_fallidos'] + 1
        
        # Calcular si debe bloquearse
        bloqueado_hasta = None
        if nuevos_intentos >= MAX_LOGIN_ATTEMPTS:
            bloqueado_hasta = ahora + timedelta(minutes=BLOCK_TIME_MINUTES)
        
        query = """
            UPDATE intentos_login 
            SET intentos_fallidos = %s, ultimo_intento = %s, bloqueado_hasta = %s
            WHERE email = %s
        """
        params = (nuevos_intentos, ahora, bloqueado_hasta, email)
        
    else:
        # Primer intento fallido, crear registro
        bloqueado_hasta = None
        if MAX_LOGIN_ATTEMPTS <= 1:
            bloqueado_hasta = ahora + timedelta(minutes=BLOCK_TIME_MINUTES)
        
        query = """
            INSERT INTO intentos_login 
            (email, intentos_fallidos, ultimo_intento, bloqueado_hasta)
            VALUES (%s, %s, %s, %s)
        """
        params = (email, 1, ahora, bloqueado_hasta)
    
    return execute_update(query, params) if intentos else execute_insert(query, params)


def reiniciar_intentos_login(email: str) -> bool:
    """
    Reinicia el contador de intentos fallidos (cuando login es exitoso).
    
    Args:
        email (str): Correo electrónico del usuario
        
    Returns:
        bool: True si se reinició correctamente
    """
    intentos = obtener_intentos_login(email)
    
    if intentos:
        query = """
            UPDATE intentos_login 
            SET intentos_fallidos = 0, ultimo_intento = NULL, bloqueado_hasta = NULL
            WHERE email = %s
        """
        return execute_update(query, (email,))
    
    return True  # No hay registro, no hay nada que reiniciar


def esta_bloqueado(email: str) -> Tuple[bool, Optional[str]]:
    """
    Verifica si una cuenta está bloqueada por intentos fallidos.
    
    Args:
        email (str): Correo electrónico del usuario
        
    Returns:
        tuple: (esta_bloqueado, mensaje_reason)
    """
    intentos = obtener_intentos_login(email)
    
    if not intentos:
        return False, None
    
    # Si hay bloqueo vigente
    if intentos['bloqueado_hasta']:
        bloqueado_hasta = intentos['bloqueado_hasta']
        
        if isinstance(bloqueado_hasta, str):
            bloqueado_hasta = datetime.strptime(bloqueado_hasta, '%Y-%m-%d %H:%M:%S')
        
        if bloqueado_hasta > datetime.now():
            # Ainda está bloqueado
            tiempo_restante = bloqueado_hasta - datetime.now()
            minutos = int(tiempo_restante.total_seconds() / 60)
            return True, f"Cuenta bloqueada. Intenta en {minutos} minuto(s)."
        else:
            # El bloqueo expiró, reiniciar
            reiniciar_intentos_login(email)
            return False, None
    
    return False, None


def iniciar_sesion(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Valida las credenciales de un usuario.
    
    Args:
        email (str): Correo electrónico del usuario
        password (str): Contraseña ingresada
        
    Returns:
        tuple: (exito, mensaje, datos_empleado)
    """
    # Paso 1: Verificar si la cuenta está bloqueada
    bloqueado, mensaje_bloqueo = esta_bloqueado(email)
    if bloqueado:
        return False, mensaje_bloqueo, None
    
    # Paso 2: Buscar empleado por email
    empleado = obtener_empleado_por_email(email)
    
    if not empleado:
        return False, "Email o contraseña incorrectos.", None
    
    # Paso 3: Verificar si el empleado está activo
    if not empleado.get('activo', False):
        return False, "Tu cuenta ha sido desactivada. Contacta al administrador.", None
    
    # Paso 4: Verificar la contraseña
    if not verificar_password(password, empleado['password_hash']):
        # Contraseña incorrecta - registrar intento fallido
        actualizar_intentos_fallidos(email)
        
        # Obtener intentos actuales para el mensaje
        intentos = obtener_intentos_login(email)
        intentos_restantes = MAX_LOGIN_ATTEMPTS - (intentos['intentos_fallidos'] if intentos else 1)
        
        return False, f"Email o contraseña incorrectos. Intentos restantes: {intentos_restantes}", None
    
    # Paso 5: Login exitoso - reiniciar contador
    reiniciar_intentos_login(email)
    
    # Limpiar datos sensibles antes de retornar
    empleado_limpio = {
        'id': empleado['id'],
        'nombre': empleado['nombre'],
        'apellido': empleado['apellido'],
        'email': empleado['email'],
        'telefono': empleado.get('telefono'),
        'puesto': empleado.get('puesto')
    }
    
    return True, "¡Bienvenido al sistema!", empleado_limpio


def cambiar_password(email: str, password_actual: str, password_nueva: str) -> Tuple[bool, str]:
    """
    Cambia la contraseña de un empleado.
    
    Args:
        email (str): Correo electrónico del usuario
        password_actual (str): Contraseña actual
        password_nueva (str): Nueva contraseña
        
    Returns:
        tuple: (exito, mensaje)
    """
    # Verificar contraseña actual
    empleado = obtener_empleado_por_email(email)
    
    if not empleado:
        return False, "Usuario no encontrado."
    
    if not verificar_password(password_actual, empleado['password_hash']):
        return False, "La contraseña actual es incorrecta."
    
    # Hashear nueva contraseña
    nuevo_hash = bcrypt.hashpw(
        password_nueva.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Actualizar en la base de datos
    query = "UPDATE empleados SET password_hash = %s WHERE email = %s"
    exito = execute_update(query, (nuevo_hash, email))
    
    if exito:
        return True, "Contraseña actualizada correctamente."
    else:
        return False, "Error al actualizar la contraseña."
