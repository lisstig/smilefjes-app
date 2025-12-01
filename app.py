import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- KONFIGURASJON ---
st.set_page_config(page_title="Smilefjes-sjekken", page_icon="🙂")

st.title("🧐 Smilefjes-sjekken")
st.caption("Sjekk hygienen på spisesteder nær deg. Data fra Mattilsynet.")

# --- API-FUNKSJON ---
@st.cache_data(ttl=3600) # HUSK: Cache data i 1 time så vi ikke maser på Mattilsynet
def hent_data(sokeord):
    # Dette er det åpne API-et til Mattilsynet (via Difi)
    url = "https://hotell.difi.no/api/json/mattilsynet/smilefjes/tilsyn"
    
    # Sjekk om det er postnummer (tall) eller sted (tekst)
    params = {'pagesize': 100} # Henter de 100 nyeste treffene
    
    if sokeord.isdigit() and len(sokeord) == 4:
        params['postnr'] = sokeord
    else:
        params['poststed'] = sokeord.upper() # API-et liker STORE BOKSTAVER
        
    try:
        r = requests.get(url, params=params)
        data = r.json().get('entries', [])
        return data
    except:
        return []

# --- HJELPEFUNKSJONER ---
def get_fjes(karakter):
    # 0 = Smilefjes, 1 = Strekmunn, 2 = Surmunn, 3 = Alvorlig
    if karakter == '0': return "🟢"
    elif karakter == '1': return "😐"
    elif karakter == '2': return "🔴"
    elif karakter == '3': return "💀"
    return "❓"

def format_dato(dato_str):
    # Gjør om "ddMMyyyy" til "dd.mm.yyyy"
    if len(dato_str) == 8:
        return f"{dato_str[:2]}.{dato_str[2:4]}.{dato_str[4:]}"
    return dato_str

# --- SØKEFELT ---
sok = st.text_input("Søk på Poststed eller Postnummer:", placeholder="F.eks. Lillestrøm eller 2000")

if sok:
    data = hent_data(sok)
    
    if not data:
        st.warning(f"Fant ingen tilsyn for '{sok}'. Prøv et annet sted.")
    else:
        # Konverter til Pandas for enklere sortering
        df = pd.DataFrame(data)
        
        # Vi vil sortere slik at nyeste tilsyn kommer først
        # Datoformatet i APIet er litt rart (ddMMyyyy), så vi må trikse litt for å sortere riktig
        df['dato_sort'] = pd.to_datetime(df['dato'], format='%d%m%Y', errors='coerce')
        df = df.sort_values(by='dato_sort', ascending=False)

        st.success(f"Fant {len(df)} tilsyn i {sok.capitalize()}!")
        
        # DEL I TO KOLONNER: BRA vs DÅRLIG
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🟢 De flinke (Siste tilsyn)")
            st.caption("Steder med smilefjes (0)")
            
            # Filtrer ut de som har karakter 0
            bra_steder = df[df['total_karakter'] == '0']
            
            for index, row in bra_steder.iterrows():
                navn = row['navn']
                dato = format_dato(row['dato'])
                adr = row['adrlinje1']
                
                with st.expander(f"🟢 {navn}"):
                    st.write(f"📅 **Dato:** {dato}")
                    st.write(f"📍 **Adresse:** {adr}")
                    st.write("✅ Alt i orden!")

        with col2:
            st.subheader("⚠️ OBS-listen")
            st.caption("Steder med mangler (1, 2 eller 3)")
            
            # Filtrer ut de som IKKE er 0
            obs_steder = df[df['total_karakter'] != '0']
            
            if obs_steder.empty:
                st.info("Ingen nylige anmerkninger funnet her! 👏")
            else:
                for index, row in obs_steder.iterrows():
                    navn = row['navn']
                    karakter = row['total_karakter']
                    ikon = get_fjes(karakter)
                    dato = format_dato(row['dato'])
                    
                    # Rød boks for å advare
                    with st.expander(f"{ikon} {navn}", expanded=True):
                        st.error(f"Karakter: {karakter}")
                        st.write(f"📅 **Dato:** {dato}")
                        st.write(f"📍 **Adresse:** {row['adrlinje1']}")
                        if karakter == '1':
                            st.write("😐 Mindre mangler (Hensynet til regelverk ivaretatt)")
                        elif karakter == '2':
                            st.write("🔴 Brudd på regelverk!")
                        elif karakter == '3':
                            st.write("💀 Alvorlig mangel / Stengt!")
