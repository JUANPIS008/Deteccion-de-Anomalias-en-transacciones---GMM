import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime


# Configuración de página
st.set_page_config(
    page_title="Detector de Fraude - GMM",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# Título principal
st.title("Detector de Anomalías en Transacciones")
st.markdown(
    """
    Sistema inteligente basado en **Gaussian Mixture Models (GMM)** para detectar
    transacciones financieras sospechosas mediante análisis de anomalías.
    """
)

# Carga de modelos
@st.cache_resource
def cargar_modelos():
    modelo = joblib.load("models/modelo_gmm.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return modelo, scaler

try:
    gmm_model, escalador = cargar_modelos()
    st.success("Modelos cargados correctamente.")

except FileNotFoundError as e:
    st.error(f"No se encontró el archivo: {e}")
    st.info(
        "Asegúrate de que los archivos "
        "`modelo_gmm.pkl` y `scaler.pkl` "
        "estén dentro de la carpeta `models/`."
    )
    st.stop()


# Columnas esperadas
FEATURE_COLS = [
    "Time",
    "Amount",
    "Merchant Category Code (MCC)",
    "Transaction Response Code"
]

# Sidebar
st.sidebar.header("Configuración del Umbral")

umbral_manual = st.sidebar.number_input(
    "Umbral de log-score",
    value=-16.46,
    min_value=-100.0,
    max_value=0.0,
    step=0.01,
    format="%.4f",
    help=(
        "Scores por debajo de este valor se clasifican como fraude.\n\n"
        "• -16.88 → Conservador\n"
        "• -16.46 → Equilibrado\n"
        "• -16.10 → Agresivo"
    ),
)

st.sidebar.markdown("---")

st.sidebar.info(
    "El modelo fue entrenado únicamente con "
    "transacciones normales. "
    "Un log-score muy bajo indica comportamiento anómalo."
)


# Formulario
st.subheader("Datos de la Transacción")

with st.form("formulario_prediccion"):

    col1, col2 = st.columns(2)

    #  Columna 1 
    with col1:

        transaction_amount = st.number_input(
            "Monto",
            min_value=0.0,
            max_value=100000.0,
            value=150.0,
            step=0.01,
            format="%.2f",
            help="Monto de la transacción."
        )

        mcc = st.selectbox(
            "Merchant Category Code (MCC)",
            options=[5411, 5812, 5999, 4111],
            format_func=lambda x: {
                5411: "5411 - Supermercados",
                5812: "5812 - Restaurantes",
                5999: "5999 - Retail",
                4111: "4111 - Transporte"
            }[x]
        )

    # Columna 2
    with col2:

        transaction_datetime = st.datetime_input(
            "Fecha y hora",
            value=datetime.now(),
            help="Fecha y hora de la transacción."
        )

        response_code = st.selectbox(
            "Código de respuesta",
            options=[0, 1, 2],
            format_func=lambda x: {
                0: "0 - Aprobada",
                1: "1 - Rechazada",
                2: "2 - Error"
            }[x]
        )

    submitted = st.form_submit_button(
        "Analizar Transacción",
        use_container_width=True
    )


# Predicción
if submitted:

    try:

        # Conversión del tiempo
        timestamp = int(
            pd.Timestamp(transaction_datetime).timestamp()
        )

        # Datos para escalado
        datos_escalar = pd.DataFrame([{
            "Amount": transaction_amount,
            "Time": timestamp
        }])

        # Reordenar columnas según el scaler
        datos_escalar = datos_escalar[
            escalador.feature_names_in_
        ]

        # Escalar valores
        scaled_values = escalador.transform(datos_escalar)

        # Convertir a DataFrame
        scaled_df = pd.DataFrame(
            scaled_values,
            columns=escalador.feature_names_in_
        )

        # Obtener valores escalados
        time_scaled = scaled_df["Time"].iloc[0]
        amount_scaled = scaled_df["Amount"].iloc[0]
            

        # Vector de entrada
        X_input = pd.DataFrame([{
            "Time": time_scaled,
            "Amount": amount_scaled,
            "Merchant Category Code (MCC)": mcc,
            "Transaction Response Code": response_code
        }])

        # Score
        log_score = gmm_model.score_samples(X_input)[0]

        # Nivel de riesgo
        if log_score < -25:
            riesgo = "ALTO"

        elif log_score < -18:
            riesgo = "MEDIO"

        else:
            riesgo = "BAJO"

        # Resultados
        st.markdown("---")
        st.subheader("Resultado del Análisis")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric(
                "Log-score",
                f"{log_score:.4f}"
            )
            st.caption(
                "Mientras más bajo sea el valor, "
                "más anómala es la transacción."
            )

        with col_r2:
            st.metric(
                "Umbral",
                f"{umbral_manual:.4f}"
            )

        with col_r3:
            st.metric(
                "Nivel de Riesgo",
                riesgo
            )

        # Barra visual
        score_visual = min(max((log_score + 40) / 40, 0), 1)

        st.write("### Riesgo estimado")
        st.progress(score_visual)

        # Clasificación        # ─────────────────────────
        if log_score < umbral_manual:

            st.error(
                "FRAUDE DETECTADO — "
                "La transacción presenta un comportamiento anómalo."
            )

        else:

            st.success(
                "TRANSACCIÓN NORMAL — "
                "No se detectaron anomalías relevantes."
            )

        # Información técnica
        with st.expander("Ver datos enviados al modelo"):

            st.dataframe(
                X_input.T.rename(
                    columns={0: "Valor"}
                )
            )

    except Exception as e:

        st.error(f"Error durante la predicción: {e}")

# Footer
st.markdown("---")

st.caption(
    "Sistema de detección de anomalías financieras "
    "basado en Gaussian Mixture Models (GMM)."
)