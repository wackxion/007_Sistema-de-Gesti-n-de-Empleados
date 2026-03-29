# 📋 SPEC.md - Sistema de Gestión de Empleados

## 1. Requisitos Funcionales

### 1.1 Registro de Empleados
- El sistema debe permitir registrar nuevos empleados con los siguientes datos:
  - Nombre (obligatorio, texto)
  - Apellido (obligatorio, texto)
  - Correo electrónico (obligatorio, único, formato válido)
  - Contraseña (obligatoria, minimo 8 caracteres)
  - Puesto/Telefono (opcional)
- Cada empleado debe tener un ID único auto-generado
- La contraseña debe ser hasheada antes de almacenarse (nunca en texto plano)

### 1.2 Autenticación (Login)
- El sistema debe validar credenciales contra la base de datos
- Debe verificar que el email exista y la contraseña coincida con el hash
- Debe manejar intentos fallidos para prevenir ataques de fuerza bruta
- Debe bloquear temporalmente la cuenta después de X intentos fallidos

### 1.3 Gestión CRUD
| Operación | Descripción |
|------------|-------------|
| **Create** | Insertar nuevos empleados |
| **Read** | Listar todos los empleados / buscar por ID o email |
| **Update** | Editar información personal (nombre, apellido, teléfono, puesto) |
| **Delete** | Eliminar empleados (soft delete recomendado) |

### 1.4 Control de Acceso
- Solo usuarios autenticados pueden acceder al sistema
- Roles opcionales: Administrador, Usuario Regular

---

## 2. Modelo de Datos

### 2.1 Diagrama de Entidad-Relación

```
┌─────────────────────┐       ┌─────────────────────┐
│      empleados      │       │   intentos_login    │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK)             │
│ nombre              │       │ usuario_id (FK)     │
│ apellido            │       │ intentos_fallidos   │
│ email (UNIQUE)      │       │ ultimo_intento      │
│ password_hash       │       │ bloqueado_hasta     │
│ telefono            │       └─────────────────────┘
│ puesto              │
│ activo (BOOLEAN)    │
│ fecha_creacion      │
│ fecha_actualizacion │
└─────────────────────┘
```

### 2.2 Detalle de Tablas

#### Tabla: `empleados`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Identificador único |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre del empleado |
| `apellido` | VARCHAR(100) | NOT NULL | Apellido del empleado |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE | Correo electrónico |
| `password_hash` | VARCHAR(255) | NOT NULL | Contraseña hasheada |
| `telefono` | VARCHAR(20) | NULL | Teléfono de contacto |
| `puesto` | VARCHAR(100) | NULL | Cargo del empleado |
| `activo` | BOOLEAN | DEFAULT TRUE | Estado del empleado |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| `updated_at` | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Última modificación |

#### Tabla: `intentos_login`

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| `id` | INT | PK, AUTO_INCREMENT | Identificador único |
| `email` | VARCHAR(150) | NOT NULL, FK | Email del usuario |
| `intentos_fallidos` | INT | DEFAULT 0 | Contador de fallos |
| `ultimo_intento` | DATETIME | NULL | Último intento fallido |
| `bloqueado_hasta` | DATETIME | NULL | Fecha de desbloqueo |

### 2.3 Índices Recomendados

```sql
-- Optimizar búsquedas por email (login)
CREATE INDEX idx_empleados_email ON empleados(email);

-- Optimizar búsquedas de intentos login
CREATE INDEX idx_intentos_email ON intentos_login(email);
```

---

## 3. Casos de Uso

### 3.1 Registro de Nuevo Empleado

```
Actor: Usuario Administrador
Flujo Principal:
1. El usuario accede al formulario de registro
2. Ingresa: nombre, apellido, email, contraseña, teléfono (opc), puesto (opc)
3. El sistema valida:
   - Email no existe previamente
   - Contraseña cumple requisitos mínimos (8+ chars)
   - Todos los campos obligatorios completos
4. El sistema hashea la contraseña con bcrypt
5. El sistema inserta el registro en la base de datos
6. El sistema retorna mensaje de éxito
```

### 3.2 Inicio de Sesión (Login)

```
Actor: Empleado
Flujo Principal:
1. El usuario ingresa email y contraseña
2. El sistema busca el email en la tabla empleados
3. Si existe:
   a. Verifica si la cuenta está bloqueada (intentos > 5)
   b. Compara la contraseña ingresada con el hash almacenado
   c. Si es correcta: inicia sesión, reinicia contador de fallos
   d. Si es incorrecta: incrementa contador de intentos fallidos
4. Si el email no existe: retorna error de autenticación
5. Si intentos fallidos >= 5: bloquea cuenta por 15 minutos
```

### 3.3 Consultar Lista de Empleados

```
Actor: Usuario autenticado
Flujo Principal:
1. El usuario solicita ver la lista de empleados
2. El sistema verifica que el usuario esté autenticado
3. El sistema consulta empleados donde activo = TRUE
4. El sistema retorna lista con: id, nombre, apellido, email, puesto
```

