import sqlite3

# Crea (o conecta a) la base de datos en el mismo directorio
conn = sqlite3.connect("clases.db")
cursor = conn.cursor()

# Activar claves foráneas en SQLite
cursor.execute("PRAGMA foreign_keys = ON")

# ── Tabla: colegios ──────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS colegios (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
""")

# ── Tabla: docentes ──────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS docentes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre   TEXT NOT NULL,
    telefono TEXT
)
""")

# ── Tabla: alumnos ───────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS alumnos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL,
    telefono    TEXT,
    año_curso   TEXT,
    id_colegio  INTEGER REFERENCES colegios(id),
    id_docente  INTEGER REFERENCES docentes(id)
)
""")

# ── Tabla: asignaturas ───────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS asignaturas (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
)
""")

# ── Tabla: clases ────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS clases (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha         DATE NOT NULL,
    id_alumno     INTEGER NOT NULL REFERENCES alumnos(id),
    id_asignatura INTEGER NOT NULL REFERENCES asignaturas(id),
    horas         REAL NOT NULL,
    valor_hora    REAL NOT NULL,
    total         REAL GENERATED ALWAYS AS (horas * valor_hora) STORED
)
""")

# ── Tabla: pagos ─────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS pagos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_alumno INTEGER NOT NULL REFERENCES alumnos(id),
    fecha     DATE NOT NULL,
    monto     REAL NOT NULL
)
""")

# Cargar asignaturas iniciales
asignaturas = ["Matemática", "Física", "Química", "Programación"]
for a in asignaturas:
    cursor.execute(
        "INSERT OR IGNORE INTO asignaturas (nombre) VALUES (?)", (a,)
    )

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente: clases.db")