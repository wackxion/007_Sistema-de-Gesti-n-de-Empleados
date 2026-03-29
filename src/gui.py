"""
Interfaz Gráfica de Usuario (GUI)
=================================

Interfaz con botones para el Sistema de Gestion de Empleados.
Utiliza tkinter (incluido en Python).

Usage:
    python src/gui.py
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional
import sys
import os

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import test_connection
from auth import iniciar_sesion
from models import (
    crear_empleado,
    obtener_empleados,
    buscar_empleados,
    actualizar_empleado,
    eliminar_empleado,
    obtener_actividades_por_empleado,
    crear_actividad,
    eliminar_actividad,
    registrar_actividad,
    obtener_registro_actividades
)


class AplicacionEmpleados:
    """
    Clase principal de la aplicacion con interfaz grafica.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestion de Empleados")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Variable para almacenar el usuario logueado
        self.usuario_logueado = None
        
        # Colores
        self.color_fondo = "#f0f0f0"
        self.color_boton = "#4CAF50"
        self.color_boton_hover = "#45a049"
        self.color_texto = "#333333"
        
        self.root.configure(bg=self.color_fondo)
        
        # Verificar conexion a la base de datos
        if not test_connection():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.\nVerifica que MariaDB este ejecutandose.")
            self.root.destroy()
            return
        
        # Crear widgets
        self.crear_widgets()
        
        # Mostrar pantalla de login
        self.mostrar_login()
    
    def crear_widgets(self):
        """Crea los elementos de la interfaz."""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg=self.color_fondo)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titulo
        self.label_titulo = tk.Label(
            self.frame_principal,
            text="Sistema de Gestion de Empleados",
            font=("Arial", 18, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        )
        self.label_titulo.pack(pady=(0, 20))
        
        # Frame contenido (se cambiara segun la vista)
        self.frame_contenido = tk.Frame(self.frame_principal, bg=self.color_fondo)
        self.frame_contenido.pack(fill=tk.BOTH, expand=True)
    
    def limpiar_frame(self):
        """Limpia el frame de contenido."""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    
    # ============================================
    # VISTAS
    # ============================================
    
    def mostrar_login(self):
        """Muestra la pantalla de inicio de sesion."""
        self.limpiar_frame()
        
        # Email
        tk.Label(self.frame_contenido, text="Email:", bg=self.color_fondo, fg=self.color_texto).pack(anchor=tk.W, pady=(10, 5))
        self.entry_email = tk.Entry(self.frame_contenido, font=("Arial", 12), width=30)
        self.entry_email.pack(fill=tk.X, pady=(0, 10))
        
        # Contrasena
        tk.Label(self.frame_contenido, text="Contrasena:", bg=self.color_fondo, fg=self.color_texto).pack(anchor=tk.W, pady=(10, 5))
        self.entry_password = tk.Entry(self.frame_contenido, font=("Arial", 12), width=30, show="*")
        self.entry_password.pack(fill=tk.X, pady=(0, 20))
        
        # Boton login
        btn_login = tk.Button(
            self.frame_contenido,
            text="Iniciar Sesion",
            font=("Arial", 12, "bold"),
            bg=self.color_boton,
            fg="white",
            command=self.action_login,
            cursor="hand2",
            width=20
        )
        btn_login.pack(pady=10)
        
        # Boton registro
        btn_registro = tk.Button(
            self.frame_contenido,
            text="Registrarse",
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            command=self.mostrar_registro,
            cursor="hand2",
            width=15
        )
        btn_registro.pack(pady=5)
        
        # Bind Enter key
        self.entry_password.bind("<Return>", lambda e: self.action_login())
    
    def mostrar_registro(self):
        """Muestra el formulario de registro."""
        self.limpiar_frame()
        
        # Titulo
        tk.Label(self.frame_contenido, text="Nuevo Empleado", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=(0, 15))
        
        # Nombre
        tk.Label(self.frame_contenido, text="Nombre:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_nombre = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_nombre.pack(fill=tk.X, pady=(0, 10))
        
        # Apellido
        tk.Label(self.frame_contenido, text="Apellido:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_apellido = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_apellido.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        tk.Label(self.frame_contenido, text="Email:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_email = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_email.pack(fill=tk.X, pady=(0, 10))
        
        # Contrasena
        tk.Label(self.frame_contenido, text="Contrasena (min 8 caracteres):", bg=self.color_fondo).pack(anchor=tk.W)
        entry_password = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30, show="*")
        entry_password.pack(fill=tk.X, pady=(0, 10))
        
        # Telefono
        tk.Label(self.frame_contenido, text="Telefono (opcional):", bg=self.color_fondo).pack(anchor=tk.W)
        entry_telefono = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_telefono.pack(fill=tk.X, pady=(0, 10))
        
        # Puesto
        tk.Label(self.frame_contenido, text="Puesto (opcional):", bg=self.color_fondo).pack(anchor=tk.W)
        entry_puesto = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_puesto.pack(fill=tk.X, pady=(0, 15))
        
        # Funcion para registrar
        def action_registrar():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            email = entry_email.get().strip()
            password = entry_password.get().strip()
            telefono = entry_telefono.get().strip()
            puesto = entry_puesto.get().strip()
            
            # Validaciones
            if not nombre or not apellido or not email or not password:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            
            if len(password) < 8:
                messagebox.showerror("Error", "La contrasena debe tener al menos 8 caracteres.")
                return
            
            if '@' not in email:
                messagebox.showerror("Error", "Email invalido.")
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
                messagebox.showinfo("Exito", f"Empleado registrado con ID: {nuevo_id}")
                self.mostrar_login()
            else:
                messagebox.showerror("Error", "No se pudo registrar. El email ya puede existir.")
        
        # Botones
        frame_botones = tk.Frame(self.frame_contenido, bg=self.color_fondo)
        frame_botones.pack(pady=10)
        
        btn_guardar = tk.Button(
            frame_botones,
            text="Registrarse",
            font=("Arial", 11, "bold"),
            bg=self.color_boton,
            fg="white",
            command=action_registrar,
            cursor="hand2",
            width=12
        )
        btn_guardar.pack(side=tk.LEFT, padx=5)
        
        btn_volver = tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            command=self.mostrar_login,
            cursor="hand2",
            width=12
        )
        btn_volver.pack(side=tk.LEFT, padx=5)
    
    def mostrar_menu_principal(self):
        """Muestra el menu principal con opciones."""
        self.limpiar_frame()
        
        # Bienvenida
        nombre_usuario = f"{self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}"
        tk.Label(
            self.frame_contenido,
            text=f"Bienvenido, {nombre_usuario}",
            font=("Arial", 14, "bold"),
            bg=self.color_fondo
        ).pack(pady=(0, 20))
        
        # Botones del menu
        botones = [
            ("Ver Lista de Empleados", self.mostrar_lista_empleados, "#2196F3"),
            ("Buscar Empleado", self.mostrar_buscar, "#FF9800"),
            ("Gestionar Actividades", self.mostrar_actividades, "#4CAF50"),
            ("Editar mi Perfil", self.mostrar_editar_perfil, "#9C27B0"),
            ("Cerrar Sesion", self.action_logout, "#f44336"),
        ]
        
        for texto, comando, color in botones:
            btn = tk.Button(
                self.frame_contenido,
                text=texto,
                font=("Arial", 12),
                bg=color,
                fg="white",
                command=comando,
                cursor="hand2",
                width=25,
                height=2
            )
            btn.pack(pady=8)
    
    def mostrar_lista_empleados(self):
        """Muestra la lista de empleados y el registro global de actividades."""
        # Registrar que alguien vio la lista
        if self.usuario_logueado:
            nombre = f"{self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}"
            registrar_actividad(self.usuario_logueado['id'], nombre, "vio_lista", "Vio la lista de empleados")
        
        self.limpiar_frame()
        
        # Titulo
        tk.Label(self.frame_contenido, text="Lista de Empleados y Registro de Actividades", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=(0, 10))
        
        # Obtener empleados
        empleados = obtener_empleados()
        
        if not empleados:
            tk.Label(self.frame_contenido, text="No hay empleados registrados.", bg=self.color_fondo).pack(pady=20)
        else:
            # Frame para la lista de empleados (izquierda) y registro (derecha)
            frame_principal = tk.Frame(self.frame_contenido, bg=self.color_fondo)
            frame_principal.pack(fill=tk.BOTH, expand=True)
            
            # Frame izquierdo: lista de empleados
            frame_izquierdo = tk.Frame(frame_principal, bg=self.color_fondo)
            frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            # Treeview para mostrar tabla de empleados
            columns = ("ID", "Nombre", "Apellido", "Email", "Puesto")
            tree = ttk.Treeview(frame_izquierdo, columns=columns, show="headings", height=15)
            
            # Encabezados
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=80)
            
            # Datos
            for emp in empleados:
                tree.insert("", tk.END, values=(
                    emp["id"],
                    emp["nombre"],
                    emp["apellido"],
                    emp["email"],
                    emp.get("puesto", "")
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Frame derecho: REGISTRO GLOBAL DE ACTIVIDADES
            frame_derecho = tk.Frame(frame_principal, bg=self.color_fondo)
            frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # Label para mostrar el registro
            label_registro = tk.Label(
                frame_derecho, 
                text="Registro de Actividades del Sistema", 
                font=("Arial", 12, "bold"), 
                bg=self.color_fondo,
                fg="#333333"
            )
            label_registro.pack(pady=10)
            
            # Treeview para mostrar registro de actividades
            tree_registro = ttk.Treeview(frame_derecho, columns=("Fecha/Hora", "Usuario", "Accion", "Detalle"), show="headings", height=15)
            tree_registro.heading("Fecha/Hora", text="Fecha/Hora")
            tree_registro.heading("Usuario", text="Usuario")
            tree_registro.heading("Accion", text="Accion")
            tree_registro.heading("Detalle", text="Detalle")
            tree_registro.column("Fecha/Hora", width=130)
            tree_registro.column("Usuario", width=100)
            tree_registro.column("Accion", width=90)
            tree_registro.column("Detalle", width=180)
            tree_registro.pack(fill=tk.BOTH, expand=True)
            
            # Obtener y mostrar el registro global
            registros = obtener_registro_actividades(50)
            
            if registros:
                for reg in registros:
                    fecha_hora = str(reg.get('fecha_hora', ''))[:16]
                    usuario = reg.get('nombre_empleado', 'Sistema') or 'Sistema'
                    accion = reg.get('tipo_accion', '')
                    detalle = reg.get('descripcion', '') or ''
                    tree_registro.insert("", tk.END, values=(fecha_hora, usuario, accion, detalle))
            else:
                tree_registro.insert("", tk.END, values=("", "", "Sin registros", "No hay actividades registradas"))
        
        # Boton volver
        tk.Button(
            self.frame_contenido,
            text="Volver",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            command=self.mostrar_menu_principal,
            cursor="hand2",
            width=12
        ).pack(pady=10)
    
    def mostrar_buscar(self):
        """Muestra formulario de busqueda."""
        self.limpiar_frame()
        
        tk.Label(self.frame_contenido, text="Buscar Empleado", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=(0, 10))
        
        # Campo de busqueda
        tk.Label(self.frame_contenido, text="Ingresa nombre, apellido o email:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_buscar = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_buscar.pack(fill=tk.X, pady=(0, 10))
        
        # Frame para resultados
        frame_resultados = tk.Frame(self.frame_contenido, bg=self.color_fondo)
        frame_resultados.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def action_buscar():
            # Limpiar resultados anteriores
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            
            termino = entry_buscar.get().strip()
            if not termino:
                messagebox.showwarning("Aviso", "Ingresa un termino de busqueda.")
                return
            
            resultados = buscar_empleados(termino)
            
            # Registrar la busqueda
            if self.usuario_logueado:
                nombre = f"{self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}"
                registrar_actividad(self.usuario_logueado['id'], nombre, "buscar_empleado", f"Busco: {termino}")
            
            if not resultados:
                tk.Label(frame_resultados, text="No se encontraron resultados.", bg=self.color_fondo).pack()
            else:
                # Tabla de resultados
                columns = ("ID", "Nombre", "Apellido", "Email")
                tree = ttk.Treeview(frame_resultados, columns=columns, show="headings", height=8)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                
                for emp in resultados:
                    tree.insert("", tk.END, values=(
                        emp["id"],
                        emp["nombre"],
                        emp["apellido"],
                        emp["email"]
                    ))
                
                tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones
        frame_botones = tk.Frame(self.frame_contenido, bg=self.color_fondo)
        frame_botones.pack(pady=10)
        
        tk.Button(
            frame_botones,
            text="Buscar",
            font=("Arial", 11, "bold"),
            bg=self.color_boton,
            fg="white",
            command=action_buscar,
            cursor="hand2",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            command=self.mostrar_menu_principal,
            cursor="hand2",
            width=10
        ).pack(side=tk.LEFT, padx=5)
    
    def mostrar_editar_perfil(self):
        """Muestra formulario para editar el perfil del usuario."""
        self.limpiar_frame()
        
        tk.Label(self.frame_contenido, text="Editar Mi Perfil", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=(0, 15))
        
        # Obtener datos actuales
        nombre_actual = self.usuario_logueado.get("nombre", "")
        apellido_actual = self.usuario_logueado.get("apellido", "")
        telefono_actual = self.usuario_logueado.get("telefono", "") or ""
        puesto_actual = self.usuario_logueado.get("puesto", "") or ""
        
        # Nombre
        tk.Label(self.frame_contenido, text="Nombre:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_nombre = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack(fill=tk.X, pady=(0, 10))
        
        # Apellido
        tk.Label(self.frame_contenido, text="Apellido:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_apellido = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_apellido.insert(0, apellido_actual)
        entry_apellido.pack(fill=tk.X, pady=(0, 10))
        
        # Telefono
        tk.Label(self.frame_contenido, text="Telefono:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_telefono = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_telefono.insert(0, telefono_actual)
        entry_telefono.pack(fill=tk.X, pady=(0, 10))
        
        # Puesto
        tk.Label(self.frame_contenido, text="Puesto:", bg=self.color_fondo).pack(anchor=tk.W)
        entry_puesto = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
        entry_puesto.insert(0, puesto_actual)
        entry_puesto.pack(fill=tk.X, pady=(0, 15))
        
        def action_guardar():
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_apellido = entry_apellido.get().strip()
            nuevo_telefono = entry_telefono.get().strip()
            nuevo_puesto = entry_puesto.get().strip()
            
            if not nuevo_nombre or not nuevo_apellido:
                messagebox.showerror("Error", "Nombre y apellido son obligatorios.")
                return
            
            exito = actualizar_empleado(
                empleado_id=self.usuario_logueado["id"],
                nombre=nuevo_nombre,
                apellido=nuevo_apellido,
                telefono=nuevo_telefono or None,
                puesto=nuevo_puesto or None
            )
            
            if exito:
                messagebox.showinfo("Exito", "Perfil actualizado correctamente.")
                # Actualizar datos locales
                self.usuario_logueado["nombre"] = nuevo_nombre
                self.usuario_logueado["apellido"] = nuevo_apellido
                self.usuario_logueado["telefono"] = nuevo_telefono
                self.usuario_logueado["puesto"] = nuevo_puesto
                self.mostrar_menu_principal()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el perfil.")
        
        # Botones
        frame_botones = tk.Frame(self.frame_contenido, bg=self.color_fondo)
        frame_botones.pack(pady=10)
        
        tk.Button(
            frame_botones,
            text="Guardar",
            font=("Arial", 11, "bold"),
            bg=self.color_boton,
            fg="white",
            command=action_guardar,
            cursor="hand2",
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 11),
            bg="#9E9E9E",
            fg="white",
            command=self.mostrar_menu_principal,
            cursor="hand2",
            width=10
        ).pack(side=tk.LEFT, padx=5)
    
    # ============================================
    # ACCIONES
    # ============================================
    
    def action_login(self):
        """Procesa el inicio de sesion."""
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Email y contrasena son obligatorios.")
            return
        
        exito, mensaje, datos = iniciar_sesion(email, password)
        
        if exito:
            self.usuario_logueado = datos
            # Registrar actividad
            nombre = f"{datos['nombre']} {datos['apellido']}"
            registrar_actividad(datos['id'], nombre, "login", f"Inicio sesion con email: {email}")
            self.mostrar_menu_principal()
        else:
            # Registrar intento fallido
            registrar_actividad(None, None, "login_fallido", f"Intento fallido con email: {email}")
            messagebox.showerror("Error", mensaje)
    
    def action_logout(self):
        """Cierra la sesion."""
        if self.usuario_logueado:
            nombre = f"{self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}"
            registrar_actividad(self.usuario_logueado['id'], nombre, "logout", "Cerro sesion")
        self.usuario_logueado = None
        self.mostrar_login()

    def mostrar_actividades(self):
        """Muestra formulario para agregar actividades."""
        self.limpiar_frame()
        
        tk.Label(self.frame_contenido, text="Gestionar Actividades", font=("Arial", 14, "bold"), bg=self.color_fondo).pack(pady=(0, 15))
        
        # Obtener lista de empleados
        empleados = obtener_empleados()
        
        if not empleados:
            tk.Label(self.frame_contenido, text="No hay empleados registrados.", bg=self.color_fondo).pack(pady=20)
        else:
            # Frame para seleccionar empleado
            tk.Label(self.frame_contenido, text="Seleccionar Empleado:", bg=self.color_fondo).pack(anchor=tk.W)
            
            # Combobox para seleccionar empleado
            empleados_list = [f"{emp['id']} - {emp['nombre']} {emp['apellido']}" for emp in empleados]
            combo_empleado = ttk.Combobox(self.frame_contenido, values=empleados_list, state="readonly", font=("Arial", 11))
            combo_empleado.pack(fill=tk.X, pady=(0, 15))
            combo_empleado.current(0)
            
            # Campos para la actividad
            tk.Label(self.frame_contenido, text="Nombre de Actividad:", bg=self.color_fondo).pack(anchor=tk.W)
            entry_actividad = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
            entry_actividad.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(self.frame_contenido, text="Fecha (YYYY-MM-DD):", bg=self.color_fondo).pack(anchor=tk.W)
            entry_fecha = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
            entry_fecha.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(self.frame_contenido, text="Hora (HH:MM):", bg=self.color_fondo).pack(anchor=tk.W)
            entry_hora = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
            entry_hora.pack(fill=tk.X, pady=(0, 10))
            
            tk.Label(self.frame_contenido, text="Descripcion (opcional):", bg=self.color_fondo).pack(anchor=tk.W)
            entry_descripcion = tk.Entry(self.frame_contenido, font=("Arial", 11), width=30)
            entry_descripcion.pack(fill=tk.X, pady=(0, 15))
            
            # Frame para botones
            frame_botones = tk.Frame(self.frame_contenido, bg=self.color_fondo)
            frame_botones.pack(pady=10)
            
            def action_agregar():
                # Obtener empleado seleccionado
                seleccion = combo_empleado.get()
                if not seleccion:
                    messagebox.showerror("Error", "Selecciona un empleado.")
                    return
                
                empleado_id = int(seleccion.split(" - ")[0])
                nombre_actividad = entry_actividad.get().strip()
                fecha = entry_fecha.get().strip()
                hora = entry_hora.get().strip()
                descripcion = entry_descripcion.get().strip() or None
                
                # Validaciones
                if not nombre_actividad:
                    messagebox.showerror("Error", "Ingresa el nombre de la actividad.")
                    return
                if not fecha:
                    messagebox.showerror("Error", "Ingresa la fecha.")
                    return
                if not hora:
                    messagebox.showerror("Error", "Ingresa la hora.")
                    return
                
                # Agregar hora :00 si no se especifica
                if len(hora.split(":")) == 2:
                    hora = hora + ":00"
                
                # Crear actividad
                nuevo_id = crear_actividad(
                    empleado_id=empleado_id,
                    nombre_actividad=nombre_actividad,
                    fecha=fecha,
                    hora=hora,
                    descripcion=descripcion
                )
                
                if nuevo_id:
                    # Registrar la actividad
                    if self.usuario_logueado:
                        nombre = f"{self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}"
                        detalle = f"Agrego actividad: {nombre_actividad} para empleado ID {empleado_id}"
                        registrar_actividad(self.usuario_logueado['id'], nombre, "agrego_actividad", detalle)
                    messagebox.showinfo("Exito", "Actividad agregada correctamente!")
                    # Limpiar campos
                    entry_actividad.delete(0, tk.END)
                    entry_fecha.delete(0, tk.END)
                    entry_hora.delete(0, tk.END)
                    entry_descripcion.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "No se pudo agregar la actividad.")
            
            # Botones
            tk.Button(
                frame_botones,
                text="Agregar Actividad",
                font=("Arial", 11, "bold"),
                bg=self.color_boton,
                fg="white",
                command=action_agregar,
                cursor="hand2",
                width=15
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                frame_botones,
                text="Volver",
                font=("Arial", 11),
                bg="#9E9E9E",
                fg="white",
                command=self.mostrar_menu_principal,
                cursor="hand2",
                width=12
            ).pack(side=tk.LEFT, padx=5)


def main():
    """Funcion principal."""
    root = tk.Tk()
    app = AplicacionEmpleados(root)
    root.mainloop()


if __name__ == "__main__":
    main()
