import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import matplotlib.pyplot as plt
import numpy as np

# ================= TITRE =================
st.markdown("<h1 style='text-align: center;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)
st.markdown("Application de web scraping – Dakar-Auto (Véhicules & Motos)")

# ================= CACHE CSV =================
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

# ================= AFFICHAGE =================
def load(dataframe, title, key):
    if st.button(title, key):
        st.write(f"Dimensions : {dataframe.shape}")
        st.dataframe(dataframe)

        st.download_button(
            "Télécharger CSV",
            convert_df(dataframe),
            f"{title}.csv",
            "text/csv"
        )

# ================= SCRAPING VÉHICULES =================
def load_vehicle_data(pages):
    df = pd.DataFrame()

    for p in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/voitures-4?page={p}"
        soup = bs(get(url).text, "html.parser")
        containers = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")

        data = []
        for c in containers:
            try:
                title = c.find("h2").text.split()
                marque = title[0]
                annee = title[-1]

                infos = c.find_all("li")
                kilometrage = infos[1].text.replace(" km", "")
                boite = infos[2].text
                carburant = infos[3].text

                prix = c.find("h3").text.replace(" F CFA", "").replace("\u202f", "")

                data.append({
                    "V1_marque": marque,
                    "V2_annee": annee,
                    "V3_prix": prix,
                    "V4_adresse": "Dakar",
                    "V5_kilometrage": kilometrage,
                    "V6_boite_vitesse": boite,
                    "V7_carburant": carburant,
                    "V8_proprietaire": "Inconnu"
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    return df

# ================= SCRAPING MOTOS =================
def load_moto_data(pages):
    df = pd.DataFrame()

    for p in range(1, pages + 1):
        url = f"https://dakar-auto.com/senegal/motos-and-scooters-3?page={p}"
        soup = bs(get(url).text, "html.parser")
        containers = soup.find_all("div", class_="listing-card__content p-2")

        data = []
        for c in containers:
            try:
                title = c.find("h2").text.split()
                marque = title[0]
                annee = title[-1]

                infos = c.find_all("li")
                kilometrage = infos[1].text.replace(" km", "")

                adresse = c.find(
                    "div",
                    class_="col-12 entry-zone-address"
                ).text.strip().replace("\n", "")

                prix = c.find("h3").text.replace(" F CFA", "").replace("\u202f", "")

                data.append({
                    "V1_marque": marque,
                    "V2_annee": annee,
                    "V3_prix": prix,
                    "V4_adresse": adresse,
                    "V5_kilometrage": kilometrage,
                    "V6_proprietaire": "Inconnu"
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    return df

# ================= SIDEBAR =================
st.sidebar.header("Paramètres")
pages = st.sidebar.selectbox("Nombre de pages", range(2, 50))
choice = st.sidebar.selectbox(
    "Options",
    [
        "Scraper véhicules",
        "Scraper motos",
        "Télécharger véhicules",
        "Télécharger motos"
    ]
)

# ================= OPTIONS =================
if choice == "Scraper véhicules":
    with st.spinner("Scraping des véhicules..."):
        vehicles = load_vehicle_data(pages)
        vehicles.to_csv("Vehicles_data.csv", index=False)

    load(vehicles, "Vehicles_data", "v1")

elif choice == "Scraper motos":
    with st.spinner("Scraping des motos..."):
        motos = load_moto_data(pages)
        motos.to_csv("Motos_data.csv", index=False)

    load(motos, "Motos_data", "m1")

elif choice == "Télécharger véhicules":
    try:
        vehicles = pd.read_csv("Vehicles_data.csv")
        load(vehicles, "Vehicles_data", "v2")
    except FileNotFoundError:
        st.error("Veuillez d'abord scraper les véhicules.")

elif choice == "Télécharger motos":
    try:
        motos = pd.read_csv("Motos_data.csv")
        load(motos, "Motos_data", "m2")
    except FileNotFoundError:
        st.error("Veuillez d'abord scraper les motos.")
