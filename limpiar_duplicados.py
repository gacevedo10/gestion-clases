import sqlite3

conn = sqlite3.connect("clases.db")
cursor = conn.cursor()

# ── VER duplicados antes de borrar ───────────────────────
print("Alumnos duplicados encontrados:")
print("-" * 40)
duplicados = cursor.execute("""
    SELECT nombre, COUNT(*) as cantidad
    FROM alumnos
    GROUP BY nombre
    HAVING COUNT(*) > 1
""").fetchall()

if not duplicados:
    print("No hay duplicados. Todo está bien.")
else:
    for nombre, cantidad in duplicados:
        print(f"  {nombre} → {cantidad} veces")

    print()
    confirmar = input("¿Querés eliminar los duplicados? (s/n): ")

    if confirmar.lower() == "s":
        # Elimina duplicados conservando el registro con el ID más bajo
        cursor.execute("""
            DELETE FROM alumnos
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM alumnos
                GROUP BY nombre
            )
        """)
        conn.commit()
        print(f"✅ Duplicados eliminados. Quedaron {cursor.execute('SELECT COUNT(*) FROM alumnos').fetchone()[0]} alumnos.")
    else:
        print("Operación cancelada, no se modificó nada.")

conn.close()