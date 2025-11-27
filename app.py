
import streamlit as st
import sqlite3
import pandas as pd

st.title("Base de Datos de la Empresa")

def get_conn():
    return sqlite3.connect("empresa.db")

op = st.sidebar.selectbox("Ver tabla", ["Trabajadores","Departamentos"])
search = st.text_input("Buscar")

conn = get_conn()

def load(name):
    df = pd.read_sql_query(f"SELECT * FROM {name}", conn)
    if search:
        df = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    return df

if op=="Trabajadores":
    st.header("Trabajadores (con ID Departamento)")
    st.dataframe(load("trabajadores"))
else:
    st.header("Departamentos")
    st.dataframe(load("departamentos"))

st.subheader("Administrador")
user = st.text_input("Usuario")
pwd = st.text_input("Contraseña", type="password")

if user=="husarph1" and pwd=="SpaceGh0st":
    st.success("Acceso concedido")

    st.write("### Añadir trabajador")
    nombre = st.text_input("Nombre del trabajador")
    deps = pd.read_sql_query("SELECT id, nombre FROM departamentos", conn)
    dep = st.selectbox("ID Departamento", deps["id"])
    salario = st.number_input("Salario", min_value=0)
    correo = st.text_input("Correo electrónico")

    if st.button("Guardar"):
        cur = conn.cursor()
        cur.execute("INSERT INTO trabajadores(nombre,departamento_id,salario,correo) VALUES (?,?,?,?)",
                    (nombre,dep,salario,correo))
        conn.commit()
        st.success("Trabajador añadido correctamente")

conn.close()
