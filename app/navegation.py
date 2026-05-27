import streamlit as st

pages = {
    "Menu Principal": [
        st.Page("principal.py", title="Pagina Principal"),
    ],

    "Datos": [
        st.Page("datos.py", title="Análisis de Datos")
    ]

}

pg = st.navigation(pages)
pg.run()