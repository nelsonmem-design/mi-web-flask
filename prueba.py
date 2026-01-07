from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def conectar_db():
    return sqlite3.connect("mensajes.db")

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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                correo TEXT,
                mensaje TEXT
            )
        """)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            mensaje TEXT
        )
    """)

    cursor.execute("SELECT * FROM mensajes")
    mensajes = cursor.fetchall()
    conexion.close()

    return render_template("admin.html", mensajes=mensajes)

if __name__ == "__main__":
    app.run(debug=True)

