import sqlite3

def conectar():
    # Conecta a la base de datos (se crea sola si no existe)
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    # Crea la tabla con los campos mínimos obligatorios del PDF
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT,
            precio REAL,
            año INTEGER,
            editorial TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def insertar_libro(titulo, autor, genero, precio, año, editorial):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO libros (titulo, autor, genero, precio, año, editorial)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (titulo, autor, genero, precio, año, editorial))
    conexion.commit()
    conexion.close()

def obtener_libros():
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM libros")
    lista = cursor.fetchall()
    conexion.close()
    return lista

def actualizar_libro(id_libro, titulo, autor, genero, precio, año, editorial):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE libros 
        SET titulo=?, autor=?, genero=?, precio=?, año=?, editorial=? 
        WHERE id=?
    """, (titulo, autor, genero, precio, año, editorial, id_libro))
    conexion.commit()
    conexion.close()

def eliminar_libro(id_libro):
    conexion = sqlite3.connect("biblioteca.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=?", (id_libro,))
    conexion.commit()
    conexion.close()