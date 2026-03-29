# agents.md - Reglas y Convenciones del Proyecto

## Información del Proyecto

**Nombre:** Sistema de Gestión de Empleados  
**Versión:** 1.0  
**Tecnologías:** Python 3.x + MariaDB  
**Metodología:** Spec Driven Development (SDD)

---

## Estructura de Carpetas

```
007_Sistema-de-Gesti-n-de-Empleados/
├── .env                    # Credenciales (NO subir a Git)
├── .gitignore              # Archivos a ignorar
├── SPEC.md                 # Especificación del proyecto
├── README.md               # Documentación principal
├── agents.md               # Este archivo - reglas para IA
├── SKILL.md                # Habilidad de documentación
├── gestionDeDatos.py       # Archivo legacy (mantener兼容性)
├── context/
│   └── employees_schema.sql    # Schema de base de datos
└── src/
    ├── __init__.py
    ├── config.py           # Carga de configuración
    ├── database.py         # Conexión a MariaDB
    ├── models.py           # Modelos de datos
    ├── auth.py             # Autenticación y seguridad
    └── main.py             # Punto de entrada
```

---

## Convenciones de Código

### 1. Nomenclatura

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Clases | PascalCase | `class Empleado:` |
| Funciones | snake_case | `def obtener_empleado():` |
| Variables | snake_case | `email_usuario` |
| Constantes | UPPER_SNAKE | `MAX_INTENTOS = 5` |
| Archivos | snake_case | `database.py` |

### 2. Documentación (OBLIGATORIO)

**Cada función debe tener un comentario descriptivo:**

```python
# Esta función obtiene un empleado por su ID de la base de datos
def obtener_empleado_por_id(empleado_id):
    """
    Obtiene un empleado específico de la base de datos.
    
    Args:
        empleado_id (int): ID único del empleado
        
    Returns:
        dict: Diccionario con los datos del empleado o None
    """
    pass
```

### 3. Seguridad (Reglas Absolutas)

- ❌ **NUNCA** guardar contraseñas en texto plano
- ❌ **NUNCA** hardcodear credenciales en el código
- ✅ **SIEMPRE** usar variables de entorno (.env)
- ✅ **SIEMPRE** hashear contraseñas con bcrypt
- ✅ **SIEMPRE** usar queries parametrizadas (evitar SQL injection)
- ✅ **SIEMPRE** validar datos de entrada

### 4. Estructura de Módulos

Cada módulo Python debe tener:
1. Docstring inicial explicando su propósito
2. Importaciones organizadas (stdlib → terceros → locales)
3. Constantes de configuración
4. Funciones/clases con docstrings
5. Comentarios antes de cada función (según SKILL.md)

---

## Reglas de Base de Datos

### Tablas Requeridas

1. **empleados** - Datos principales de empleados
2. **intentos_login** - Control de seguridad (fuerza bruta)

### Buenas Prácticas SQL

- Usar `CREATE INDEX` para optimizar búsquedas
- Preferir `SOFT DELETE` (activo = FALSE) sobre DELETE físico
- Usar transacciones para operaciones múltiples
- Validar datos antes de insertar

---

## Reglas para Agentes IA (Kiara)

### Antes de escribir código:

1. ✅ Leer SPEC.md para entender requerimientos
2. ✅ Verificar si existe agents.md para conventions
3. ✅ Revisar estructura de carpetas existente

### Al escribir código:

1. ✅ Agregar comentario descriptivo ANTES de cada función
2. ✅ Usar nombres descriptivos para variables
3. ✅ Manejar excepciones apropiadamente
4. ✅ No exponer credenciales en mensajes de error

### Después de escribir código:

1. ✅ Verificar que funciona correctamente
2. ✅ Ejecutar tests si existen
3. ✅ No dejar prints de debug en producción

---

## Validaciones Requeridas

### Registro de Empleado

| Campo | Validación |
|-------|------------|
| nombre | 2-100 caracteres, solo letras y espacios |
| apellido | 2-100 caracteres, solo letras y espacios |
| email | Formato válido, único en BD |
| password | Mínimo 8 caracteres, 1 letra + 1 número |
| telefono | Opcional, formato válido si se ingresa |
| puesto | Opcional, máximo 100 caracteres |

### Login

- Verificar cuenta no esté bloqueda
- Comparar hash de contraseña (bcrypt)
- Registrar intentos fallidos
- Bloquear tras 5 intentos fallidos (15 minutos)

---

## Contacto

**Desarrollador:** wackxion  
**Proyecto:** Reto de 100 Programas en Python  
**Nivel:** 2 - Almacenamiento y SQL con MariaDB (3/30)

---

*Este archivo define las reglas que todo agente IA debe seguir al trabajar en este proyecto.*
