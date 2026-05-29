import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

st.set_page_config(
    page_title="Detector de Fraude",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0b0f19;
    color: #c9d1d9;
}
.block-container { padding: 2.5rem 2.5rem; max-width: 860px; }
h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; color: #e6edf3; }

.page-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.18em; text-transform: uppercase;
    background: #161b27; border: 1px solid #21334a; color: #58a6ff;
    padding: 4px 12px; border-radius: 2px; display: inline-block; margin-bottom: 1rem;
}
.page-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.8rem; font-weight: 600; color: #e6edf3; margin-bottom: 0.4rem;
}
.page-sub { font-size: 0.9rem; color: #6e7681; margin-bottom: 1.8rem; line-height: 1.7; }
.divider { border: none; border-top: 1px solid #1e2d40; margin: 1.8rem 0; }

.section-title {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #58a6ff; border-left: 3px solid #58a6ff;
    padding-left: 10px; margin-bottom: 1rem;
}

.result-card-fraud {
    background: #1a0f0f; border: 1px solid #f0883e55;
    border-left: 4px solid #f0883e;
    border-radius: 0 8px 8px 0; padding: 1.4rem 1.6rem; margin-top: 1.2rem;
}
.result-card-normal {
    background: #0d1a0f; border: 1px solid #3fb95055;
    border-left: 4px solid #3fb950;
    border-radius: 0 8px 8px 0; padding: 1.4rem 1.6rem; margin-top: 1.2rem;
}
.result-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.4rem;
}
.result-label.fraud { color: #f0883e; }
.result-label.normal { color: #3fb950; }
.result-title {
    font-family: 'IBM Plex Mono', monospace; font-size: 1.2rem;
    font-weight: 600; color: #e6edf3; margin-bottom: 0.5rem;
}
.result-desc { font-size: 0.85rem; color: #8b949e; line-height: 1.65; }

.score-box {
    background: #111827; border: 1px solid #1e2d40;
    border-radius: 6px; padding: 1.1rem 1.3rem; text-align: center;
}
.score-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.15em; text-transform: uppercase; color: #58a6ff; margin-bottom: 0.3rem;
}
.score-value {
    font-family: 'IBM Plex Mono', monospace; font-size: 1.6rem;
    font-weight: 600; color: #e6edf3;
}
.score-sub { font-size: 0.72rem; color: #6e7681; margin-top: 0.2rem; }

.risk-high  { color: #f0883e; }
.risk-med   { color: #d29922; }
.risk-low   { color: #3fb950; }

.info-note {
    background: #111827; border: 1px solid #1e2d40;
    border-radius: 6px; padding: 1rem 1.2rem;
    font-size: 0.82rem; color: #6e7681; line-height: 1.65;
}

.stSelectbox label, .stNumberInput label, .stDateInput label, .stTimeInput label {
    color: #8b949e !important; font-size: 0.85rem;
}

footer { display: none; }
</style>
""", unsafe_allow_html=True)

# Carga de modelos
@st.cache_resource
def cargar_modelos():
    modelo = joblib.load("models/modelo_gmm.pkl")
    scaler = joblib.load("models/scaler.pkl")
    return modelo, scaler

try:
    gmm_model, escalador = cargar_modelos()
except FileNotFoundError as e:
    st.error(f"No se encontro el archivo: {e}")
    st.info("Asegurate de que modelo_gmm.pkl y scaler.pkl esten en la carpeta models/")
    st.stop()

FEATURE_COLS = list(gmm_model.feature_names_in_)

# Sidebar
st.sidebar.markdown("### Configuracion del Detector")
umbral_manual = st.sidebar.number_input(
    "Umbral de log-score",
    value=-16.46,
    min_value=-100.0,
    max_value=0.0,
    step=0.01,
    format="%.4f",
    help=(
        "Define la sensibilidad del detector.\n\n"
        "Scores por debajo de este valor se clasifican como fraude.\n\n"
        "Rango calibrado con el dataset actual:\n"
        "  -16.88  Conservador — menos alertas\n"
        "  -16.46  Equilibrado — percentil 5%\n"
        "  -16.10  Agresivo    — mas alertas"
    ),
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Variables del modelo**")
for col in FEATURE_COLS:
    st.sidebar.code(col, language=None)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.78rem; color:#6e7681; line-height:1.65;">
El modelo GMM fue entrenado exclusivamente con transacciones clasificadas como normales.
Calcula la densidad de probabilidad logaritmica de cada nueva transaccion bajo esa
distribucion aprendida. Un score muy bajo indica que la transaccion es estadisticamente
improbable dentro del comportamiento normal.
</div>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="page-tag">Modulo de Prediccion</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Analisis de Transaccion</div>', unsafe_allow_html=True)
st.markdown("""
<p class="page-sub">
Ingresa los datos de una transaccion financiera para determinar si su comportamiento
es consistente con el patron normal aprendido por el modelo, o si presenta
caracteristicas estadisticamente anomalas que sugieren actividad fraudulenta.
</p>
""", unsafe_allow_html=True)

# Formulario
st.markdown('<div class="section-title">Datos de la Transaccion</div>', unsafe_allow_html=True)

with st.form("form_prediccion"):

    col1, col2 = st.columns(2, gap="large")

    with col1:
        transaction_amount = st.number_input(
            "Monto de la transaccion",
            min_value=0.0,
            max_value=100000.0,
            value=150.0,
            step=0.01,
            format="%.2f",
            help="Valor monetario de la transaccion en la moneda original del registro."
        )

        mcc = st.selectbox(
            "Merchant Category Code (MCC)",
            options=[5411, 5812, 5999, 4111, 6011, 7995, 6051],
            format_func=lambda x: {
                5411: "5411 — Supermercados",
                5812: "5812 — Restaurantes",
                5999: "5999 — Retail general",
                4111: "4111 — Transporte",
                6011: "6011 — Cajeros automaticos (ATM)",
                7995: "7995 — Casinos y apuestas",
                6051: "6051 — Casas de cambio",
            }[x],
            help=(
                "Codigo numerico que identifica la categoria del comercio donde "
                "se realizo la transaccion, segun el estandar ISO 18245."
            )
        )

    with col2:
        fecha = st.date_input(
            "Fecha de la transaccion",
            value=datetime.now().date(),
            help="Fecha en que se realizo la transaccion."
        )

        hora = st.time_input(
            "Hora de la transaccion",
            value=datetime.now().time(),
            help="Hora exacta de la transaccion en formato 24h."
        )

        response_code = st.selectbox(
            "Codigo de respuesta del procesador",
            options=list(range(13)),
            format_func=lambda x: {
                0:  "0  — Aprobada",
                1:  "1  — Rechazada por fondos insuficientes",
                2:  "2  — Error del sistema",
                3:  "3  — Transaccion no permitida",
                4:  "4  — Tarjeta vencida",
                5:  "5  — Rechazada por banco emisor",
                6:  "6  — Error de comunicacion",
                7:  "7  — Fraude confirmado por banco",
                8:  "8  — Limite de credito excedido",
                9:  "9  — PIN incorrecto",
                10: "10 — Tarjeta reportada como robada",
                11: "11 — Cuenta bloqueada",
                12: "12 — Transaccion duplicada",
            }[x],
            help=(
                "Codigo devuelto por el procesador de pagos al momento de la transaccion. "
                "Los codigos distintos de 0 indican alguna condicion de error o rechazo."
            )
        )

    submitted = st.form_submit_button(
        "Analizar Transaccion",
        use_container_width=True
    )

# Prediccion
if submitted:
    try:
        transaction_datetime = datetime.combine(fecha, hora)
        timestamp = int(pd.Timestamp(transaction_datetime).timestamp())

        datos_escalar = pd.DataFrame([{
            "Amount": transaction_amount,
            "Time":   timestamp
        }])[escalador.feature_names_in_]

        scaled_values = escalador.transform(datos_escalar)
        scaled_df = pd.DataFrame(scaled_values, columns=escalador.feature_names_in_)

        time_scaled   = scaled_df["Time"].iloc[0]
        amount_scaled = scaled_df["Amount"].iloc[0]

        X_input = pd.DataFrame([{
            "Time":                          time_scaled,
            "Amount":                        amount_scaled,
            "Merchant Category Code (MCC)":  mcc,
            "Transaction Response Code":     response_code,
        }])[FEATURE_COLS]

        log_score = gmm_model.score_samples(X_input)[0]
        diferencia = log_score - umbral_manual

        if log_score < -25:
            riesgo = "ALTO"
            riesgo_class = "risk-high"
        elif log_score < umbral_manual:
            riesgo = "MEDIO"
            riesgo_class = "risk-med"
        else:
            riesgo = "BAJO"
            riesgo_class = "risk-low"

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Resultado del Analisis</div>', unsafe_allow_html=True)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-label">Log-score GMM</div>
                <div class="score-value">{log_score:.4f}</div>
                <div class="score-sub">Densidad logaritmica bajo el modelo</div>
            </div>
            """, unsafe_allow_html=True)

        with sc2:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-label">Umbral configurado</div>
                <div class="score-value">{umbral_manual:.4f}</div>
                <div class="score-sub">Limite de clasificacion activo</div>
            </div>
            """, unsafe_allow_html=True)

        with sc3:
            signo = "+" if diferencia >= 0 else ""
            st.markdown(f"""
            <div class="score-box">
                <div class="score-label">Nivel de riesgo</div>
                <div class="score-value {riesgo_class}">{riesgo}</div>
                <div class="score-sub">Diferencia vs umbral: {signo}{diferencia:.4f}</div>
            </div>
            """, unsafe_allow_html=True)

        # Barra de riesgo
        score_norm = min(max((log_score + 40) / 40, 0.0), 1.0)
        st.progress(score_norm)
        st.caption("Barra de riesgo: izquierda = mayor anomalia, derecha = mayor normalidad")

        # Clasificacion final
        if log_score < umbral_manual:
            st.markdown(f"""
            <div class="result-card-fraud">
                <div class="result-label fraud">Alerta de Fraude</div>
                <div class="result-title">Transaccion Anomala Detectada</div>
                <div class="result-desc">
                    El log-score de esta transaccion ({log_score:.4f}) se encuentra por debajo
                    del umbral de deteccion ({umbral_manual:.4f}), lo que indica que su patron
                    es estadisticamente improbable bajo la distribucion de comportamiento normal
                    aprendida por el modelo. Se recomienda revision manual antes de procesar.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card-normal">
                <div class="result-label normal">Sin Anomalias</div>
                <div class="result-title">Transaccion dentro del Rango Normal</div>
                <div class="result-desc">
                    El log-score de esta transaccion ({log_score:.4f}) supera el umbral
                    de deteccion ({umbral_manual:.4f}), indicando que su patron es consistente
                    con el comportamiento financiero normal aprendido durante el entrenamiento.
                    La transaccion puede procesarse sin restricciones adicionales.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Ver vector de entrada enviado al modelo"):
            st.dataframe(
                X_input.T.rename(columns={0: "Valor escalado"}),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Error durante la prediccion: {e}")

# Footer
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#3d444d;
   text-align:center; letter-spacing:0.1em;">
DETECTOR DE FRAUDE &mdash; GAUSSIAN MIXTURE MODEL &mdash; SISTEMA DE ANOMALIAS FINANCIERAS
</p>
""", unsafe_allow_html=True)