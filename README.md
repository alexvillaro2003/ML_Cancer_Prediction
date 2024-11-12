# 🩺 Cancer Prediction Model 🔍

Este proyecto utiliza machine learning para predecir si una persona podría sufrir cáncer. Aprovechando datos de factores personales y de salud, este modelo busca ofrecer una herramienta preliminar de evaluación de riesgo que puede ser útil para clínicas o para uso personal.

## 📌 Objetivo del Proyecto

El objetivo principal es desarrollar un modelo que permita predecir el riesgo de cáncer basándose en factores como:

- Edad
- Género
- Índice de Masa Corporal (BMI)
- Hábitos de Fumar
- Actividad Física
- Consumo de Alcohol
- Antecedentes Genéticos
- Antecedentes Personales de Cáncer

Esta herramienta puede ayudar a:

- Identificar riesgos individuales en base a datos personales.
- Ofrecer una evaluación preliminar que motive una consulta profesional si es necesario.

## 📂 Dataset

El dataset utilizado se encuentra en Kaggle: [Cancer Prediction Dataset](https://www.kaggle.com/datasets/rabieelkharoua/cancer-prediction-dataset), y también en la ruta del repositorio: data/raw/The_Cancer_data_1500_V2.csv

Contiene información sobre factores que pueden contribuir al riesgo de cáncer, siendo variables no invasivas y accesibles para análisis iniciales.

## 🚀 Enfoque y Metodología

1. **Exploración de Datos**: Análisis de distribuciones y relaciones para identificar patrones de riesgo.
2. **Preprocesamiento**: Limpieza y transformación de datos para optimizar el rendimiento del modelo.
3. **Entrenamiento de Modelo**: Se utiliza un clasificador de árbol de decisión junto a técnicas de búsqueda de hiperparámetros (RandomizedSearchCV).
4. **Evaluación**: El modelo es evaluado utilizando métricas de precisión, sensibilidad, y matriz de confusión.

## ✨ Resultados y Beneficios Esperados

- **Evaluación Preliminar de Riesgo**: Permitir a los usuarios tener una noción sobre el riesgo de cáncer en base a factores personales.
- **Soporte en la Toma de Decisiones**: Facilitar que los usuarios consideren realizar exámenes médicos o ajustes de estilo de vida según los resultados.

## 🛠️ Herramientas Utilizadas

- **Lenguaje**: Python
- **Librerías**: `pandas v2.2.3`, `numpy v2.1.1`, `seaborn v0.13.2`, `scikit-learn v1.5.2`, `streamlit v1.40.1`, `pyYAML v6.0.2`
- **Interfaz de Usuario**: La aplicación ha sido implementada en Streamlit para facilitar el uso del modelo.

## 🤖 Ejecutar el Proyecto

Para iniciar la aplicación en Streamlit:

```bash
streamlit run app/app.py

```

## 📄 Licencia

Este proyecto es de uso abierto bajo la licencia MIT.
