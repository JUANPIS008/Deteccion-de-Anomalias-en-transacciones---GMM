import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Detector de Fraude - GMM", layout="centered", initial_sidebar_state="collapsed")

st.title("Detector de anomalias en transacciones")
st.markdown("Ingresa los datos de la transacción para predecir si es **normal** o **sospechosa**.")

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
    st.info("Asegúrate de que `modelo_gmm.pkl` y `scaler.pkl` estén en la carpeta `models/`.")
    st.stop()

FEATURE_COLS = list(gmm_model.feature_names_in_)

# ── Sidebar ──
st.sidebar.header("Configuración del umbral")
umbral_manual = st.sidebar.number_input(
    "Umbral de log-score",
    value=-16.46,
    min_value=-100.0,
    max_value=0.0,
    step=0.01,
    format="%.4f",
    help=(
        "Scores por debajo de este valor se clasifican como fraude.\n\n"
        "Rango calibrado con tus datos:\n"
        "• -16.88 → conservador (menos alertas)\n"
        "• -16.46 → equilibrado (percentil 5%)\n"
        "• -16.10 → agresivo (más alertas)"
    ),
)
st.sidebar.markdown("---")
st.sidebar.info(
    "El modelo GMM fue entrenado **solo con transacciones normales**. "
    "Un log-score muy bajo indica comportamiento anómalo."
)


# ── Formulario ──
st.subheader("Datos de la transacción")

with st.form("formulario_prediccion"):

    col1, col2 = st.columns(2)

    with col1:
        transaction_amount = st.number_input(
            "Monto",
            min_value=0.0,
            value=150.0,
            step=0.01,
            format="%.2f",
            help="Monto en moneda original. Se normalizará automáticamente con el scaler.",
        )
        mcc = st.number_input(
            "Merchant Category Code (MCC)",
            min_value=0,
            value=5411,
            step=1,
            help="Codigo de categoría del comercio. Ej: 5411 = Supermercados, 5812 = Restaurantes.",
        )

    with col2:
        transaction_datetime = st.text_input(
            "Fecha y hora de la transacción",
            value="2024-01-15 14:30:00",
            help="Formato: YYYY-MM-DD HH:MM:SS.",
        )
        response_code = st.number_input(
            "Codigo de respuesta",
            min_value=0,
            value=0,
            step=1,
            help="Codigo de respuesta del procesador. Ej: 0 = Aprobada, 1 = Rechazada, 2 = Error.",
        )

    submitted = st.form_submit_button("Predecir", use_container_width=True)

# ── Predicción ──
if submitted:
    try:
        timestamp = pd.to_datetime(transaction_datetime).timestamp()

        amount_time_scaled = escalador.transform([[transaction_amount, timestamp]])
        amount_scaled = amount_time_scaled[0, 0]  
        time_scaled   = amount_time_scaled[0, 1]   

        X_input = pd.DataFrame([{
            "Time":                          time_scaled,
            "Amount":                        amount_scaled,
            "Merchant Category Code (MCC)":  mcc,
            "Transaction Response Code":     response_code,
        }])[FEATURE_COLS]

        log_score = gmm_model.score_samples(X_input)[0]

        st.markdown("---")
        st.subheader("Resultado de la predicción")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Log-score de densidad", f"{log_score:.4f}")
            st.caption("Cuanto más bajo, más anomala es la transacción.")
        with col_r2:
            st.metric("Umbral configurado", f"{umbral_manual:.4f}")
        with col_r3:
            diferencia = log_score - umbral_manual
            st.metric("Diferencia vs umbral", f"{diferencia:.4f}")
            st.caption("Negativo = por debajo del umbral.")

        if log_score < umbral_manual:
            st.error("FRAUDE DETECTADO — La transacción es sospechosa.")
        else:
            st.success("TRANSACCION NORMAL — No se detectaron anomalías.")

        with st.expander("Ver vector enviado al modelo"):
            st.dataframe(X_input.T.rename(columns={0: "Valor escalado"}))

    except Exception as e:
        st.error(f"Error durante la predicción: {e}")