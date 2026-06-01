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

.risk-high { color: #f0883e; }
.risk-med  { color: #d29922; }
.risk-low  { color: #3fb950; }

.info-note {
    background: #111827; border: 1px solid #1e2d40;
    border-radius: 6px; padding: 1rem 1.2rem;
    font-size: 0.82rem; color: #6e7681; line-height: 1.65;
}

/* Manual de usuario */
.manual-container {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin-bottom: 0.5rem;
}
.manual-intro {
    font-size: 0.88rem;
    color: #8b949e;
    line-height: 1.75;
    margin-bottom: 1.4rem;
    border-bottom: 1px solid #1e2d40;
    padding-bottom: 1.2rem;
}
.manual-step {
    display: flex;
    gap: 1.2rem;
    align-items: flex-start;
    margin-bottom: 1.2rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #161b27;
}
.manual-step:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: #58a6ff;
    background: #0b0f19;
    border: 1px solid #21334a;
    border-radius: 3px;
    padding: 2px 8px;
    white-space: nowrap;
    margin-top: 2px;
    min-width: 28px;
    text-align: center;
}
.step-content {}
.step-field {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.3rem;
}
.step-desc {
    font-size: 0.82rem;
    color: #6e7681;
    line-height: 1.65;
}
.step-example {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #3fb950;
    background: #0b1a0f;
    border: 1px solid #1e3a1e;
    border-radius: 3px;
    padding: 2px 8px;
    display: inline-block;
    margin-top: 0.4rem;
}
.step-warning {
    font-size: 0.78rem;
    color: #d29922;
    background: #1a1500;
    border: 1px solid #3a2e00;
    border-radius: 3px;
    padding: 4px 10px;
    display: inline-block;
    margin-top: 0.4rem;
}
.manual-result-block {
    background: #0b0f19;
    border: 1px solid #1e2d40;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
}
.result-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0.5rem 0;
    border-bottom: 1px solid #161b27;
    gap: 1rem;
}
.result-row:last-child { border-bottom: none; }
.result-row-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #58a6ff;
    white-space: nowrap;
}
.result-row-desc {
    font-size: 0.8rem;
    color: #6e7681;
    line-height: 1.55;
    text-align: right;
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
    st.error(f"No se encontró el archivo: {e}")
    st.info("Asegúrate de que modelo_gmm.pkl y scaler.pkl estén en la carpeta models/")
    st.stop()

FEATURE_COLS = list(gmm_model.feature_names_in_)

# Sidebar
st.sidebar.markdown("### Configuración del Detector")
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
Calcula la densidad de probabilidad logarítmica de cada nueva transacción bajo esa
distribución aprendida. Un score muy bajo indica que la transacción es estadísticamente
improbable dentro del comportamiento normal.
</div>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="page-tag">Módulo de predicción</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Análisis de Transacción</div>', unsafe_allow_html=True)
st.markdown("""
<p class="page-sub">
Ingresa los datos de una transacción financiera para determinar si su comportamiento
es consistente con el patrón normal aprendido por el modelo, o si presenta
caracteristicas estadisticamente anomalas que sugieren actividad fraudulenta.
</p>
""", unsafe_allow_html=True)

# Informacion del dataset 
with st.expander("Sobre el dataset y el alcance del modelo"):

    st.caption(
        "Esta sección describe el origen de los datos utilizados para entrenar el modelo "
        "y las condiciones bajo las cuales sus predicciones son válidas."
    )

    st.markdown("---")

    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown("**Origen de los datos**")
        st.write(
            "El modelo fue entrenado con el dataset Credit Card Fraud, publicado por "
            "la empresa Incribo y disponible públicamente en Kaggle. Se trata de un "
            "conjunto de datos sintético diseñado para simular escenarios reales de "
            "fraude en tarjetas de crédito con fines analíticos y educativos. "
            "Al ser sintético, no contiene información financiera real de usuarios "
            "o entidades bancarias."
        )

        st.markdown("**Distribución de clases**")
        st.write(
            "El dataset presenta un balance casi equitativo entre transacciones normales "
            "y fraudulentas (aproximadamente 50% cada una), lo cual difiere de los "
            "escenarios financieros reales donde el fraude suele representar menos del 1%. "
            "Esta característica afecta la forma en que el modelo GMM calibra sus "
            "predicciones y debe tenerse en cuenta al interpretar los resultados."
        )

    with c2:
        st.markdown("**Composición del dataset**")
        st.code(
            "  8,000  transacciones en total\n"
            "  4,011  transacciones normales\n"
            "  3,989  transacciones fraudulentas\n"
            "     20  variables por registro",
            language=None
        )

        st.markdown("**Variables utilizadas por el modelo**")
        st.code(
            "Time               — fecha y hora de la transacción\n"
            "Amount             — monto de la transacción\n"
            "MCC                — Código de categoría del comercio\n"
            "Response Code      — Código de respuesta del procesador\n"
            "Fraud Flag or Label — 0 = normal, 1 = fraude",
            language=None
        )

    st.markdown("---")
    st.markdown("**Limitaciones que debes conocer**")

    l1, l2 = st.columns(2, gap="large")

    with l1:
        st.warning(
            "El dataset es sintético. Los patrones de fraude fueron generados "
            "artificialmente y pueden no reflejar con exactitud los comportamientos "
            "observados en sistemas financieros reales.",
            icon=None
        )

    with l2:
        st.warning(
            "El volumen de 8,000 registros es considerablemente menor al utilizado "
            "en producción por instituciones financieras reales, donde se analizan "
            "millones de transacciones. Esto limita la capacidad generalizadora del modelo.",
            icon=None
        )

    st.markdown("---")
    st.caption(
        "Fuente: Incribo — Credit Card Fraud Dataset. "
        "Disponible en: kaggle.com/datasets/teamincribo/credit-card-fraud"
    )

# Formulario 
st.markdown('<hr class="divider">', unsafe_allow_html=True)
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
            help="Valor monetario de la transacción. Usa punto como separador decimal. Ejemplo: 1250.75"        
            )

        mcc = st.selectbox(
            "Merchant Category Code (MCC)",
            options=[5411, 5812, 5999, 4111, 6011, 7995, 6051],
            format_func=lambda x: {
                5411: "5411 — Supermercados",
                5812: "5812 — Restaurantes",
                5999: "5999 — Retail general",
                4111: "4111 — Transporte",
                6011: "6011 — Cajeros automáticos (ATM)",
                7995: "7995 — Casinos y apuestas",
                6051: "6051 — Casas de cambio",
            }[x],
            help="Categoría del comercio donde se realizó la transacción según el estándar ISO 18245."
        )

    with col2:
        fecha = st.date_input(
            "Fecha de la transacción",
            value=datetime.now().date(),
            help="Fecha exacta en que se genero el cargo. No usar fecha de corte o de estado de cuenta."
        )

        hora = st.time_input(
            "Hora de la transacción",
            value=datetime.now().time(),
            help="Hora en formato 24h. Las transacciones en madrugada pueden generar puntajes de riesgo mas altos."
        )

        response_code = st.selectbox(
            "Código de respuesta del procesador",
            options=list(range(13)),
            format_func=lambda x: {
                0:  "0  — Aprobada",
                1:  "1  — Rechazada por fondos insuficientes",
                2:  "2  — Error del sistema",
                3:  "3  — Transacción no permitida",
                4:  "4  — Tarjeta vencida",
                5:  "5  — Rechazada por banco emisor",
                6:  "6  — Error de comunicación",
                7:  "7  — Fraude confirmado por banco",
                8:  "8  — Limite de credito excedido",
                9:  "9  — PIN incorrecto",
                10: "10 — Tarjeta reportada como robada",
                11: "11 — Cuenta bloqueada",
                12: "12 — Transacción duplicada",
            }[x],
            help="Código devuelto por el procesador al momento de la transacción. Aparece en el comprobante de pago."
        )

    submitted = st.form_submit_button(
        "Analizar Transacción",
        use_container_width=True
    )

