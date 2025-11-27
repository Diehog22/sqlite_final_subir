import streamlit as st
import sqlite3
import pandas as pd

st.title("Base de Datos de la Empresa")

def get_conn():
    return sqlite3.connect("empresa.db")

conn = get_conn()

# --------------------------
# CARGAR TABLAS
# --------------------------
def load_table(name):
    return pd.read_sql_query(f"SELECT * FROM {name}", conn)

def save_table(df, table_name):
    c = conn.cursor()
    c.execute(f"DELETE FROM {table_name}")  # limpiar tabla
    conn.commit()

    # guardar de nuevo fila por fila
    if table_name == "departamentos":
        for _, row in df.iterrows():
            c.execute("""
                INSERT INTO departamentos(id, nombre, director, email, ubicacion)
                VALUES (?,?,?,?,?)
            """, (row["id"], row["nombre"], row["director"], row["email"], row["ubicacion"]))
    
    if table_name == "trabajadores":
        for _, row in df.iterrows():
            c.execute("""
                INSERT INTO trabajadores(id, nombre, departamento_id, salario, correo)
                VALUES (?,?,?,?,?)
            """, (row["id"], row["nombre"], row["departamento_id"], row["salario"], row["correo"]))
    
    conn.commit()

# --------------------------
# MENÚ LATERAL
# --------------------------
tab = st.sidebar.selectbox("Seleccionar tabla", ["Trabajadores", "Departamentos"])
search = st.text_input("Buscar")

df = load_table(tab.lower())

# FILTRO
if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

# MOSTRAR TABLA
st.subheader(f"Tabla: {tab}")
edited_df = st.experimental_data_editor(df, use_container_width=True)

# --------------------------
# LOGIN ADMIN
# --------------------------
st.subheader("Administrador (solo para editar BD)")

user = st.text_input("Usuario")
pwd = st.text_input("Contraseña", type="password")

if user == "husarph1" and pwd == "SpaceGh0st":
    st.success("Acceso concedido — modo edición activado")

    # Guardar cambios hechos con data editor
    if st.button("💾 Guardar cambios en la base de datos"):
        save_table(edited_df, tab.lower())
        st.success("Cambios guardados correctamente en SQLite")

    # --------------------------
    # AÑADIR NUEVO DEPARTAMENTO
    # --------------------------
    if tab == "Departamentos":
        st.write("---")
        st.write("### Añadir nuevo departamento")
        n = st.text_input("Nombre")
        d = st.text_input("Director")
        e = st.text_input("Email")
        u = st.text_input("Ubicación")

        if st.button("Agregar departamento"):
            c = conn.cursor()
            c.execute("""
                INSERT INTO departamentos(nombre, director, email, ubicacion)
                VALUES (?,?,?,?)
            """, (n, d, e, u))
            conn.commit()
            st.success("Departamento agregado")

    # --------------------------
    # AÑADIR NUEVO TRABAJADOR
    # --------------------------
    if tab == "Trabajadores":
        st.write("---")
        st.write("### Añadir nuevo trabajador")
        n = st.text_input("Nombre trabajador")
        depts = load_table("departamentos")
        dep = st.selectbox("Departamento", depts["id"])
        s = st.number_input("Salario", min_value=0)
        crr = st.text_input("Correo")

        if st.button("Agregar trabajador"):
            c = conn.cursor()
            c.execute("""
                INSERT INTO trabajadores(nombre, departamento_id, salario, correo)
                VALUES (?,?,?,?)
            """, (n, dep, s, crr))
            conn.commit()
            st.success("Trabajador agregado")

conn.close()
