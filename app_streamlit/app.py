import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('../models/DecissionTree_RandomSearchCV/model_DTCRSCV.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

st.title("Predicción de Cáncer")

st.markdown("""
Esta aplicación permite ingresar información del paciente para predecir si tiene cáncer o no. 
Por favor, ingrese los valores requeridos:
""")

age = st.number_input("Edad (20-80 años)", min_value=20, max_value=80, value=30)
gender = st.selectbox("Género", options={0: "Masculino", 1: "Femenino"}, format_func=lambda x: {0: "Masculino", 1: "Femenino"}[x])
bmi = st.slider("Índice de Masa Corporal (BMI)", min_value=15.0, max_value=40.0, value=25.0, step=0.1)
smoking = st.radio("¿Fuma?", options={0: "No", 1: "Sí"}, format_func=lambda x: {0: "No", 1: "Sí"}[x])

genetic_risk = st.selectbox("Riesgo Genético", options={0: "Bajo", 1: "Medio", 2: "Alto"}, format_func=lambda x: {0: "Bajo", 1: "Medio", 2: "Alto"}[x])
riesgo_0 = int(genetic_risk == 0)
riesgo_1 = int(genetic_risk == 1)
riesgo_2 = int(genetic_risk == 2)

physical_activity = st.slider("Horas de Actividad Física por Semana", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
alcohol_intake = st.slider("Consumo de Alcohol por Semana (unidades)", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
cancer_history = st.radio("¿Historial Personal de Cáncer?", options={0: "No", 1: "Sí"}, format_func=lambda x: {0: "No", 1: "Sí"}[x])

if st.button("Predecir"):

    input_data = np.array([[age, gender, bmi, smoking, riesgo_0, riesgo_1, riesgo_2, physical_activity, alcohol_intake, cancer_history]])
    prediction = model.predict(input_data)


    if prediction[0] == 1:
        st.error("El modelo predice que el paciente **TIENE CÁNCER**.")
    else:
        st.success("El modelo predice que el paciente **NO TIENE CÁNCER**.")