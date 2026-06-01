import streamlit as st
 
pages = {
    "Análisis": [
        st.Page("prediccion.py", title="Detector de Fraude"),
    ],

    "Información": [
        st.Page("principal.py", title="Información del Proyecto"),
        st.Page("datos.py", title="Exploración de Datos"),
    ],
    
}
 
pg = st.navigation(pages)
pg.run()