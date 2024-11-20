import os
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import pdfplumber
import re
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

def load_model():

    with open('../models/XGBoost_RandomizedSearchCV/model_XGBRSCV.pkl', 'rb') as file:
        model = pickle.load(file)
    return model



def calculo_bmi(altura, peso):

    bmi = peso / (altura ** 2)
    return bmi


def generar_expediente_pdf(edad, genero, bmi, fuma, riesgo_0, riesgo_1, riesgo_2, actividad_fisica, consumo_alcohol, historial_cancer, prob):
    # Crear objeto FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Configurar fuente
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Expediente Médico - Predicción de Cáncer", ln=True, align='C')
    pdf.ln(10)

    # Datos del paciente
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Edad: {edad} años", ln=True)
    pdf.cell(200, 10, txt=f"Género: {'Masculino' if genero == 0 else 'Femenino'}", ln=True)
    pdf.cell(200, 10, txt=f"Índice de Masa Corporal (BMI): {bmi:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Fuma: {'Sí' if fuma == 1 else 'No'}", ln=True)
    pdf.cell(200, 10, txt=f"Riesgo Genético: {'Bajo' if riesgo_0 == 1 else 'Medio' if riesgo_1 == 1 else 'Alto'}", ln=True)
    pdf.cell(200, 10, txt=f"Actividad Física: {actividad_fisica} horas/semana", ln=True)
    pdf.cell(200, 10, txt=f"Consumo de Alcohol: {consumo_alcohol} unidades/semana", ln=True)
    pdf.cell(200, 10, txt=f"Historial de Cáncer: {'Sí' if historial_cancer == 1 else 'No'}", ln=True)

    pdf.ln(10)

    # Verificar que prob no sea None antes de usarlo
    if prob is not None and len(prob) > 0 and len(prob[0]) > 1:
        if prob[0][1] > prob[0][0]:
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt="El modelo predice que el paciente TIENE CÁNCER.", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Probabilidad estimada: {prob[0][1] * 100:.2f}%", ln=True)
        else:
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(200, 10, txt="El modelo predice que el paciente NO TIENE CÁNCER.", ln=True, align='L')
            pdf.cell(200, 10, txt=f"Probabilidad estimada: {prob[0][0] * 100:.2f}%", ln=True)
    else:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="No se pudo obtener la predicción del cáncer.", ln=True)

    # Generar el gráfico de probabilidades
    categories = ['No Cáncer', 'Cáncer']
    probabilities = [prob[0][0], prob[0][1]]

    # Crear el gráfico pie
    fig, ax = plt.subplots()
    ax.pie(probabilities, labels=categories, autopct='%1.1f%%', colors=['green', 'red'], startangle=90, wedgeprops={'edgecolor': 'black'})

    # Configurar el título
    ax.set_title('Probabilidad de tener o no tener Cáncer')

    # Guardar el gráfico como imagen temporal
    img_path = "grafico_probabilidad_pie.png"
    fig.savefig(img_path, format='png')

    # Cerrar la figura para liberar memoria
    plt.close(fig)

    # Añadir la imagen al PDF
    pdf.ln(10)  # Dejar espacio antes de la imagen
    pdf.image(img_path, x=10, y=pdf.get_y(), w=180)  # Insertar la imagen en el PDF

    # Eliminar la imagen temporal
    os.remove(img_path)

    # Guardar el archivo en una ruta temporal
    pdf_output_path = "expediente_medico.pdf"
    pdf.output(pdf_output_path)

    # Retornar la ruta del archivo generado
    return pdf_output_path





