from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
# =========================
# Conexión PostgreSQL
# =========================
def conectar_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            correo TEXT,
            mensaje TEXT
        )
    """)
    conexion.commit()
    conexion.close()

# Crear tabla al arrancar la app
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
            "INSERT INTO mensajes (nombre, correo, mensaje) VALUES (%s, %s, %s)",
            (nombre, correo, mensaje)
        )
        conexion.commit()
        conexion.close()

        flash("Mensaje enviado con éxito ✅", "success")
        return redirect(url_for("contacto"))

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
# Arranque local
# =========================
if __name__ == "__main__":
    app.run(debug=True)
