from utils import *

model = load_model()

st.title("Predicción de Cáncer")

# Menú
tabs = st.tabs(["Predicción Manual", "Predicción desde PDF"])

# Predicción Manual
with tabs[0]:
    st.markdown("""
    Esta aplicación permite ingresar información del paciente para predecir si tiene cáncer o no. 
    Por favor, ingrese los valores requeridos:
    """)

    edad = st.number_input("Edad (20-80 años)", min_value=20, max_value=80, value=30)

    genero = st.selectbox("Género", options=["Masculino", "Femenino"])
    genero = 0 if genero == "Masculino" else 1  # type: ignore

    if "mostrar_calculo_bmi" not in st.session_state:
        st.session_state.mostrar_calculo_bmi = False

    if "bmi" not in st.session_state or not isinstance(st.session_state.bmi, float):
        st.session_state.bmi = 25.0  # Valor predeterminado válido

    bmi = st.slider(
        "Índice de Masa Corporal (BMI)",
        min_value=15.0,
        max_value=40.0,
        value=float(st.session_state.bmi) if isinstance(st.session_state.bmi, float) else 25.0,
        step=0.1
    )

    if st.button("Calcular BMI", key="bmi_button"):
        st.session_state.mostrar_calculo_bmi = not st.session_state.mostrar_calculo_bmi

    if st.session_state.mostrar_calculo_bmi:
        st.write("Ingrese su altura y peso para calcular el BMI:")
        altura = st.number_input("Altura en metros", min_value=0.5, max_value=2.5, step=0.01, value=1.70, key="altura")
        peso = st.number_input("Peso en kilogramos", min_value=10.0, max_value=300.0, step=0.1, value=70.0, key="peso")

        if altura > 0 and peso > 0:
            bmi_calculado = calculo_bmi(altura, peso)
            if isinstance(bmi_calculado, float):
                st.session_state.bmi = bmi_calculado
                st.write(f"Su BMI calculado es: **{bmi_calculado:.2f}**")
            else:
                st.warning("El cálculo del BMI no generó un valor válido.")


    fuma = st.radio("¿Fuma?", options=["No", "Sí"])
    fuma = 0 if fuma == "No" else 1  # type: ignore


    riesgo_genetico = st.selectbox("Riesgo Genético", options=["Bajo", "Medio", "Alto"])
    riesgo_0 = 1 if riesgo_genetico == "Bajo" else 0
    riesgo_1 = 1 if riesgo_genetico == "Medio" else 0
    riesgo_2 = 1 if riesgo_genetico == "Alto" else 0

    actividad_fisica = st.slider("Horas de Actividad Física por Semana", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    consumo_alcohol = st.slider("Consumo de Alcohol por Semana (unidades)", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
    historial_cancer = st.radio("¿Historial Personal de Cáncer?", options=["No", "Sí"])
    historial_cancer = 0 if historial_cancer == "No" else 1 # type: ignore


    # Prediccion Manual
    if st.button("Predecir"):
        data = np.array([[edad, genero, st.session_state.bmi, fuma, riesgo_0, riesgo_1, riesgo_2, actividad_fisica, consumo_alcohol, historial_cancer]])
        pred = model.predict(data)
        prob = model.predict_proba(data)


        if pred[0] == 1:
            st.error("El modelo predice que el paciente TIENE CÁNCER.")
            st.write(f"**Probabilidad estimada:** {prob[0][1] * 100:.2f}%")
        else:
            st.success("El modelo predice que el paciente NO TIENE CÁNCER.")
            st.write(f"**Probabilidad estimada:** {prob[0][0] * 100:.2f}%")

        st.session_state.prediccion_realizada = True


    # Botón para generar el PDF
    if "prediccion_realizada" in st.session_state and st.session_state.prediccion_realizada:

        data = np.array([[edad, genero, st.session_state.bmi, fuma, riesgo_0, riesgo_1, riesgo_2, actividad_fisica, consumo_alcohol, historial_cancer]])
        pred = model.predict(data)
        prob = model.predict_proba(data)

        pdf_data = generar_expediente_pdf(edad, genero, st.session_state.bmi, fuma, 
                                        riesgo_0, riesgo_1, riesgo_2, actividad_fisica, 
                                        consumo_alcohol, historial_cancer, prob)

        st.download_button(
            label="Descargar Expediente",
            data=open(pdf_data, "rb").read(),
            file_name="expediente_medico.pdf",
            mime="application/pdf",
            key="download_button_manual"
        )            



# Predicción desde PDF
with tabs[1]:
    st.markdown("""
    Carga un archivo PDF con tus datos médicos para obtener una predicción automática.
    """)

    archivo = st.file_uploader("Sube tu archivo PDF", type="pdf")

    if archivo is not None:

        with pdfplumber.open(archivo) as pdf:
            texto = ""
            for page in pdf.pages:
                texto += page.extract_text()


        st.write("Texto extraído del PDF:")
        st.text_area("Texto extraído", texto, height=300)


        def extract_data_from_pdf(texto):
            data = {}


            if "Hombre" in texto:
                data['gender'] = 0
            elif "Mujer" in texto:
                data['gender'] = 1


            if "No fumador" in texto:
                data['smoking'] = 0
            elif "fumador" in texto:
                data['smoking'] = 1


            age_search = re.search(r"(\d+) años", texto)
            if age_search:
                data['age'] = int(age_search.group(1))


            if "bebedor 2 copas ocasionalmente" in texto:
                data['alcohol_intake'] = 0.5


            data['riesgo_genetico'] = 'Bajo'

            if data['riesgo_genetico'] == 'Bajo':
                data['riesgo_0'] = 1
                data['riesgo_1'] = 0
                data['riesgo_2'] = 0
            elif data['riesgo_genetico'] == 'Medio':
                data['riesgo_0'] = 0
                data['riesgo_1'] = 1
                data['riesgo_2'] = 0
            else:
                data['riesgo_0'] = 0
                data['riesgo_1'] = 0
                data['riesgo_2'] = 1

            data['cancer_history'] = 0


            bmi_search = re.search(r"IMC: (\d+\.\d+)", texto)
            if bmi_search:
                data['bmi'] = float(bmi_search.group(1))

            else:
                data['bmi'] = 25.0

            return data

        data = extract_data_from_pdf(texto)

        st.write("Datos extraídos del PDF:")
        st.write(data)


        if st.button("Predecir desde PDF"):
            input_data = np.array([[data['age'], data['gender'], data['bmi'], data['smoking'],2,
                        data['alcohol_intake'], data['cancer_history'],
                        data['riesgo_0'], data['riesgo_1'], data['riesgo_2']]])


            pred = model.predict(input_data)
            prob = model.predict_proba(input_data)

            if pred[0] == 1:
                st.error("El modelo predice que el paciente TIENE CÁNCER.")
                st.write(f"**Probabilidad estimada:** {prob[0][1] * 100}%")
            else:
                st.success("El modelo predice que el paciente NO TIENE CÁNCER.")
                st.write(f"**Probabilidad estimada:** {prob[0][0] * 100}%")

        
        # Botón para generar el PDF
        st.session_state.prediccion_realizada_2 = True


        # Botón para generar el PDF
        if "prediccion_realizada_2" in st.session_state and st.session_state.prediccion_realizada_2:

            input_data = np.array([[data['age'], data['gender'], data['bmi'], data['smoking'],2,
                        data['alcohol_intake'], data['cancer_history'],
                        data['riesgo_0'], data['riesgo_1'], data['riesgo_2']]])

            
            pred = model.predict(input_data)
            prob = model.predict_proba(input_data)
                            

            actividad_fisica = 2.0
            st.session_state.bmi = False

            pdf_data = generar_expediente_pdf(data['age'], data['gender'], data['bmi'], data['smoking'], 
                                            data['riesgo_0'], data['riesgo_1'], data['riesgo_2'], actividad_fisica, 
                                            data['alcohol_intake'], historial_cancer, prob)

            st.download_button(
                label="Descargar Expediente",
                data=open(pdf_data, "rb").read(),
                file_name="expediente_medico.pdf",
                mime="application/pdf",
                key="download_button_pdf"
            )            



# Pie de página
st.markdown("---")

st.markdown("### Información Adicional")

# Desplegable 1: Modelo predictivo y métricas
with st.expander("Modelo Predictivo y Métricas"):
    st.write("""
    Este modelo de predicción de cáncer está basado en un algoritmo de aprendizaje automático entrenado con datos médicos.
    A continuación, se presentan las métricas clave del modelo:
    """)
    st.write("- **Precisión (Accuracy):** 0.936000")
    st.write("- **Sensibilidad (Recall):** 0.894366")
    st.write("- **Precisión (Precision):** 0.933824")
    st.write("""
    Estas métricas reflejan el rendimiento del modelo en un conjunto de datos de prueba.
    """)

# Desplegable 2: Descripción del modelo
with st.expander("Descripción del Modelo"):
    st.write("""
    el modelo XGBoost entrenado con los parámetros ajustados muestra un buen desempeño 
    general, con un alto recall, lo cual es clave para problemas en los que la identificación
    precisa de las instancias positivas es crucial. Este modelo combina una alta precisión con
    una buena capacidad de generalización, lo que lo hace adecuado para clasificación en conjuntos 
    de datos desbalanceados y complejos.
    """)
    st.write("""
    Este sistema no reemplaza una consulta médica, sino que es una herramienta complementaria para ayudar
    en la evaluación de riesgos.
    """)

# Desplegable 3: Quiénes somos
with st.expander("Quiénes Somos"):
    st.write("""
    © Alejandro Villarreal Rodríguez.
    """)
    st.write("""
    Si tienes dudas o sugerencias, no dudes en contactarme.
    """)
