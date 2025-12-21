import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup as bs
from requests import get
import logging
import os

logging.basicConfig(level=logging.WARNING)

# ================= TITRE =================
st.markdown("<h1 style='text-align: center;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)
st.markdown("Application de web scraping – Dakar-Auto (Véhicules, Motos & Locations)")

# ================= FONCTIONS =================
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def load(dataframe, title, key1, key2):
    st.write(f"Dimensions : {dataframe.shape}")
    st.dataframe(dataframe)
    st.download_button(
        "Télécharger CSV",
        convert_df(dataframe),
        f"{title}.csv",
        "text/csv",
        key=key2
    )

def scrape_listing(url, type_):
    soup = bs(get(url).text, "html.parser")

    if type_ == "vehicle":
        containers = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")
    else:
        containers = soup.find_all("div", class_="listing-card__content p-2")

    data = []
    for c in containers:
        try:
            title = c.find("h2").text.split()
            marque = title[0]
            annee = int(title[-1])
            prix = int(c.find("h3").text.replace(" F CFA", "").replace("\u202f", ""))

            if type_ == "vehicle":
                infos = c.find_all("li")
                kilometrage = int(infos[1].text.replace(" km", "").replace("\u202f", ""))
                boite = infos[2].text
                carburant = infos[3].text
                data.append({
                    "marque": marque,
                    "annee": annee,
                    "prix": prix,
                    "adresse": "Dakar",
                    "kilometrage": kilometrage,
                    "boite": boite,
                    "carburant": carburant,
                    "proprietaire": "Inconnu"
                })

            elif type_ == "moto":
                infos = c.find_all("li")
                kilometrage = int(infos[1].text.replace(" km", "").replace("\u202f", ""))
                adresse = c.find("div", class_="col-12 entry-zone-address").text.strip()
                data.append({
                    "marque": marque,
                    "annee": annee,
                    "prix": prix,
                    "adresse": adresse,
                    "kilometrage": kilometrage,
                    "proprietaire": "Inconnu"
                })

            else:  # location
                adresse = c.find("div", class_="col-12 entry-zone-address").text.strip()
                proprietaire = c.find("span", class_="owner")
                proprietaire = proprietaire.text.strip() if proprietaire else "Inconnu"
                data.append({
                    "marque": marque,
                    "annee": annee,
                    "prix": prix,
                    "adresse": adresse,
                    "proprietaire": proprietaire
                })

        except Exception as e:
            logging.warning(f"Erreur scraping : {e}")

    return pd.DataFrame(data)

# ================= PARAMETRES =================
Pages = st.sidebar.selectbox("Nombre de pages à scraper", list(np.arange(2, 50)))

# ================= MENU BOUTONS =================
st.markdown("### Menu")

col1, col2, col3, col4 = st.columns(4)

with col1:
    btn_scrape = st.button("🔍 Scrape Data")
with col2:
    btn_download = st.button("📥 Download Data")
with col3:
    btn_dashboard = st.button("📊 Dashboard")
with col4:
    btn_evaluate = st.button("⭐ Evaluate App")

# ================= NAVIGATION =================
if "page" not in st.session_state:
    st.session_state.page = None

if btn_scrape:
    st.session_state.page = "scrape"
if btn_download:
    st.session_state.page = "download"
if btn_dashboard:
    st.session_state.page = "dashboard"
if btn_evaluate:
    st.session_state.page = "evaluate"

# ================= LOGIQUE =================
if st.session_state.page == "scrape":

    Vehicles_data = pd.DataFrame()
    Motocycle_data = pd.DataFrame()
    Locations_data = pd.DataFrame()

    progress = st.progress(0.0)

    for p in range(1, Pages + 1):
        Vehicles_data = pd.concat([
            Vehicles_data,
            scrape_listing(f"https://dakar-auto.com/senegal/voitures-4?page={p}", "vehicle")
        ], ignore_index=True)

        Motocycle_data = pd.concat([
            Motocycle_data,
            scrape_listing(f"https://dakar-auto.com/senegal/motos-and-scooters-3?page={p}", "moto")
        ], ignore_index=True)

        Locations_data = pd.concat([
            Locations_data,
            scrape_listing(f"https://dakar-auto.com/senegal/location-de-voitures-19?page={p}", "location")
        ], ignore_index=True)

        progress.progress(p / Pages)

    Vehicles_data.to_csv("Vehicles_data.csv", index=False)
    Motocycle_data.to_csv("Motocycles_data.csv", index=False)
    Locations_data.to_csv("Locations_data.csv", index=False)

    load(Vehicles_data, "Vehicles_data", "1", "101")
    load(Motocycle_data, "Motocycles_data", "2", "102")
    load(Locations_data, "Locations_data", "3", "103")

elif st.session_state.page == "download":

    if all(os.path.exists(f) for f in [
        "Vehicles_data.csv",
        "Motocycles_data.csv",
        "Locations_data.csv"
    ]):
        load(pd.read_csv("Vehicles_data.csv"), "Vehicles_data", "1", "101")
        load(pd.read_csv("Motocycles_data.csv"), "Motocycles_data", "2", "102")
        load(pd.read_csv("Locations_data.csv"), "Locations_data", "3", "103")
    else:
        st.error("Veuillez d'abord scraper les données.")

elif st.session_state.page == "dashboard":

    if all(os.path.exists(f) for f in [
        "Vehicles_data.csv",
        "Motocycles_data.csv",
        "Locations_data.csv"
    ]):

        df1 = pd.read_csv("Vehicles_data.csv")
        df2 = pd.read_csv("Motocycles_data.csv")
        df3 = pd.read_csv("Locations_data.csv")

        c1, c2, c3 = st.columns(3)

        with c1:
            plt.figure()
            df1.marque.value_counts()[:5].plot(kind="bar")
            plt.title("Top 5 véhicules")
            st.pyplot(plt.gcf())

        with c2:
            plt.figure()
            df2.marque.value_counts()[:5].plot(kind="bar")
            plt.title("Top 5 motos")
            st.pyplot(plt.gcf())

        with c3:
            plt.figure()
            df3.marque.value_counts()[:5].plot(kind="bar")
            plt.title("Top 5 locations")
            st.pyplot(plt.gcf())

    else:
        st.error("Veuillez d'abord scraper les données.")

elif st.session_state.page == "evaluate":

    st.markdown("<h3 style='text-align: center;'>Give your Feedback</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('[Kobo Evaluation Form](https://ee.kobotoolbox.org/x/bovbBGz7)')
    with col2:
        st.markdown('[Google Forms Evaluation](https://docs.google.com/forms/d/e/XXXXXXXXX/viewform)')