### 3.4 Actualizar Empleado

```
Actor: Administrador
Flujo Principal:
1. El usuario selecciona un empleado a editar
2. El usuario modifica los campos deseados
3. El sistema valida:
   - Email nuevo no esté en uso por otro empleado
   - Campos obligatorios presentes
4. El sistema actualiza el registro
5. El sistema retorna mensaje de éxito
```

### 3.5 Eliminar Empleado

```
Actor: Administrador
Flujo Principal:
1. El usuario selecciona un empleado a eliminar
2. El sistema solicita confirmación
3. El sistema marca activo = FALSE (soft delete)
4. El sistema retorna mensaje de éxito
```

---

## 4. Reglas de Negocio

### 4.1 Validaciones de Datos

| Campo | Regla |
|-------|-------|
| Nombre | Min 2 caracteres, max 100, solo letras y espacios |
| Apellido | Min 2 caracteres, max 100, solo letras y espacios |
| Email | Formato válido de email (regex), único en BD |
| Contraseña | Mínimo 8 caracteres, al menos 1 letra y 1 número |
| Teléfono | Formato opcional, válido si se ingresa |
| Puesto | Max 100 caracteres |

### 4.2 Reglas de Seguridad

| Regla | Descripción |
|-------|-------------|
| Hash de contraseña | Usar bcrypt con salt único por usuario |
| Intentos máximos | Bloquear tras 5 intentos fallidos |
| Tiempo de bloqueo | 15 minutos de espera después de bloqueo |
| Sesión | Tiempo máximo de inactividad: 30 minutos |
| Contraseña | Cambiar cada 90 días (futuro) |

### 4.3 Reglas de Negocio Adicionales

- **Soft Delete**: No eliminar físicamente registros, marcar como inactivos
- **Auditoría**: Registrar fecha de creación y última modificación
- **Unicidad**: Un email solo puede pertenecer a un empleado activo
- **Paginación**: Máximo 50 empleados por página en listados

---

## 5. Seguridad

### 5.1 Protección de Contraseñas

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE SEGURIDAD                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  USUARIO                                                    │
│      │                                                      │
│      ▼                                                      │
│  ┌─────────────────────┐                                    │
│  │ Input: "miPassword" │                                    │
│  └─────────────────────┘                                    │
│            │                                                │
│            ▼                                                │
│  ┌─────────────────────────────────────┐                   │
│  │ bcrypt.hash(password + salt_único)  │                   │
│  └─────────────────────────────────────┘                   │
│            │                                                │
│            ▼                                                │
│  ┌─────────────────────────────────────┐                   │
│  │ $2b$12$Kw5z8Yh3X... (hash de 60 caracteres)            │
│  └─────────────────────────────────────┘                   │
│            │                                                │
│            ▼                                                │
│  ┌─────────────────────────────────────┐                   │
│  │ Se almacena en: password_hash       │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Medidas de Seguridad Implementadas

| Medida | Descripción | Implementación |
|--------|-------------|----------------|
| **Hashing** | Contraseñas nunca en texto plano | bcrypt |
| **Variables de entorno** | Credenciales fuera del código | .env + python-dotenv |
| **SQL Injection** | Queries parametrizadas | Prepared statements |
| **Fuerza bruta** | Limitar intentos fallidos | Tabla intentos_login |
| **Bloqueo temporal** | Después de X intentos | 15 minutos de espera |
| **Git ignore** | No subir credenciales | .gitignore |

### 5.3 Estructura del archivo .env

```env
# Configuración de Base de Datos MariaDB
DB_HOST=localhost
DB_PORT=3306
DB_NAME=empleados_db
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña_segura

# Configuración de Seguridad
SECRET_KEY=clave_secreta_para_sesiones
BCRYPT_ROUNDS=12
MAX_LOGIN_ATTEMPTS=5
BLOCK_TIME_MINUTES=15
```

### 5.4 Lista de archivos a crear/ignorar

```gitignore
# Archivos sensibles
.env
.env.local
*.pyc
__pycache__/
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 6.-stack Tecnológico

| Componente | Tecnología |
|------------|-------------|
| Lenguaje | Python 3.x |
| Base de datos | MariaDB |
| ORM/Driver | mysql-connector-python |
| Hashing | bcrypt |
| Variables de entorno | python-dotenv |
| Testing | pytest |

---

## 7. Próximos Pasos (Roadmap)

- [ ] Crear estructura de carpetas (src/, context/)
- [ ] Generar script SQL del schema
- [ ] Configurar archivo .env
- [ ] Implementar conexión a MariaDB
- [ ] Crear clase DatabaseConnection
- [ ] Implementar modelo Empleado (CRUD)
- [ ] Implementar sistema de autenticación
- [ ] Implementar protección contra fuerza bruta
- [ ] Crear CLI o menú principal
- [ ] Escribir tests con pytest

---

**Documento generado bajo metodología Spec Driven Development (SDD)**
**Proyecto: Sistema de Gestión de Empleados v1.0**
