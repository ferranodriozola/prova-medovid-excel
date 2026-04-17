import streamlit as st
import pandas as pd
import requests

# --- EL TEU CODI DE CONVERSIÓ ---
# He creat una funció on has d'enganxar la teva lògica de Python
def el_meu_codi_python(df):
    """
    Aquesta funció rep un DataFrame de Pandas (l'Excel)
    i retorna el text XML final.
    """
    xml_resultat = '<?xml version="1.0" encoding="UTF-8"?>\n<dades>\n'
    
    for index, fila in df.iterrows():
        xml_resultat += f'  <item id="{index}">\n'
        for col in df.columns:
            # Aquí personalitza segons el teu XML
            xml_resultat += f'    <{col}>{fila[col]}</{col}>\n'
        xml_resultat += '  </item>\n'
    
    xml_resultat += '</dades>'
    return xml_resultat

# --- CONFIGURACIÓ DE LA PÀGINA WEB ---
st.set_page_config(page_title="Convertidor Excel a XML", page_icon="🚀")

st.title("🔄 Generador d'XML de l'Equip")
st.write("Aquesta eina agafa les dades en temps real de Google Sheets i genera l'XML.")

# URL del Google Sheet publicat com a CSV
# Posa aquí la URL que has copiat al pas 1
URL_SHEET = "https://docs.google.com/spreadsheets/d/1FvNGh_SySwgVFaPHBzAxd6EocWnOCPQ-kUTFe1TIWSE/edit?usp=sharing"

if st.button('Generar XML actualitzat'):
    with st.spinner('Llegint Google Sheets i processant...'):
        try:
            df = pd.read_csv(URL_SHEET)
            
            resultat_final = el_meu_codi_python(df)
            
            st.success("✅ XML generat correctament!")
            
            st.subheader("Resultat XML:")

            st.code(resultat_final, language='xml')
            
            # Opcional: Botó per descarregar el fitxer directament
            st.download_button(
                label="Descarregar fitxer .xml",
                data=resultat_final,
                file_name="dades_equip.xml",
                mime="application/xml"
            )
            
        except Exception as e:
            st.error(f"S'ha produït un error: {e}")
else:
    st.info("Fes clic al botó per carregar les dades més recents.")
