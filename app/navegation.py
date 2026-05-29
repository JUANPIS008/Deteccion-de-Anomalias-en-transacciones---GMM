import streamlit as st
 
pages = {
    "Sistema": [
        st.Page("principal.py", title="Inicio"),
    ],
    "Analisis": [
        st.Page("datos.py", title="Exploracion de Datos"),
        st.Page("prediccion.py", title="Detector de Fraude"),
    ],
}
 
pg = st.navigation(pages)
pg.run()