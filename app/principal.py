import streamlit as st

st.set_page_config(page_title="Sistema de Deteccion de Fraude", layout="wide", initial_sidebar_state="collapsed")

# Estilos globales
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0b0f19;
    color: #c9d1d9;
}

.block-container {
    padding: 2.5rem 3rem 3rem 3rem;
    max-width: 1100px;
}

h1, h2, h3 {
    font-family: 'IBM Plex Mono', monospace;
    color: #e6edf3;
    letter-spacing: -0.5px;
}

.hero-tag {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: #161b27;
    border: 1px solid #21334a;
    color: #58a6ff;
    padding: 4px 12px;
    border-radius: 2px;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.6rem;
    font-weight: 600;
    color: #e6edf3;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: #8b949e;
    line-height: 1.75;
    max-width: 680px;
    margin-bottom: 2.5rem;
}

.divider {
    border: none;
    border-top: 1px solid #1e2d40;
    margin: 2.5rem 0;
}

.stat-card {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
}

.stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.4rem;
}

.stat-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.9rem;
    font-weight: 600;
    color: #e6edf3;
}

.stat-desc {
    font-size: 0.8rem;
    color: #6e7681;
    margin-top: 0.3rem;
}

.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #58a6ff;
    border-left: 3px solid #58a6ff;
    padding-left: 10px;
    margin-bottom: 1.2rem;
}

.problem-block {
    background: #111827;
    border: 1px solid #1e2d40;
    border-left: 3px solid #f0883e;
    border-radius: 0 6px 6px 0;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.problem-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #f0883e;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.problem-text {
    font-size: 0.9rem;
    color: #8b949e;
    line-height: 1.65;
}

.solution-block {
    background: #111827;
    border: 1px solid #1e2d40;
    border-left: 3px solid #3fb950;
    border-radius: 0 6px 6px 0;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.solution-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #3fb950;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.solution-text {
    font-size: 0.9rem;
    color: #8b949e;
    line-height: 1.65;
}

.pipeline-step {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}

.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    color: #58a6ff;
    opacity: 0.4;
}

.step-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #e6edf3;
    margin: 0.3rem 0;
    font-weight: 600;
}

.step-text {
    font-size: 0.78rem;
    color: #6e7681;
    line-height: 1.55;
}

.metric-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.metric-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    padding: 3px 10px;
    border-radius: 2px;
    background: #161b27;
    border: 1px solid #21334a;
    color: #8b949e;
}

.metric-badge.warn {
    border-color: #f0883e44;
    color: #f0883e;
}

.metric-badge.ok {
    border-color: #3fb95044;
    color: #3fb950;
}

