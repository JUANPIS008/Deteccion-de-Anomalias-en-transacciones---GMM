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