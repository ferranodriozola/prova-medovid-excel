import streamlit as st
import pandas as pd
import requests
import certifi
from io import BytesIO

# --- CONFIGURACIÓ DE LA PÀGINA ---
st.set_page_config(page_title="Eina de Dades Multiformat", page_icon="🛠️")

st.title("🛠️ Visor de Dades de l'Equip")
st.write("Tria com vols visualitzar les dades del Google Sheet.")

# 1. Configuració de la font de dades
URL_XLSX = f"https://docs.google.com/spreadsheets/d/{st.secrets['SHEET_ID']}/export?format=xlsx"


@st.cache_data
def descarregar_excel(url_xlsx: str) -> bytes:
    resposta = requests.get(url_xlsx, timeout=30, verify=certifi.where())
    resposta.raise_for_status()
    return resposta.content


@st.cache_data
def obtenir_fulls(url_xlsx: str):
    xls = pd.ExcelFile(BytesIO(descarregar_excel(url_xlsx)))
    return xls.sheet_names


@st.cache_data
def llegir_full(url_xlsx: str, full: str):
    return pd.read_excel(BytesIO(descarregar_excel(url_xlsx)), sheet_name=full)


fulls_disponibles = obtenir_fulls(URL_XLSX)

# 2. Interfície de selecció
full_seleccionat = st.selectbox("Selecciona el full de l'Excel:", fulls_disponibles)

opcio = st.radio(
    "Selecciona el format de sortida:",
    ('Taula Interactiva', 'Text Pla (Còpia ràpida)'),
    index=0
)

# Afegim un separador visual
st.divider()

# 3. Botó d'execució
if st.button('Carregar i Convertir'):
    with st.spinner('Processant dades...'):
        try:
            # Llegim el full seleccionat
            df = llegir_full(URL_XLSX, full_seleccionat)
            
            # Filtrem el rang A1:H10
            df_filtrat = df.iloc[0:250, 0:11]
            
            if opcio == 'Taula Interactiva':
                st.subheader("Visualització en format Taula")
                st.dataframe(df_filtrat, width='stretch')
                st.info("Pots clicar a les capçaleres per ordenar les dades.")
            
            else:
                st.subheader("Visualització en format Text")
                text_pla = df_filtrat.to_string(index=False)
                # Fem servir language='text' perquè no ressalti colors estranys
                st.code(text_pla, language='text')
                st.info("Usa el botó de la dreta per copiar tot el text al portaretalls.")

        except Exception as e:
            st.error(f"S'ha produït un error en la connexió: {e}")
else:
    st.info("Selecciona un format a dalt i prem el botó per començar.")
