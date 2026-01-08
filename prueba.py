from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# =========================
# Base de datos
# =========================
def conectar_db():
    return sqlite3.connect("mensajes.db")

def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            mensaje TEXT
        )
    """)
    conexion.commit()
    conexion.close()

# Inicializar la base al arrancar
inicializar_db()

# =========================
# Rutas
# =========================
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO mensajes (nombre, correo, mensaje) VALUES (?, ?, ?)",
            (nombre, correo, mensaje)
        )
        conexion.commit()
        conexion.close()

    return render_template("contacto.html")

@app.route("/admin")
def admin():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM mensajes ORDER BY id DESC")
    mensajes = cursor.fetchall()
    conexion.close()

    return render_template("admin.html", mensajes=mensajes)

# =========================
# Arranque
# =========================
if __name__ == "__main__":
    app.run(debug=True)
