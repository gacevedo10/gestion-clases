import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB = "clases.db"


def get_db():
    """Abre una conexión a la base de datos."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ── INICIO ───────────────────────────────────────────────
@app.route("/")
def inicio():
    return redirect(url_for("alumnos"))


# ── ALUMNOS ──────────────────────────────────────────────
@app.route("/alumnos")
def alumnos():
    conn = get_db()
    lista = conn.execute("""
        SELECT a.id, a.nombre, a.telefono, a.año_curso,
               c.nombre AS colegio,
               d.nombre AS docente
        FROM alumnos a
        LEFT JOIN colegios c ON a.id_colegio = c.id
        LEFT JOIN docentes d ON a.id_docente = d.id
        ORDER BY a.nombre
    """).fetchall()
    conn.close()
    return render_template("alumnos.html", alumnos=lista)


# ── CLASES ───────────────────────────────────────────────
@app.route("/clases")
def clases():
    conn = get_db()
    lista = conn.execute("""
        SELECT cl.id, cl.fecha, a.nombre AS alumno,
               as_.nombre AS asignatura,
               cl.horas, cl.valor_hora, cl.total
        FROM clases cl
        JOIN alumnos a   ON cl.id_alumno     = a.id
        JOIN asignaturas as_ ON cl.id_asignatura = as_.id
        ORDER BY cl.fecha DESC
    """).fetchall()
    conn.close()
    return render_template("clases.html", clases=lista)


@app.route("/clases/nueva", methods=["GET", "POST"])
def nueva_clase():
    conn = get_db()
    if request.method == "POST":
        conn.execute("""
            INSERT INTO clases (fecha, id_alumno, id_asignatura, horas, valor_hora)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["fecha"],
            request.form["id_alumno"],
            request.form["id_asignatura"],
            request.form["horas"],
            request.form["valor_hora"],
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("clases"))

    alumnos_lista = conn.execute("SELECT id, nombre FROM alumnos ORDER BY nombre").fetchall()
    asignaturas_lista = conn.execute("SELECT id, nombre FROM asignaturas ORDER BY nombre").fetchall()
    conn.close()
    return render_template("nueva_clase.html",
                           alumnos=alumnos_lista,
                           asignaturas=asignaturas_lista)


# ── PAGOS ────────────────────────────────────────────────
@app.route("/pagos")
def pagos():
    conn = get_db()
    lista = conn.execute("""
        SELECT p.id, p.fecha, a.nombre AS alumno, p.monto
        FROM pagos p
        JOIN alumnos a ON p.id_alumno = a.id
        ORDER BY p.fecha DESC
    """).fetchall()
    conn.close()
    return render_template("pagos.html", pagos=lista)


@app.route("/pagos/nuevo", methods=["GET", "POST"])
def nuevo_pago():
    conn = get_db()
    if request.method == "POST":
        conn.execute("""
            INSERT INTO pagos (id_alumno, fecha, monto)
            VALUES (?, ?, ?)
        """, (
            request.form["id_alumno"],
            request.form["fecha"],
            request.form["monto"],
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("pagos"))

    alumnos_lista = conn.execute("SELECT id, nombre FROM alumnos ORDER BY nombre").fetchall()
    conn.close()
    return render_template("nuevo_pago.html", alumnos=alumnos_lista)


# ── DEUDAS ───────────────────────────────────────────────
@app.route("/deudas")
def deudas():
    conn = get_db()
    lista = conn.execute("""
        SELECT a.nombre,
               COALESCE(SUM(cl.total), 0)  AS total_clases,
               COALESCE(SUM(p.monto),  0)  AS total_pagado,
               COALESCE(SUM(cl.total), 0) - COALESCE(SUM(p.monto), 0) AS saldo
        FROM alumnos a
        LEFT JOIN clases cl ON a.id = cl.id_alumno
        LEFT JOIN pagos  p  ON a.id = p.id_alumno
        GROUP BY a.id, a.nombre
        ORDER BY saldo DESC
    """).fetchall()
    conn.close()
    return render_template("deudas.html", deudas=lista)


# ── ARRANQUE ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)