# Manual de usuario
with st.expander("Como completar el formulario correctamente"):

    st.caption(
        "Este módulo analiza una transacción financiera individual y determina si su comportamiento "
        "es normal o anormal según el modelo de detección entrenado. Para obtener un resultado "
        "correcto, cada campo debe completarse con los valores exactos del comprobante o registro "
        "de la transacción que se desea evaluar."
    )

    st.markdown("---")

    # Paso 1
    st.markdown("**1 — Monto de la transacción**")
    st.write(
        "Ingresa el valor monetario total de la transacción en la moneda en que fue registrada "
        "originalmente. Usa punto como separador decimal. No incluyas simbolos de moneda ni "
        "separadores de miles. El campo acepta valores entre 0.00 y 100,000.00."
    )
    st.code("Correcto:   1250.75\nIncorrecto: $1.250,75", language=None)

    st.markdown("---")

    # Paso 2
    st.markdown("**2 — Merchant Category Code (MCC)**")
    st.write(
        "Selecciona la categoría del comercio donde se realizó la transacción. El MCC es un código "
        "de 4 dígitos asignado por la red de pagos al tipo de negocio. Si no conoces el MCC exacto "
        "del comercio, selecciona la categoría que más se aproxime al giro del negocio."
    )
    st.code(
        "5411 — Supermercados y tiendas de abarrotes\n"
        "5812 — Restaurantes y servicios de comida\n"
        "5999 — Comercio minorista general\n"
        "4111 — Transporte urbano y servicios de movilidad\n"
        "6011 — Cajeros automaticos (ATM) y retiros en efectivo\n"
        "7995 — Casinos, apuestas y juegos de azar\n"
        "6051 — Casas de cambio de moneda extranjera",
        language=None
    )
    st.warning(
        "Los códigos 6011, 7995 y 6051 corresponden a categorías de alto riesgo "
        "y pueden generar puntajes de anomalía más elevados por naturaleza.",
        icon=None
    )

    st.markdown("---")

    # Paso 3
    st.markdown("**3 — Fecha de la transacción**")
    st.write(
        "Selecciona la fecha exacta en que se realizó la transacción usando el selector de calendario. "
        "La fecha debe corresponder al momento en que el cargo fue generado, no a la fecha de corte "
        "o de estado de cuenta. El sistema acepta fechas pasadas y la fecha actual."
    )
    st.code("Formato: DD/MM/AAAA   |   Ejemplo: 15/03/2024", language=None)

    st.markdown("---")

    # Paso 4
    st.markdown("**4 — Hora de la transacción**")
    st.write(
        "Ingresa la hora exacta de la transacción en formato de 24 horas. Este dato es relevante "
        "para el modelo porque el horario en que ocurre una transacción forma parte de su patrón "
        "de comportamiento. Las transacciones en horas inusuales como madrugada pueden recibir "
        "puntajes de anomalía más altos."
    )
    st.code(
        "14:35 — Tarde (horario comercial normal)\n"
        "03:12 — Madrugada (puede elevar el puntaje de riesgo)",
        language=None
    )

    st.markdown("---")

    # Paso 5
    st.markdown("**5 — Código de respuesta del procesador**")
    st.write(
        "Selecciona el código que el procesador de pagos devolvió al momento de la transacción. "
        "Indica si fue aprobada, rechazada o si ocurrió algún tipo de error. Generalmente aparece "
        "en el comprobante de pago o en el registro del sistema de punto de venta."
    )
    st.code(
        "0  — Aprobada: la transacción fue procesada exitosamente\n"
        "1  — Rechazada por fondos insuficientes\n"
        "5  — Rechazada por el banco emisor sin causa especificada\n"
        "7  — Fraude confirmado por el banco emisor\n"
        "10 — Tarjeta reportada como robada o extraviada\n"
        "11 — Cuenta bloqueada por la entidad financiera",
        language=None
    )
    st.warning(
        "Los códigos 7, 10 y 11 indican situaciones de alto riesgo confirmadas por la entidad "
        "financiera y casi siempre producirán una alerta de fraude.",
        icon=None
    )

    st.markdown("---")

    # Paso 6
    st.markdown("**6 — Interpretación de los resultados**")
    st.write(
        "Una vez enviado el formulario, el sistema muestra tres indicadores y una clasificación final."
    )

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Log-score GMM**")
        st.caption(
            "Valor negativo calculado por el modelo. Cuanto más cercano a cero, más normal "
            "es la transacción. Cuanto más bajo (más negativo), mas anómala es respecto al "
            "comportamiento aprendido."
        )
        st.markdown("**Umbral configurado**")
        st.caption(
            "Valor de corte del detector. Si el log-score cae por debajo de este número, "
            "la transacción se clasifica como fraude. Se ajusta desde el panel lateral."
        )
    with r2:
        st.markdown("**Nivel de riesgo**")
        st.caption(
            "BAJO: transacción dentro del rango normal.\n"
            "MEDIO: ligeramente por debajo del umbral, se recomienda revisión.\n"
            "ALTO: anomalía significativa detectada."
        )
        st.markdown("**Diferencia vs umbral**")
        st.caption(
            "Valor positivo: score por encima del umbral (normal). "
            "Valor negativo: score por debajo del umbral (potencial fraude)."
        )

    st.markdown("---")

    # Paso 7
    st.markdown("**7 — Ajuste del umbral de sensibilidad**")
    st.write(
        "El umbral de log-score se puede modificar desde el panel lateral. Un umbral mas alto "
        "detecta más transacciones como fraude, pero genera más falsas alarmas. Un umbral más bajo "
        "es más conservador y solo alerta ante anomalías severas. El valor por defecto (-16.46) "
        "corresponde al percentil 5% calibrado con el dataset de entrenamiento."
    )
    st.code(
        "-16.88 — Conservador: solo anomalías muy evidentes\n"
        "-16.46 — Equilibrado: configuración recomendada\n"
        "-16.10 — Agresivo: detecta más casos, más falsas alarmas",
        language=None
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
        st.markdown('<div class="section-title">Resultado del Análisis</div>', unsafe_allow_html=True)

        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-label">Log-score GMM</div>
                <div class="score-value">{log_score:.4f}</div>
                <div class="score-sub">Densidad logarítmica bajo el modelo</div>
            </div>
            """, unsafe_allow_html=True)

        with sc2:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-label">Umbral configurado</div>
                <div class="score-value">{umbral_manual:.4f}</div>
                <div class="score-sub">Limite de clasificación activo</div>
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

        score_norm = min(max((log_score + 40) / 40, 0.0), 1.0)
        st.progress(score_norm)
        st.caption("Barra de riesgo: izquierda = mayor anomalía — derecha = mayor normalidad")

        if log_score < umbral_manual:
            st.markdown(f"""
            <div class="result-card-fraud">
                <div class="result-label fraud">Alerta de Fraude</div>
                <div class="result-title">Transacción Anómala Detectada</div>
                <div class="result-desc">
                    El log-score de esta transacción ({log_score:.4f}) se encuentra por debajo
                    del umbral de detección ({umbral_manual:.4f}), lo que indica que su patron
                    es estadísticamente improbable bajo la distribución de comportamiento normal
                    aprendida por el modelo. Se recomienda revisión manual antes de procesar.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card-normal">
                <div class="result-label normal">Sin Anomalías</div>
                <div class="result-title"> Transacción dentro del Rango Normal</div>
                <div class="result-desc">
                    El log-score de esta transacción ({log_score:.4f}) supera el umbral
                    de detección ({umbral_manual:.4f}), indicando que su patrón es consistente
                    con el comportamiento financiero normal aprendido durante el entrenamiento.
                    La transacción puede procesarse sin restricciones adicionales.
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
DETECTOR DE FRAUDE &mdash; GAUSSIAN MIXTURE MODEL &mdash; SISTEMA DE ANOMALÍAS FINANCIERAS
</p>
""", unsafe_allow_html=True)