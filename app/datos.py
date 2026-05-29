import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

st.set_page_config(
    page_title="Exploracion de Datos",
    layout="wide",
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
.block-container { padding: 2.5rem 3rem; max-width: 1200px; }
h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; color: #e6edf3; }

.page-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: #161b27;
    border: 1px solid #21334a;
    color: #58a6ff;
    padding: 4px 12px;
    border-radius: 2px;
    display: inline-block;
    margin-bottom: 1rem;
}

.page-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.5rem;
}

.page-sub {
    font-size: 0.95rem;
    color: #6e7681;
    margin-bottom: 2rem;
    line-height: 1.7;
}

.divider { border: none; border-top: 1px solid #1e2d40; margin: 2rem 0; }

.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #58a6ff;
    border-left: 3px solid #58a6ff;
    padding-left: 10px;
    margin-bottom: 1.2rem;
}

.stat-card {
    background: #111827;
    border: 1px solid #1e2d40;
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
}

.stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.3rem;
}

.stat-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.7rem;
    font-weight: 600;
    color: #e6edf3;
}

.stat-desc { font-size: 0.75rem; color: #6e7681; margin-top: 0.2rem; }

.insight-box {
    background: #111827;
    border: 1px solid #1e2d40;
    border-left: 3px solid #58a6ff;
    border-radius: 0 6px 6px 0;
    padding: 1rem 1.3rem;
    font-size: 0.85rem;
    color: #8b949e;
    line-height: 1.7;
    margin-top: 1rem;
}

footer { display: none; }
</style>
""", unsafe_allow_html=True)

# Carga de datos
@st.cache_data
def cargar_datos():
    url = 'https://github.com/JUANPIS008/datasets/blob/main/credit_card_fraud.csv?raw=true'
    return pd.read_csv(url)

with st.spinner("Cargando dataset..."):
    df = cargar_datos()

df_normal = df[df['Fraud Flag or Label'] == 0]
df_fraude = df[df['Fraud Flag or Label'] == 1]

PLOT_BG    = "#0b0f19"
CARD_BG    = "#111827"
GRID_COLOR = "#1e2d40"
COLOR_NORM = "#58a6ff"
COLOR_FRAUD= "#f0883e"
FONT_MONO  = "IBM Plex Mono"

def apply_style(ax, title=""):
    ax.set_facecolor(CARD_BG)
    ax.figure.patch.set_facecolor(PLOT_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.tick_params(colors="#6e7681", labelsize=8)
    ax.xaxis.label.set_color("#8b949e")
    ax.yaxis.label.set_color("#8b949e")
    ax.xaxis.label.set_fontsize(9)
    ax.yaxis.label.set_fontsize(9)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    if title:
        ax.set_title(title, color="#e6edf3", fontsize=10,
                     fontfamily=FONT_MONO, pad=10)

# Header 
st.markdown('<div class="page-tag">Modulo de Analisis</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Exploracion del Dataset</div>', unsafe_allow_html=True)
st.markdown("""
<p class="page-sub">
Analisis descriptivo y visual del conjunto de datos de transacciones financieras.
Esta seccion permite comprender la distribucion de las variables, el nivel de desbalance
entre clases y el comportamiento estadistico de las features utilizadas por el modelo GMM.
</p>
""", unsafe_allow_html=True)

# KPIs
st.markdown('<div class="section-title">Estadisticas Generales</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    ("Registros Totales",    f"{len(df):,}",              "Transacciones en el dataset"),
    ("Transacciones Normales",f"{len(df_normal):,}",      f"{len(df_normal)/len(df)*100:.1f}% del total"),
    ("Transacciones Fraude", f"{len(df_fraude):,}",       f"{len(df_fraude)/len(df)*100:.1f}% del total"),
    ("Monto Promedio",       f"${df['Transaction Amount'].mean():,.0f}", "Promedio general"),
    ("Monto Maximo",         f"${df['Transaction Amount'].max():,.0f}",  "Valor mas alto registrado"),
]
for col, (label, value, desc) in zip([c1, c2, c3, c4, c5], kpis):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Graficos fila 1 ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Distribucion por Clase</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="large")

with g1:
    fig, ax = plt.subplots(figsize=(6, 3.8))
    counts = df['Fraud Flag or Label'].value_counts().sort_index()
    bars = ax.bar(
        ['Normal', 'Fraude'], counts.values,
        color=[COLOR_NORM, COLOR_FRAUD],
        width=0.45, edgecolor="none"
    )
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                f"{val:,}", ha='center', va='bottom',
                color="#e6edf3", fontsize=9, fontfamily=FONT_MONO)
    apply_style(ax, "Cantidad de transacciones por clase")
    ax.set_ylabel("Transacciones")
    st.pyplot(fig)
    plt.close()
    st.markdown("""
    <div class="insight-box">
        El dataset presenta un balance casi perfecto entre clases (50/50), lo cual es inusual
        en datasets de fraude real. En produccion, el fraude suele representar menos del 1%.
        Esta proporcion igual afecta negativamente al GMM, que asume que el comportamiento
        anormal es raro en comparacion con el normal.
    </div>
    """, unsafe_allow_html=True)

with g2:
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.hist(df_normal['Transaction Amount'], bins=40, alpha=0.75,
            color=COLOR_NORM, label='Normal', edgecolor='none')
    ax.hist(df_fraude['Transaction Amount'], bins=40, alpha=0.6,
            color=COLOR_FRAUD, label='Fraude', edgecolor='none')
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR,
              labelcolor="#8b949e", fontsize=8)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    apply_style(ax, "Distribucion del monto por clase")
    ax.set_xlabel("Monto de la transaccion")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)
    plt.close()
    st.markdown("""
    <div class="insight-box">
        Las distribuciones de monto entre transacciones normales y fraudulentas son
        estadisticamente indistinguibles. Ambas tienen media cercana a $2,500 y
        desviacion estandar similar. Esta superposicion es la causa principal de las
        limitaciones de precision del modelo con este dataset.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Graficos fila 2
st.markdown('<div class="section-title">Variables Categoricas</div>', unsafe_allow_html=True)

g3, g4, g5 = st.columns(3, gap="large")

with g3:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ct = df.groupby(['Card Type', 'Fraud Flag or Label']).size().unstack(fill_value=0)
    ct.columns = ['Normal', 'Fraude']
    ct.plot(kind='bar', ax=ax, color=[COLOR_NORM, COLOR_FRAUD],
            edgecolor='none', width=0.6)
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR,
              labelcolor="#8b949e", fontsize=8)
    ax.set_xticklabels(ct.index, rotation=0, fontsize=8)
    apply_style(ax, "Fraude por tipo de tarjeta")
    ax.set_xlabel("")
    ax.set_ylabel("Transacciones")
    st.pyplot(fig)
    plt.close()

