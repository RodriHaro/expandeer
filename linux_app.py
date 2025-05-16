import json
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, END, filedialog
import keyboard
import os
import time
import pyperclip  # Para manejar el portapapeles
from datetime import datetime  # Para variables de fecha/hora
import sys

# Archivo JSON para guardar atajos
FILE_NAME = "atajos.json"
CONFIG_FILE = "config.json"

# Configuración por defecto
DEFAULT_CONFIG = {
    "iniciar_con_windows": False,
    "mostrar_notificaciones": True
}

# Cargar configuración
def cargar_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    else:
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG

# Guardar configuración
def guardar_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

# Configurar inicio con el sistema (Linux)
def configurar_inicio_sistema(habilitar=True):
    # Esta es una versión simplificada para Linux
    # En un sistema Linux real, se debería crear un archivo .desktop en ~/.config/autostart/
    print("Nota: La función de inicio automático no está implementada para Linux")
    return False

# Cargar atajos desde JSON
def cargar_atajos():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

# Guardar atajos al JSON
def guardar_atajos(atajos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(atajos, f, indent=4, ensure_ascii=False)

# Procesar variables dinámicas en el texto
def procesar_variables(texto):
    ahora = datetime.now()
    
    # Reemplazar variables de fecha/hora
    variables = {
        "{{date}}": ahora.strftime("%d/%m/%Y"),
        "{{time}}": ahora.strftime("%H:%M"),
        "{{datetime}}": ahora.strftime("%d/%m/%Y %H:%M"),
        "{{year}}": ahora.strftime("%Y"),
        "{{month}}": ahora.strftime("%m"),
        "{{day}}": ahora.strftime("%d"),
        "{{hour}}": ahora.strftime("%H"),
        "{{minute}}": ahora.strftime("%M")
    }
    
    for var, valor in variables.items():
        texto = texto.replace(var, valor)
    
    return texto

# Clase principal de la app
class ExpansubiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpanSubi (Linux)")
        self.atajos = cargar_atajos()
        self.config = cargar_config()
        self.buffer = ""
        self.max_buffer_length = 30  # Longitud máxima del buffer
        self.clipboard_original = ""  # Para guardar el contenido original del portapapeles
        
        # Configurar estilo moderno
        self.configurar_estilo()
        
        # Crear marco principal
        main_frame = tk.Frame(root, bg="#f5f5f5")
        main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Crear menú
        self.crear_menu()
        
        # Etiqueta de instrucciones
        tk.Label(main_frame, text="Atajos de texto disponibles:", font=("Helvetica", 11), bg="#f5f5f5", fg="#333333").pack(anchor=tk.W, pady=(0, 5))
        
        # Frame para la lista y barra de desplazamiento
        list_frame = tk.Frame(main_frame, bg="#f5f5f5")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Barra de desplazamiento
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista de atajos
        self.listbox = Listbox(list_frame, width=50, height=15, font=("Helvetica", 10),
                              yscrollcommand=scrollbar.set, bg="white", 
                              selectbackground="#4a86e8", selectforeground="white")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Estilo de botones
        button_style = {"font": ("Helvetica", 10), "bg": "#4a86e8", "fg": "white", 
                      "activebackground": "#3a76d8", "activeforeground": "white",
                      "relief": tk.FLAT, "padx": 15, "pady": 5, "width": 8}
        
        # Botones de gestión de atajos
        tk.Button(button_frame, text="Agregar", command=self.agregar, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Editar", command=self.editar, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Eliminar", command=self.eliminar, **button_style).pack(side=tk.LEFT, padx=5)
        
        # Frame para botones de importación/exportación
        imp_exp_frame = tk.Frame(main_frame, bg="#f5f5f5")
        imp_exp_frame.pack(fill=tk.X, pady=5)
        
        # Botones de importación y exportación
        tk.Button(imp_exp_frame, text="Importar", command=self.importar_atajos, **button_style).pack(side=tk.LEFT, padx=5)
        tk.Button(imp_exp_frame, text="Exportar", command=self.exportar_atajos, **button_style).pack(side=tk.LEFT, padx=5)
        
        # Estado de la aplicación
        self.estado_var = tk.StringVar(value="Estado: Monitoreando")
        self.estado_label = tk.Label(main_frame, textvariable=self.estado_var, 
                                   font=("Helvetica", 10), bg="#f5f5f5", fg="#555555")
        self.estado_label.pack(pady=10)
        
        # Checkbox para activar/desactivar
        self.activado = tk.BooleanVar(value=True)
        self.check = tk.Checkbutton(main_frame, text="Activo", variable=self.activado, 
                                  command=self.toggle_activado, font=("Helvetica", 10),
                                  bg="#f5f5f5", activebackground="#f5f5f5")
        self.check.pack(pady=5)
        
        # Etiqueta de ayuda
        ayuda_text = "Variables disponibles: {{date}}, {{time}}, {{datetime}}, {{year}}, {{month}}, {{day}}"
        tk.Label(main_frame, text=ayuda_text, font=("Helvetica", 8), bg="#f5f5f5", fg="#777777").pack(pady=5)
        
        # Etiqueta de versión Linux
        linux_text = "Versión Linux - Algunas funciones pueden estar limitadas"
        tk.Label(main_frame, text=linux_text, font=("Helvetica", 8), bg="#f5f5f5", fg="#ff6600").pack(pady=5)

        self.actualizar_lista()
        self.iniciar_escucha()
        
        # Asegurar que los atajos se desactiven cuando se cierre la app
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def crear_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Importar atajos", command=self.importar_atajos)
        file_menu.add_command(label="Exportar atajos", command=self.exportar_atajos)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.on_closing)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Configuración
        config_menu = tk.Menu(menu_bar, tearoff=0)
        
        # Variable para mostrar notificaciones
        self.mostrar_notif_var = tk.BooleanVar(value=self.config.get("mostrar_notificaciones", True))
        config_menu.add_checkbutton(label="Mostrar notificaciones", 
                                  variable=self.mostrar_notif_var,
                                  command=self.guardar_configuracion)
        
        menu_bar.add_cascade(label="Configuración", menu=config_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def guardar_configuracion(self):
        self.config["mostrar_notificaciones"] = self.mostrar_notif_var.get()
        guardar_config(self.config)
    
    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de ExpanSubi", 
                          "ExpanSubi v1.0 (Linux Edition)\n\n" +
                          "Un expansor de texto creado para gestionar reembolsos\n" +
                          "Desarrollado con Python\n\n" +
                          "© 2025 - Todos los derechos reservados")
    
    def importar_atajos(self):
        try:
            archivo = filedialog.askopenfilename(
                title="Importar atajos",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            
            if not archivo:
                return
                
            with open(archivo, "r", encoding="utf-8") as f:
                nuevos_atajos = json.load(f)
            
            # Preguntar cómo manejar los atajos existentes
            if self.atajos:
                respuesta = messagebox.askyesno(
                    "Conflicto potencial", 
                    "¿Desea reemplazar los atajos existentes con los nuevos? \n\n" +
                    "Sí = Reemplazar todo\n" +
                    "No = Combinar (los nuevos prevalecerán en caso de conflicto)"
                )
                
                if respuesta:
                    # Reemplazar completamente
                    self.atajos = nuevos_atajos
                else:
                    # Combinar, con preferencia a los nuevos
                    for atajo, texto in nuevos_atajos.items():
                        self.atajos[atajo] = texto
            else:
                # No hay atajos existentes, simplemente usar los nuevos
                self.atajos = nuevos_atajos
            
            guardar_atajos(self.atajos)
            self.actualizar_lista()
            
            if self.config.get("mostrar_notificaciones", True):
                messagebox.showinfo("Importación exitosa", 
                                   f"Se importaron {len(nuevos_atajos)} atajos correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error al importar", 
                                f"No se pudieron importar los atajos: {str(e)}")
    
    def exportar_atajos(self):
        try:
            archivo = filedialog.asksaveasfilename(
                title="Exportar atajos",
                defaultextension=".json",
                filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
            )
            
            if not archivo:
                return
                
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(self.atajos, f, indent=4, ensure_ascii=False)
            
            if self.config.get("mostrar_notificaciones", True):    
                messagebox.showinfo("Exportación exitosa", 
                                   f"Se exportaron {len(self.atajos)} atajos correctamente.")
        
        except Exception as e:
            messagebox.showerror("Error al exportar", 
                                f"No se pudieron exportar los atajos: {str(e)}")

    def toggle_activado(self):
        if self.activado.get():
            self.iniciar_escucha()
            self.estado_var.set("Estado: Monitoreando")
        else:
            self.detener_escucha()
            self.estado_var.set("Estado: Detenido")

    def on_closing(self):
        self.detener_escucha()
        self.root.destroy()
        
    def actualizar_lista(self):
        self.listbox.delete(0, END)
        for atajo, texto in self.atajos.items():
            # Truncar texto largo para mostrar
            texto_display = texto[:50] + "..." if len(texto) > 50 else texto
            self.listbox.insert(END, f"{atajo} → {texto_display}")

    def agregar(self):
        atajo = simpledialog.askstring("Nuevo atajo", "Escribí el atajo (ej: :firma):")
        if not atajo:
            return
            
        # Mostrar una ventana más grande para el texto
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Texto para atajo: {atajo}")
        dialog.geometry("500x300")
        
        tk.Label(dialog, text="Texto que reemplazará el atajo:").pack(pady=5)
        
        texto_entry = tk.Text(dialog, width=60, height=10)
        texto_entry.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Variables frame con ejemplos
        var_frame = tk.Frame(dialog)
        var_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(var_frame, text="Variables disponibles:", font=("Arial", 8)).pack(side=tk.LEFT)
        tk.Label(var_frame, text="{{date}}, {{time}}, {{datetime}}, {{year}}", font=("Arial", 8)).pack(side=tk.LEFT, padx=5)
        
        def guardar():
            texto = texto_entry.get("1.0", tk.END).strip()
            if texto:
                self.atajos[atajo] = texto
                guardar_atajos(self.atajos)
                self.actualizar_lista()
                
                if self.config.get("mostrar_notificaciones", True):
                    messagebox.showinfo("Atajo agregado", f"Atajo '{atajo}' guardado correctamente.")
                    
                dialog.destroy()
        
        tk.Button(dialog, text="Guardar", command=guardar).pack(pady=10)

    def editar(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
            
        clave = list(self.atajos.keys())[seleccion[0]]
        texto_actual = self.atajos[clave]
        
        # Mostrar una ventana más grande para editar
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar atajo: {clave}")
        dialog.geometry("500x300")
        
        tk.Label(dialog, text=f"Editar texto para el atajo '{clave}':").pack(pady=5)
        
        texto_entry = tk.Text(dialog, width=60, height=10)
        texto_entry.insert("1.0", texto_actual)
        texto_entry.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Variables frame con ejemplos
        var_frame = tk.Frame(dialog)
        var_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(var_frame, text="Variables disponibles:", font=("Arial", 8)).pack(side=tk.LEFT)
        tk.Label(var_frame, text="{{date}}, {{time}}, {{datetime}}, {{year}}", font=("Arial", 8)).pack(side=tk.LEFT, padx=5)
        
        def guardar_edicion():
            nuevo_texto = texto_entry.get("1.0", tk.END).strip()
            if nuevo_texto:
                self.atajos[clave] = nuevo_texto
                guardar_atajos(self.atajos)
                self.actualizar_lista()
                
                if self.config.get("mostrar_notificaciones", True):
                    messagebox.showinfo("Atajo editado", f"Atajo '{clave}' actualizado correctamente.")
                    
                dialog.destroy()
        
        tk.Button(dialog, text="Guardar", command=guardar_edicion).pack(pady=10)

    def eliminar(self):
        seleccion = self.listbox.curselection()
        if seleccion:
            clave = list(self.atajos.keys())[seleccion[0]]
            confirmacion = messagebox.askyesno("Confirmar eliminación", 
                                             f"¿Estás seguro de que deseas eliminar el atajo '{clave}'?")
            if confirmacion:
                del self.atajos[clave]
                guardar_atajos(self.atajos)
                self.actualizar_lista()
                
                if self.config.get("mostrar_notificaciones", True):
                    messagebox.showinfo("Atajo eliminado", f"Atajo '{clave}' eliminado correctamente.")
    
    def detener_escucha(self):
        try:
            # Dejar de escuchar todas las teclas
            keyboard.unhook_all()
            self.estado_var.set("Estado: Detenido")
        except Exception as e:
            print(f"Error al detener la escucha: {e}")

    def procesar_tecla(self, event):
        if not self.activado.get():
            return
            
        # Detectar Ctrl+Z (para deshacer)
        if event.name == 'z' and keyboard.is_pressed('ctrl'):
            # Simplemente ignoramos Ctrl+Z para evitar interferir con la funcionalidad nativa
            return
            
        try:
            # Si es la tecla Backspace, eliminar el último carácter del buffer
            if event.name == 'backspace' and self.buffer:
                self.buffer = self.buffer[:-1]
                return
            
            # Si no es un caracter imprimible, ignorar
            if len(event.name) != 1 and event.name not in ['space', 'enter']:
                return
            
            # Agregar la tecla al buffer
            if event.name == 'space':
                self.buffer += ' '
            elif event.name == 'enter':
                self.buffer += '\n'
            else:
                self.buffer += event.name
            
            # Limitar tamaño del buffer
            if len(self.buffer) > self.max_buffer_length:
                self.buffer = self.buffer[-self.max_buffer_length:]
            
            # Verificar si hay algún atajo en el buffer
            for atajo, reemplazo in self.atajos.items():
                if self.buffer.endswith(atajo):  # El atajo sin necesidad de espacio
                    # Procesar variables dinámicas
                    texto_procesado = procesar_variables(reemplazo)
                    
                    # Actualizar estado
                    self.estado_var.set(f"Activado: {atajo}")
                    self.root.update_idletasks()

                    try:
                        # Desactivar temporalmente para evitar recursión
                        temp = self.activado.get()
                        self.activado.set(False)
                        
                        # Guardar el contenido original del portapapeles
                        self.clipboard_original = pyperclip.paste()
                        
                        # Copiar el texto de reemplazo al portapapeles
                        pyperclip.copy(texto_procesado)
                        
                        # Enviar backspace para eliminar solo el atajo
                        for _ in range(len(atajo)):
                            keyboard.send('backspace')
                        
                        # Pegar el reemplazo (instantáneo) - en Linux puede ser diferente
                        if os.name == 'nt':  # Windows
                            keyboard.send('ctrl+v')
                        else:  # Linux/Mac
                            keyboard.send('ctrl+v')  # La mayoría de aplicaciones Linux usan Ctrl+V
                        
                        # Pequeña pausa antes de restaurar el portapapeles
                        time.sleep(0.05)
                        
                        # Restaurar el portapapeles original
                        pyperclip.copy(self.clipboard_original)
                        
                        # Reactivar la escucha
                        self.activado.set(temp)
                    except Exception as e:
                        print(f"Error al reemplazar: {e}")
                        self.activado.set(True)
                        # Intentar restaurar el portapapeles
                        try:
                            pyperclip.copy(self.clipboard_original)
                        except:
                            pass
                    
                    # Reiniciar el buffer
                    self.buffer = ""
                    
                    # Actualizar estado
                    self.estado_var.set("Estado: Monitoreando")
                    break
        
        except Exception as e:
            print(f"Error al procesar tecla: {e}")

    def iniciar_escucha(self):
        try:
            self.detener_escucha()
            self.buffer = ""
            
            # Registrar solo un listener para todas las teclas
            keyboard.on_press(self.procesar_tecla)
            
            self.estado_var.set("Estado: Monitoreando")
            print("Escucha de teclado iniciada")
        except Exception as e:
            print(f"Error al iniciar la escucha: {e}")
            self.estado_var.set(f"Error: {e}")

    def configurar_estilo(self):
        # Configurar estilo general de la ventana
        self.root.configure(bg="#f5f5f5")
        self.root.option_add("*Font", "Helvetica 10")
        self.root.option_add("*Background", "#f5f5f5")
        self.root.option_add("*Foreground", "#333333")

# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x550")  # Tamaño inicial de la ventana un poco más grande
    
    # No intentar cargar el ícono en Linux
    app = ExpansubiApp(root)
    root.mainloop()