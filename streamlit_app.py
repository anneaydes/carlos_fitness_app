"""
carlos_fitness_app- Analizador Inteligente de entrenamiento

Esta aplicación permite a entrenadores y usuarios analizar
datos físicos básicos como edad, peso y estatura para generar:

- Cálculo de IMC
- Recomendación calórica
- Rutina semanal
- Sugerencia de dieta
- Progreso mensual estimado
- Gráfica de evolución del peso

Librerías utilizadas:
- Streamlit (interfaz web)
- Pandas (manejo de datos)
- Matplotlib (visualización)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


st.title("carlos_fitness_app - Analizador Inteligente de Entrenamiento")

st.write("Introduce tus datos para generar un análisis de entrenamiento.")

archivo = "clientes.csv"

if os.path.exists(archivo):
    datos_clientes = pd.read_csv(archivo)
else:
    datos_clientes = pd.DataFrame(columns=["Nombre","Edad","Sexo","Peso","Estatura"])
nombre = st.text_input("Nombre")

edad = st.slider("Edad", 15, 70)

sexo = st.selectbox(
    "Sexo",
    ["Femenino", "Masculino"]
)

peso = st.number_input("Peso (libras)", min_value=80, max_value=400)

estatura = st.number_input("Estatura (pies)", min_value=4.0, max_value=7.0)

if st.button("Registrar cliente"):

    nuevo_cliente = {
        "Nombre": nombre,
        "Edad": edad,
        "Sexo": sexo,
        "Peso": peso,
        "Estatura": estatura
    }

    datos_clientes = pd.concat([datos_clientes, pd.DataFrame([nuevo_cliente])], ignore_index=True)

    datos_clientes.to_csv("clientes.csv", index=False)

    st.success("Cliente registrado correctamente")

if st.button("Generar análisis"):

    estatura_metros = estatura * 0.3048
    peso_kg = peso * 0.453592

    imc = peso_kg / (estatura_metros ** 2)

    st.subheader("Resultado del análisis")

    st.write(f"Nombre: {nombre}")
    st.write(f"Edad: {edad}")
    st.write(f"IMC: {round(imc,2)}")



    if imc < 18.5:
        estado = "Bajo peso"
        recomendacion = "Superávit calórico"
        rutina = "Entrenamiento de fuerza 4 veces por semana"
        dieta = "Aumentar proteínas, arroz, avena, carnes"
        cambio = 1

    elif imc < 25:
        estado = "Peso normal"
        recomendacion = "Mantenimiento calórico"
        rutina = "Entrenamiento mixto fuerza + cardio"
        dieta = "Dieta balanceada con proteínas y vegetales"
        cambio = 0

    else:
        estado = "Sobrepeso"
        recomendacion = "Déficit calórico"
        rutina = "Cardio 4 veces + fuerza 2 veces"
        dieta = "Reducir azúcares y aumentar proteínas"
        cambio = -1


    st.write(f"Estado físico: {estado}")

    st.subheader("Recomendación calórica")
    st.write(recomendacion)

    st.subheader("Rutina sugerida")
    st.write(rutina)

    st.subheader("Dieta sugerida")
    st.write(dieta)



    meses = ["Mes 1","Mes 2","Mes 3","Mes 4","Mes 5","Mes 6"]

    progreso = []

    peso_actual = peso

    for mes in meses:

        peso_actual = peso_actual + cambio

        progreso.append(peso_actual)



    datos = pd.DataFrame({
        "Mes": meses,
        "Peso estimado": progreso
    })



    st.subheader("Progreso estimado del peso")



    color = "pink"

    if sexo == "Masculino":
        color = "blue"



    fig, ax = plt.subplots()

    ax.plot(datos["Mes"], datos["Peso estimado"], marker="o", color=color)

    ax.set_xlabel("Mes")
    ax.set_ylabel("Peso (libras)")
    ax.set_title("Progreso estimado")


    st.pyplot(fig)
    st.subheader("Clientes registrados")
    if os.path.exists("clientes.csv"):

        tabla = pd.read_csv("clientes.csv")

    st.dataframe(tabla)

    cliente_eliminar = st.selectbox(
        "Selecciona el cliente que deseas eliminar",
        tabla["Nombre"]
    )
    if st.button("Eliminar cliente"):

        tabla = tabla[tabla["Nombre"] != cliente_eliminar]

    tabla.to_csv("clientes.csv", index=False)

    st.success("Cliente eliminado correctamente")

if st.button("Ver clientes"):

    if os.path.exists("clientes.csv"):
        tabla = pd.read_csv("clientes.csv")
        st.dataframe(tabla)
    else:
        st.write("No hay clientes registrados aún")



