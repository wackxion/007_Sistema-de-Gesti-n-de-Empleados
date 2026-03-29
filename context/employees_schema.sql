-- ============================================================
-- Schema: Sistema de Gestión de Empleados
-- Base de datos: MariaDB
-- Versión: 1.0
-- ============================================================

-- Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS empleados_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE empleados_db;

-- ============================================================
-- Tabla: empleados
-- Almacena la información de los empleados del sistema
-- ============================================================
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único del empleado',
    nombre VARCHAR(100) NOT NULL COMMENT 'Nombre del empleado',
    apellido VARCHAR(100) NOT NULL COMMENT 'Apellido del empleado',
    email VARCHAR(150) NOT NULL UNIQUE COMMENT 'Correo electrónico único del empleado',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Contraseña hasheada con bcrypt',
    telefono VARCHAR(20) NULL COMMENT 'Número de teléfono del empleado',
    puesto VARCHAR(100) NULL COMMENT 'Cargo o puesto del empleado',
    activo BOOLEAN DEFAULT TRUE COMMENT 'Estado del empleado (1=activo, 0=inactivo)',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de creación del registro',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha y hora de última modificación',
    
    -- Índice para búsquedas por email (optimiza el login)
    INDEX idx_empleados_email (email),
    -- Índice para listar solo empleados activos
    INDEX idx_empleados_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla principal de empleados del sistema';

-- ============================================================
-- Tabla: intentos_login
-- Controla los intentos de inicio de sesión para prevenir ataques de fuerza bruta
-- ============================================================
CREATE TABLE IF NOT EXISTS intentos_login (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único del registro',
    email VARCHAR(150) NOT NULL COMMENT 'Email del usuario que intenta iniciar sesión',
    intentos_fallidos INT DEFAULT 0 COMMENT 'Contador de intentos fallidos consecutivos',
    ultimo_intento DATETIME NULL COMMENT 'Fecha y hora del último intento fallido',
    bloqueado_hasta DATETIME NULL COMMENT 'Fecha y hora hasta la cual el usuario está bloqueado',
    
    -- Índice para buscar rápido por email
    INDEX idx_intentos_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Control de intentos de login para prevención de fuerza bruta';

-- ============================================================
-- Datos de prueba (empleados de ejemplo)
-- NOTA: Las contraseñas están hasheadas con bcrypt
-- Password: "Empleado123" para todos los usuarios de prueba
-- ============================================================
-- INSERT INTO empleados (nombre, apellido, email, password_hash, telefono, puesto) VALUES
-- ('Juan', 'Pérez', 'juan.perez@empresa.com', '$2b$12$Kw5z8Yh3X1qW2pL8mN4cO0eF9gH7iJ8kLmNoPqRsTuVwXyZ1234567890A', '555-0101', 'Desarrollador'),
-- ('María', 'García', 'maria.garcia@empresa.com', '$2b$12$Kw5z8Yh3X1qW2pL8mN4cO0eF9gH7iJ8kLmNoPqRsTuVwXyZ1234567890A', '555-0102', 'Diseñadora'),
-- ('Carlos', 'Rodríguez', 'carlos.rodriguez@empresa.com', '$2b$12$Kw5z8Yh3X1qW2pL8mN4cO0eF9gH7iJ8kLmNoPqRsTuVwXyZ1234567890A', '555-0103', 'Gerente');

-- ============================================================
-- Tabla: actividades
-- Almacena las actividades/tareas de cada empleado
-- ============================================================
CREATE TABLE IF NOT EXISTS actividades (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único de la actividad',
    empleado_id INT NOT NULL COMMENT 'ID del empleado (FK)',
    nombre_actividad VARCHAR(200) NOT NULL COMMENT 'Nombre/título de la actividad',
    fecha DATE NOT NULL COMMENT 'Fecha de la actividad',
    hora TIME NOT NULL COMMENT 'Hora de la actividad',
    descripcion TEXT NULL COMMENT 'Descripción adicional de la actividad',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha y hora de creación',
    
    -- Clave foránea al empleado
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    
    -- Índice para búsquedas por empleado
    INDEX idx_actividades_empleado (empleado_id),
    -- Índice para búsquedas por fecha
    INDEX idx_actividades_fecha (fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Actividades/tareas de cada empleado';

-- ============================================================
-- Verificar estructura creada
-- ============================================================
-- SHOW TABLES;
-- DESCRIBE empleados;
-- DESCRIBE intentos_login;
-- DESCRIBE actividades;
