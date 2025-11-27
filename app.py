import streamlit as st
import sqlite3
import pandas as pd

# -------------------------------
# AUTENTICACIÓN SENCILLA
# -------------------------------
def check_login():
    st.sidebar.title("Login")

    user = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if user == "husarph1" and password == "SpaceGh0st":
        return True
    else:
        st.sidebar.info("Use admin credentials para editar")
        return False


# -------------------------------
# CONEXIÓN A LA BD
# -------------------------------
def get_connection():
    return sqlite3.connect("empresa.db", check_same_thread=False)


def load_table(table):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def save_table(table, df):
    conn = get_connection()
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()


# -------------------------------
# APP
# -------------------------------
st.title("Base de Datos de la Empresa")

login_ok = check_login()

buscar = st.text_input("Buscar")

# -------------------------------
# TABLA TRABAJADORES
# -------------------------------
st.subheader("Tabla: Trabajadores")

df = load_table("trabajadores")

if buscar:
    df = df[df.apply(lambda row: row.astype(str).str.contains(buscar, case=False).any(), axis=1)]

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
)

if login_ok:
    if st.button("Guardar Cambios (Trabajadores)"):
        save_table("trabajadores", edited_df)
        st.success("Guardado correctamente.")


# -------------------------------
# TABLA DEPARTAMENTO
# -------------------------------
st.subheader("Tabla: Departamentos")

df_dep = load_table("departamento")[["ID", "Nombre"]]

edited_dep = st.data_editor(
    df_dep,
    use_container_width=True,
    num_rows="dynamic",
)

if login_ok:
    if st.button("Guardar Cambios (Departamentos)"):
        save_table("departamento", edited_dep)
        st.success("Guardado correctamente.")
