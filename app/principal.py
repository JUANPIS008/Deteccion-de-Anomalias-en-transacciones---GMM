import streamlit as st

import pandas as pd

st.set_page_config(page_title="DAT RUN", layout="wide", initial_sidebar_state="collapsed")

url = 'https://github.com/JUANPIS008/datasets/blob/main/credit_card_fraud.csv?raw=true'

df = pd.read_csv(url)

def main():
    st.title("Detección de anomalías en transacciones con GMM")
    st.dataframe(df)

if __name__ == "__main__":
    main()