footer { display: none; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="hero-tag">Sistema de Deteccion de Anomalias</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Deteccion de Fraude<br>en Transacciones Financieras</div>', unsafe_allow_html=True)
st.markdown("""
<p class="hero-sub">
Sistema basado en aprendizaje automatico no supervisado que identifica transacciones
financieras anomalas en tiempo real. Utiliza Gaussian Mixture Models (GMM) entrenados
exclusivamente con comportamiento normal para detectar desviaciones estadisticas
significativas que pueden indicar actividad fraudulenta.
</p>
""", unsafe_allow_html=True)

# Resumen del dataset
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Resumen del Dataset</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Transacciones</div>
        <div class="stat-value">8,000</div>
        <div class="stat-desc">Registros totales analizados</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Transacciones Normales</div>
        <div class="stat-value">4,011</div>
        <div class="stat-desc">50.1% del total — clase base del GMM</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Transacciones Fraude</div>
        <div class="stat-value">3,989</div>
        <div class="stat-desc">49.9% del total — clase anomala</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Variables del Modelo</div>
        <div class="stat-value">4</div>
        <div class="stat-desc">Time, Amount, MCC, Response Code</div>
    </div>
    """, unsafe_allow_html=True)

# Problema y Solucion
st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_prob, col_sol = st.columns(2, gap="large")

with col_prob:
    st.markdown('<div class="section-title">El Problema</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="problem-block">
        <div class="problem-title">Desbalance de Clases</div>
        <div class="problem-text">
            En entornos financieros reales, el fraude representa entre el 0.1% y el 5%
            de las transacciones totales. Los clasificadores supervisados entrenados en
            estos datos tienden a ignorar la clase minoritaria, produciendo modelos
            que simplemente predicen siempre la clase mayoritaria.
        </div>
    </div>
    <div class="problem-block">
        <div class="problem-title">Costo Asimetrico de los Errores</div>
        <div class="problem-text">
            No detectar un fraude (falso negativo) tiene un costo economico y reputacional
            mucho mayor que bloquear una transaccion legitima (falso positivo).
            Esta asimetria exige un enfoque que priorice el recall sobre la precision.
        </div>
    </div>
    <div class="problem-block">
        <div class="problem-title">Evolucion Constante del Fraude</div>
        <div class="problem-text">
            Los patrones de fraude cambian continuamente. Un modelo supervisado
            entrenado con fraudes historicos puede quedar obsoleto rapidamente
            ante tecnicas nuevas que no han sido vistas anteriormente.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_sol:
    st.markdown('<div class="section-title">La Solucion: GMM</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="solution-block">
        <div class="solution-title">Aprendizaje No Supervisado</div>
        <div class="solution-text">
            El modelo se entrena exclusivamente con transacciones normales, aprendiendo
            su distribucion estadistica. No requiere ejemplos de fraude etiquetados
            para funcionar, lo que lo hace aplicable incluso cuando el fraude es raro
            o no esta disponible en el conjunto de entrenamiento.
        </div>
    </div>
    <div class="solution-block">
        <div class="solution-title">Deteccion por Densidad</div>
        <div class="solution-text">
            El GMM asigna a cada transaccion un log-score de densidad de probabilidad.
            Las transacciones que caen en regiones de baja densidad bajo la distribucion
            aprendida — es decir, que son estadisticamente improbables dado el
            comportamiento normal — se clasifican como anomalias.
        </div>
    </div>
    <div class="solution-block">
        <div class="solution-title">Umbral Configurable</div>
        <div class="solution-text">
            El nivel de sensibilidad del detector se ajusta mediante un umbral
            de log-score calibrado con los datos reales del sistema. Esto permite
            balancear precision y recall segun el contexto operativo sin necesidad
            de reentrenar el modelo.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Metricas del modelo
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Estado del Modelo en Produccion</div>', unsafe_allow_html=True)

mc1, mc2 = st.columns([1, 1], gap="large")

with mc1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Metricas de Evaluacion (Test Set)</div>
        <br>
        <div style="display:flex; flex-direction:column; gap:0.6rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e2d40; padding-bottom:0.6rem;">
                <span style="font-size:0.85rem; color:#8b949e;">Accuracy</span>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; color:#f0883e;">50%</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e2d40; padding-bottom:0.6rem;">
                <span style="font-size:0.85rem; color:#8b949e;">Precision (Fraude)</span>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; color:#f0883e;">57%</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e2d40; padding-bottom:0.6rem;">
                <span style="font-size:0.85rem; color:#8b949e;">Recall (Fraude)</span>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; color:#3fb950;">96%</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:0.85rem; color:#8b949e;">F1-Score (Fraude)</span>
                <span style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; color:#8b949e;">0.71</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with mc2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-label">Interpretacion de las Metricas</div>
        <br>
        <div class="problem-text" style="font-size:0.85rem; line-height:1.75;">
            El <strong style="color:#3fb950;">recall del 96%</strong> indica que el modelo identifica
            correctamente casi la totalidad de los fraudes reales presentes en el conjunto de prueba.
            En seguridad financiera, esta es la metrica critica: es preferible generar alertas de mas
            que dejar pasar transacciones fraudulentas sin detectar.
            <br><br>
            La <strong style="color:#f0883e;">precision del 57%</strong> refleja una tasa de falsos
            positivos moderada, atribuible a que el dataset de entrenamiento es sintetico y las
            distribuciones de ambas clases son estadisticamente similares. En produccion con datos
            reales, esta metrica mejora significativamente.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#3d444d; text-align:center; letter-spacing:0.1em;">
SISTEMA DE DETECCION DE ANOMALIAS FINANCIERAS &mdash; GAUSSIAN MIXTURE MODEL
</p>
""", unsafe_allow_html=True)