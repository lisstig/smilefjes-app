import streamlit as st

# --- KONFIGURASJON ---
st.set_page_config(page_title="Smilefjes-sjekken", page_icon="🙂")

st.title("🙂 Smilefjes-sjekken")
st.caption("Snarvei til Mattilsynets tilsynsresultater.")

st.info("ℹ️ Obs: Mattilsynet har stengt det åpne API-et sitt. Denne appen hjelper deg derfor å søke direkte i deres offisielle database.")

# --- SØKEFELT ---
sok = st.text_input("Hvor vil du spise? (Kommune eller navn):", placeholder="F.eks. Lillestrøm eller Pizzabakeren")

if sok:
    # Vi lager en smart lenke direkte til Mattilsynets søk
    # %20 er koden for mellomrom i nettadresser
    sok_ryddet = sok.strip()
    link = f"https://smilefjes.mattilsynet.no/sok?q={sok_ryddet}"
    
    st.success(f"Klar til å søke etter **'{sok_ryddet}'**!")
    
    # Stor, tydelig knapp
    st.link_button(f"🔍 Se resultater for '{sok_ryddet}' hos Mattilsynet", link, type="primary")
    
    st.markdown("---")
    st.caption("Du blir videresendt til smilefjes.mattilsynet.no")

else:
    # Viser noen eksempler før man søker
    st.markdown("---")
    st.subheader("Eller prøv en av disse:")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.link_button("📍 Lillestrøm", "https://smilefjes.mattilsynet.no/kommune/lillestrom")
    with c2:
        st.link_button("📍 Oslo", "https://smilefjes.mattilsynet.no/kommune/oslo")
    with c3:
        st.link_button("📍 Strømmen", "https://smilefjes.mattilsynet.no/sok?q=Strømmen")
