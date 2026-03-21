# 🏢 Proyecto 007: Sistema de Gestión de Empleados (Secure Auth)

Bienvenido al Proyecto 007 de mi **Reto de 100 Programas en Python**. En este desarrollo, elevo el nivel de complejidad al gestionar información sensible de una empresa mediante una conexión robusta con **MariaDB**.

---

### 🚀 Objetivo del Proyecto
Desarrollar un sistema de almacenamiento persistente para empleados que permita registrar usuarios y contraseñas de forma segura, evitando los errores comunes de seguridad por defecto y aplicando técnicas de cifrado.

### 🛠️ Tecnologías y Metodología
* **Lenguaje:** Python 3.x
* **Base de Datos:** MariaDB (SQL)
* **Seguridad:** Implementación de **Hashing de contraseñas** (no texto plano) y uso de variables de entorno con `.env` [3].
* **Arquitectura:** **Spec Driven Development (SDD)**, definiendo requerimientos antes de codificar [4].
* **Asistencia:** Orquestación técnica por mi agente **Kiara** bajo el rol de **Human-in-the-loop** [5].

---

### 📂 Estructura del Proyecto
- `📁 context/`: Esquema de la base de datos (`employees_schema.sql`) para dar contexto a la IA [6].
- `📁 src/`: Lógica principal en Python.
- `📄 agents.md`: Reglas de estilo y convenciones para Kiara [7].
- `📄 .env`: Archivo protegido para credenciales de base de datos (excluido por `.gitignore`).

---

### 📋 Funcionalidades Clave
1. **Registro Seguro:** Almacenamiento de nuevos empleados con contraseñas hasheadas.
2. **Autenticación (Login):** Validación de credenciales contra la base de datos MariaDB.
3. **Gestión CRUD:** Visualización y edición de datos personales del staff.
4. **Protección contra Fuerza Bruta:** Lógica para limitar intentos fallidos de inicio de sesión [3].

---

### 🤖 Nota sobre el Desarrollo
Siguiendo la filosofía de **MoureDev**, este proyecto no es "vibe coding". He supervisado cada query SQL y función de Python generada por **Kiara**, asegurando que el sistema sea escalable y resistente a inyecciones SQL [8, 9].

**Desarrollado por [wackxion](https://github.com/wackxion) - Estudiante de Videojuegos en UNAHUR.**
Consejos para "afilar" este proyecto:
Seguridad Crítica: Recuerda que en el 2026, guardar contraseñas en texto plano es un error de los años 90 que aún se ve en auditorías
. Pídele a Kiara que use una librería como bcrypt o hashlib para el hasheo.
Actualiza tu Perfil: Al subir este repositorio, no olvides actualizar tu README principal
:
Progreso del reto: [#######   ] 7/100.
Nivel 2: Almacenamiento y SQL con MariaDB (3/30).
Variable de Entorno: Asegúrate de que el archivo .env contenga el host, usuario y contraseña de MariaDB, y que esté en tu .gitignore para no subir tus claves reales a GitHub.
¿Te gustaría que te ayude a redactar el archivo de especificaciones (spec.md) para que se lo pases a Kiara y ella diseñe las tablas de empleados?
