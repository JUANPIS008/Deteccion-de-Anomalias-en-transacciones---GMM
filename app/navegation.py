import streamlit as st
 
pages = {
    "Analisis": [
        st.Page("prediccion.py", title="Detector de Fraude"),
    ],

    "Informacion": [
        st.Page("principal.py", title="Informacion del Proyecto"),
        st.Page("datos.py", title="Exploracion de Datos"),
    ],
    
}
 
pg = st.navigation(pages)
pg.run()