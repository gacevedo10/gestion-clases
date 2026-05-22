import sqlite3
from datetime import date

conn = sqlite3.connect("clases.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# ── COLEGIOS ─────────────────────────────────────────────
# Reemplazá con los nombres reales de los colegios
colegios = [
    "Instituto 25 de Mayo",
    "ITAPU",
]

for nombre in colegios:
    cursor.execute(
        "INSERT OR IGNORE INTO colegios (nombre) VALUES (?)", (nombre,)
    )

# ── DOCENTES ─────────────────────────────────────────────
# Agregá las docentes con las que tenés contacto
# Si no tenés el teléfono, podés poner None
docentes = [
    ("Romina Delfini", "3584195535"),
    ("Laura Vignoli", "None"),
    ("Gisela Dogliani", "3534295692"),
    # Agregá más filas si necesitás
]

for nombre, telefono in docentes:
    cursor.execute(
        "INSERT OR IGNORE INTO docentes (nombre, telefono) VALUES (?, ?)",
        (nombre, telefono)
    )

conn.commit()

# ── ALUMNOS ──────────────────────────────────────────────
# Primero obtenemos los IDs de colegios y docentes que acabamos de insertar
# para poder referenciarlos correctamente

def id_colegio(nombre):
    r = cursor.execute("SELECT id FROM colegios WHERE nombre = ?", (nombre,)).fetchone()
    return r[0] if r else None

def id_docente(nombre):
    r = cursor.execute("SELECT id FROM docentes WHERE nombre = ?", (nombre,)).fetchone()
    return r[0] if r else None

# Formato de cada alumno:
# (nombre, telefono, año_curso, nombre_colegio, nombre_docente)
# Si no sabés el docente de un alumno, poné None en nombre_docente
alumnos = [
    ("Thiago Flores", "3585147629", "5° año", "Instituto 25 de Mayo", "Romina Delfini"),
    ("Amanda Fernández", "3535692010", "3° año", "ITAPU", None),
    ("Thiago González", "3584253689", "4° año", "ITAPU", "Laura Vignoli"),
    ("Delfina", "3562436547", "3° año", "ITAPU", None),
    ("Triana", "3584820381", "5° año", "Instituto 25 de Mayo", "Romina Delfini"),
    # Agregá más filas si necesitás
]

for nombre, telefono, año, colegio, docente in alumnos:
    cursor.execute(
        """INSERT INTO alumnos (nombre, telefono, año_curso, id_colegio, id_docente)
           VALUES (?, ?, ?, ?, ?)""",
        (nombre, telefono, año, id_colegio(colegio), id_docente(docente))
    )

conn.commit()
conn.close()

print("✅ Datos cargados correctamente.")
print(f"   → {len(colegios)} colegios")
print(f"   → {len(docentes)} docentes")
print(f"   → {len(alumnos)} alumnos")