import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import base_datos  # Importamos nuestro archivo de base de datos

# Inicializamos la base de datos al arrancar
base_datos.conectar()

def limpiar_campos():
    entry_id.delete(0, tk.END)
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_anio.delete(0, tk.END)
    entry_editorial.delete(0, tk.END)

def refrescar_tabla():
    # Borra los datos viejos de la pantalla
    for fila in tabla.get_children():
        tabla.delete(fila)
    # Carga los datos nuevos desde la base de datos
    for libro in base_datos.obtener_libros():
        tabla.insert("", tk.END, values=libro)

def registrar():
    if entry_titulo.get() == "" or entry_autor.get() == "":
        messagebox.showwarning("Alerta", "Título y Autor son obligatorios")
        return
    
    base_datos.insertar_libro(
        entry_titulo.get(),
        entry_autor.get(),
        entry_genero.get(),
        float(entry_precio.get()) if entry_precio.get() else 0.0,
        int(entry_anio.get()) 
        if entry_anio.get() else 0,
        entry_editorial.get()
    )
    refrescar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Libro registrado correctamente")

def seleccionar_fila(event):
    # Al hacer clic en un elemento de la tabla, copia los datos a las cajas de texto
    item_seleccionado = tabla.focus()
    if not item_seleccionado:
        return
    valores = tabla.item(item_seleccionado, 'values')
    
    limpiar_campos()
    entry_id.insert(0, valores[0])
    entry_titulo.insert(0, valores[1])
    entry_autor.insert(0, valores[2])
    entry_genero.insert(0, valores[3])
    entry_precio.insert(0, valores[4])
    entry_anio.insert(0, valores[5])
    entry_editorial.insert(0, valores[6])

def modificar():
    if entry_id.get() == "":
        messagebox.showwarning("Alerta", "Selecciona un libro de la tabla primero")
        return
    
    base_datos.actualizar_libro(
        int(entry_id.get()),
        entry_titulo.get(),
        entry_autor.get(),
        entry_genero.get(),
        float(entry_precio.get()) if entry_precio.get() else 0.0,
        int(entry_anio.get()) if entry_anio.get() else 0,
        entry_editorial.get()
    )
    refrescar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Libro actualizado correctamente")

def borrar():
    if entry_id.get() == "":
        messagebox.showwarning("Alerta", "Selecciona un libro de la tabla primero")
        return
    
    base_datos.eliminar_libro(int(entry_id.get()))
    refrescar_tabla()
    limpiar_campos()
    messagebox.showinfo("Éxito", "Libro eliminado correctamente")


# --- CONFIGURACIÓN DE LA VENTANA ---
ventana = tk.Tk()
ventana.title("Gestión de Libros - CRUD")

# Etiquetas y cajas de texto de entrada
tk.Label(ventana, text="ID (Autoincremental):").grid(row=0, column=0, padx=5, pady=5)
entry_id = tk.Entry(ventana)
entry_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(ventana, text="Título (*):").grid(row=1, column=0, padx=5, pady=5)
entry_titulo = tk.Entry(ventana)
entry_titulo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(ventana, text="Autor (*):").grid(row=2, column=0, padx=5, pady=5)
entry_autor = tk.Entry(ventana)
entry_autor.grid(row=2, column=1, padx=5, pady=5)

tk.Label(ventana, text="Género:").grid(row=3, column=0, padx=5, pady=5)
entry_genero = tk.Entry(ventana)
entry_genero.grid(row=3, column=1, padx=5, pady=5)

tk.Label(ventana, text="Precio:").grid(row=4, column=0, padx=5, pady=5)
entry_precio = tk.Entry(ventana)
entry_precio.grid(row=4, column=1, padx=5, pady=5)

tk.Label(ventana, text="Año Publicación:").grid(row=5, column=0, padx=5, pady=5)
entry_anio = tk.Entry(ventana)
entry_anio.grid(row=5, column=1, padx=5, pady=5)

tk.Label(ventana, text="Editorial:").grid(row=6, column=0, padx=5, pady=5)
entry_editorial = tk.Entry(ventana)
entry_editorial.grid(row=6, column=1, padx=5, pady=5)

# Botones de Acción (CRUD)
btn_crear = tk.Button(ventana, text="Agregar Libro", command=registrar)
btn_crear.grid(row=7, column=0, padx=5, pady=5)

btn_actualizar = tk.Button(ventana, text="Modificar Seleccionado", command=modificar)
btn_actualizar.grid(row=7, column=1, padx=5, pady=5)

btn_eliminar = tk.Button(ventana, text="Eliminar Seleccionado", command=borrar)
btn_eliminar.grid(row=7, column=2, padx=5, pady=5)

# Tabla para mostrar el catálogo (Treeview)
columnas = ("id", "titulo", "autor", "genero", "precio", "anio", "editorial")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

# Encabezados de la tabla
tabla.heading("id", text="ID")
tabla.heading("titulo", text="Título")
tabla.heading("autor", text="Autor")
tabla.heading("genero", text="Género")
tabla.heading("precio", text="Precio")
tabla.heading("anio", text="Año")
tabla.heading("editorial", text="Editorial")

# Ajuste de tamaño de columnas
for col in columnas:
    tabla.column(col, width=100)

tabla.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# Detectar cuándo se hace clic en una fila para rellenar los campos
tabla.bind("<ButtonRelease-1>", seleccionar_fila)

# Cargar los datos iniciales en la interfaz gráfica
refrescar_tabla()

# Iniciar la ventana
ventana.mainloop()