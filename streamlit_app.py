import streamlit as st
import pandas as pd

# --- CONFIGURACIÓ DE LA PÀGINA ---
st.set_page_config(page_title="Visor de Dades", page_icon="📊")

st.title("📊 Previsualització de l'Excel")

# 1. ID del teu Google Sheet (extret de la teva URL)
SHEET_ID = "1FvNGh_SySwgVFaPHBzAxd6EocWnOCPQ-kUTFe1TIWSE"
# 2. Construïm la URL d'exportació directa a CSV
URL_CSV = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

if st.button('Carregar dades de Google Sheets'):
    with st.spinner('Connectant amb Google Sheets...'):
        try:
            # Llegim tot el document
            df = pd.read_csv(URL_CSV)
            
            # FILTRATGE (A:H és columnes 0 a 8, Files 1:10 és índex 0 a 10)
            # .iloc[files, columnes]
            df_filtrat = df.iloc[0:10, 0:8]
            
            st.success("Dades carregades correctament!")
            
            # Mostrem la taula a la web
            # st.dataframe crea una taula interactiva (pots moure columnes, ordenar, etc.)
            st.subheader("Segment seleccionat (A1:H10):")
            st.dataframe(df_filtrat, use_container_width=True)
            
            # Si prefereixes una taula estàtica i neta, pots fer servir:
            # st.table(df_filtrat)

        except Exception as e:
            st.error(f"No s'ha pogut llegir l'arxiu. Revisa que el Sheets estigui 'Publicat a la web'. Error: {e}")
else:
    st.info("Prem el botó per veure l'estat actual de l'Excel.")
