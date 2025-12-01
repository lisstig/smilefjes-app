# 🙂 Smilefjes-sjekken

**Sjekk hygienen på spisesteder nær deg.**

Dette er en enkel web-app som lar deg søke opp kommuner eller postnumre for å se Mattilsynets tilsynsresultater ("Smilefjes-ordningen").

## 🔎 Hva gjør appen?
* **Søk lokalt:** Skriv inn "Lillestrøm" eller "2000" og se status for restauranter i området.
* **Topp & Bunn:** Appen sorterer automatisk spisestedene i to lister:
    * 🟢 **De flinke:** Steder som har alt på stell (Smilefjes).
    * ⚠️ **OBS-listen:** Steder som fikk merknader (Strek- eller Surmunn) ved forrige tilsyn.
* **Detaljer:** Se dato for tilsyn og hva slags karakter de fikk (0, 1, 2 eller 3).

## ℹ️ Datakilder
Appen henter åpne, offentlige data direkte fra **Mattilsynet** (via Difi sitt API).
Dataene oppdateres jevnlig av Mattilsynet.

## 🛠️ Teknisk
Laget med Python og [Streamlit](https://streamlit.io).

---
*Dette er en uoffisiell app laget for å gjøre informasjonen lettere tilgjengelig.*