with g4:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    src = df.groupby(['Transaction Source', 'Fraud Flag or Label']).size().unstack(fill_value=0)
    src.columns = ['Normal', 'Fraude']
    src.plot(kind='bar', ax=ax, color=[COLOR_NORM, COLOR_FRAUD],
             edgecolor='none', width=0.5)
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR,
              labelcolor="#8b949e", fontsize=8)
    ax.set_xticklabels(src.index, rotation=0, fontsize=8)
    apply_style(ax, "Fraude por canal de transaccion")
    ax.set_xlabel("")
    ax.set_ylabel("Transacciones")
    st.pyplot(fig)
    plt.close()

with g5:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    dev = df.groupby(['Device Information', 'Fraud Flag or Label']).size().unstack(fill_value=0)
    dev.columns = ['Normal', 'Fraude']
    dev.plot(kind='bar', ax=ax, color=[COLOR_NORM, COLOR_FRAUD],
             edgecolor='none', width=0.5)
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR,
              labelcolor="#8b949e", fontsize=8)
    ax.set_xticklabels(dev.index, rotation=0, fontsize=8)
    apply_style(ax, "Fraude por dispositivo")
    ax.set_xlabel("")
    ax.set_ylabel("Transacciones")
    st.pyplot(fig)
    plt.close()

st.markdown("""
<div class="insight-box">
    Ningun tipo de tarjeta, canal ni dispositivo muestra una tasa de fraude significativamente
    distinta al resto. Todas las categorias se distribuyen en proporcion casi igual entre
    Normal y Fraude, lo que confirma el origen sintetico y aleatorio del dataset.
    En datos reales, variables como el canal online o dispositivos moviles suelen
    correlacionarse mas con actividad fraudulenta.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# Tabla 
st.markdown('<div class="section-title">Muestra del Dataset</div>', unsafe_allow_html=True)

cols_mostrar = [
    'Transaction Date and Time', 'Transaction Amount',
    'Merchant Category Code (MCC)', 'Transaction Response Code',
    'Card Type', 'Transaction Source', 'Device Information',
    'Fraud Flag or Label'
]

st.dataframe(
    df[cols_mostrar].head(100),
    use_container_width=True,
    hide_index=True
)

# Footer 
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<p style="font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:#3d444d;
   text-align:center; letter-spacing:0.1em;">
EXPLORACION DE DATOS &mdash; SISTEMA DE DETECCION DE ANOMALIAS FINANCIERAS
</p>
""", unsafe_allow_html=True)