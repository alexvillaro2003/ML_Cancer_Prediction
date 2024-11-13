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


    if "bmi" not in st.session_state:
        st.session_state.bmi = 25.0 

    if "mostrar_calculo_bmi" not in st.session_state:
        st.session_state.mostrar_calculo_bmi = False 


    bmi = st.slider("Índice de Masa Corporal (BMI)", min_value=15.0, max_value=40.0, value=st.session_state.bmi, step=0.1)


    if st.button("Calcular BMI", key="bmi_button"):
        st.session_state.mostrar_calculo_bmi = not st.session_state.mostrar_calculo_bmi


    if st.session_state.mostrar_calculo_bmi:
        st.write("Ingrese su altura y peso para calcular el BMI:")
        altura = st.number_input("Altura en metros", min_value=0.5, max_value=2.5, step=0.01, value=1.70, key="altura")
        peso = st.number_input("Peso en kilogramos", min_value=10.0, max_value=300.0, step=0.1, value=70.0, key="peso")
        

        if altura > 0 and peso > 0:
            bmi_calculado = calculo_bmi(altura, peso)
            st.session_state.bmi = bmi_calculado
            st.write(f"Su BMI calculado es: **{bmi_calculado:.2f}**")


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


    if st.button("Predecir"):
        data = np.array([[edad, genero, st.session_state.bmi, fuma, riesgo_0, riesgo_1, riesgo_2, actividad_fisica, consumo_alcohol, historial_cancer]])
        pred = model.predict(data)

        if pred[0] == 1:
            st.error("El modelo predice que el paciente TIENE CÁNCER.")
        else:
            st.success("El modelo predice que el paciente NO TIENE CÁNCER.")



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

            data['st.session_state.bmi'] = False

            return data

        data = extract_data_from_pdf(texto)

        st.write("Datos extraídos del PDF:")
        st.write(data)


        if st.button("Predecir desde PDF"):
            input_data = np.array([[data['age'], data['gender'], data['bmi'], data['smoking'], 
                            data['riesgo_0'], data['riesgo_1'], data['riesgo_2'], 
                            data['alcohol_intake'], data['cancer_history'], data['st.session_state.bmi']]])

            pred = model.predict(input_data)

            if pred[0] == 1:
                st.error("El modelo predice que el paciente TIENE CÁNCER.")
            else:
                st.success("El modelo predice que el paciente NO TIENE CÁNCER.")

