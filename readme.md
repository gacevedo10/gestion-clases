# 📚 Sistema de Gestión de Clases Particulares
 
Aplicación web desarrollada en Python y Flask para gestionar clases particulares de nivel secundario.
 
Permite registrar alumnos, clases dictadas, pagos recibidos y consultar el saldo pendiente de cada alumno, reemplazando el uso de una hoja de cálculo manual.
 
---
 
## ✨ Funcionalidades
 
- **Alumnos** — registro de alumnos con datos de contacto, colegio, año y docente de referencia
- **Clases** — registro de cada clase con fecha, asignatura, horas y valor por hora
- **Pagos** — registro de pagos recibidos por alumno
- **Deudas** — vista de saldo pendiente por alumno, calculado automáticamente
---
 
## 🛠️ Tecnologías utilizadas
 
- Python 3
- Flask
- SQLite
- HTML / CSS (Jinja2 templates)
---
 
## ⚙️ Instalación y uso
 
**1. Clonar el repositorio**
```bash
git clone https://github.com/gacevedo10/gestion-clases.git
cd gestion-clases
```
 
**2. Instalar dependencias**
```bash
pip install flask
```
 
**3. Crear la base de datos**
```bash
python crear_base.py
```
 
**4. Ejecutar la aplicación**
```bash
python app.py
```
 
**5. Abrir en el navegador**
```
http://127.0.0.1:5000
```
 
---
 
## 📁 Estructura del proyecto
 
```
gestion-clases/
├── app.py              # Servidor Flask y rutas
├── crear_base.py       # Script de creación de la base de datos
├── cargar_datos.py     # Script de carga inicial de datos
└── templates/
    ├── base.html       # Template base con navegación
    ├── alumnos.html    # Lista de alumnos
    ├── clases.html     # Lista de clases
    ├── nueva_clase.html# Formulario nueva clase
    ├── pagos.html      # Lista de pagos
    ├── nuevo_pago.html # Formulario nuevo pago
    └── deudas.html     # Saldo por alumno
```
 
---
 
## 📌 Notas
 
- La base de datos `clases.db` no se incluye en el repositorio por contener datos personales.
- Al clonar el proyecto, ejecutar `crear_base.py` genera una base de datos nueva y vacía lista para usar.
---
 
## 👤 Autor
 
**Gonzalo Acevedo**  
GitHub: [@gacevedo10](https://github.com/gacevedo10)