import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup as bs
from requests import get
import logging
import os
#def add_bg_from_local(image_file):
   # import base64
    #with open(image_file, "rb") as f:
    #    encoded = base64.b64encode(f.read()).decode()
    #st.markdown(
       # f"""
       # <style>
        #.stApp {{
       #     background-image: url("data:image/jpg;base64,{encoded}");
       #     background-size: cover;
       # }}
       # </style>
        #""",
        #unsafe_allow_html=True
    #)

# ================= APPEL IMAGE DE FOND =================
#current_dir = os.path.dirname(os.path.abspath(__file__))  # dossier du script
#image_path = os.path.join(current_dir, "img_file3.jpg")
#add_bg_from_local(image_path)  # <-- remplace l'ancien add_bg_from_local('img_file3.jpg')

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
    st.download_button("Télécharger CSV", convert_df(dataframe), f"{title}.csv", "text/csv", key=key2)

def scrape_listing(url, type_):
    df = pd.DataFrame()
    soup = bs(get(url).text, "html.parser")
    if type_=="vehicle":
        containers = soup.find_all("div", class_="listings-cards__list-item mb-md-3 mb-3")
    else:
        containers = soup.find_all("div", class_="listing-card__content p-2")
    
    data = []
    for c in containers:
        try:
            title = c.find("h2").text.split()
            marque = title[0]
            annee = int(title[-1])
            prix = int(c.find("h3").text.replace(" F CFA","").replace("\u202f",""))

            if type_=="vehicle":
                infos = c.find_all("li")
                kilometrage = int(infos[1].text.replace(" km","").replace("\u202f",""))
                boite = infos[2].text
                carburant = infos[3].text
                data.append({"marque":marque,"annee":annee,"prix":prix,"adresse":"Dakar",
                             "kilometrage":kilometrage,"boite":boite,"carburant":carburant,"proprietaire":"Inconnu"})
            elif type_=="moto":
                infos = c.find_all("li")
                kilometrage = int(infos[1].text.replace(" km","").replace("\u202f",""))
                adresse = c.find("div", class_="col-12 entry-zone-address").text.strip()
                data.append({"marque":marque,"annee":annee,"prix":prix,"adresse":adresse,"kilometrage":kilometrage,"proprietaire":"Inconnu"})
            else:  # location
                adresse = c.find("div", class_="col-12 entry-zone-address").text.strip()
                proprietaire = c.find("span", class_="owner").text.strip() if c.find("span", class_="owner") else "Inconnu"
                data.append({"marque":marque,"annee":annee,"prix":prix,"adresse":adresse,"proprietaire":proprietaire})
        except Exception as e:
            logging.warning(f"Erreur scraping : {e}")
    return pd.DataFrame(data)

# ================= SIDEBAR =================
st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list(np.arange(2, 50)))
Choices = st.sidebar.selectbox('Options', [
    'Scrape data using beautifulSoup',
    'Download scraped data',
    'Dashboard of the data',
    'Evaluate the App'
])

# ================= BACKGROUND & CSS =================
#add_bg_from_local('img_file3.jpg') 
#local_css('style.css')  

# ================= LOGIQUE =================
if Choices=='Scrape data using beautifulSoup':
    Vehicles_data_mul_pag = pd.DataFrame()
    Motocycle_data_mul_pag = pd.DataFrame()
    Locations_data_mul_pag = pd.DataFrame()
    progress = st.progress(0)
    
    for p in range(1, Pages+1):
        Vehicles_data_mul_pag = pd.concat([Vehicles_data_mul_pag, scrape_listing(f"https://dakar-auto.com/senegal/voitures-4?page={p}", "vehicle")], ignore_index=True)
        Motocycle_data_mul_pag = pd.concat([Motocycle_data_mul_pag, scrape_listing(f"https://dakar-auto.com/senegal/motos-and-scooters-3?page={p}", "moto")], ignore_index=True)
        Locations_data_mul_pag = pd.concat([Locations_data_mul_pag, scrape_listing(f"https://dakar-auto.com/senegal/location-de-voitures-19?page={p}", "location")], ignore_index=True)
        progress.progress(p/Pages)

    Vehicles_data_mul_pag.to_csv("Vehicles_data.csv", index=False)
    Motocycle_data_mul_pag.to_csv("Motocycles_data.csv", index=False)
    Locations_data_mul_pag.to_csv("Locations_data.csv", index=False)

    load(Vehicles_data_mul_pag, 'Vehicles data', '1', '101')
    load(Motocycle_data_mul_pag, 'Motocycle data', '2', '102')
    load(Locations_data_mul_pag, 'Locations data', '3', '103')

elif Choices == 'Download scraped data': 
    if all(os.path.exists(f) for f in ['Vehicles_data.csv','Motocycles_data.csv','Locations_data.csv']):
        Vehicles = pd.read_csv('Vehicles_data.csv')
        Motocycles = pd.read_csv('Motocycles_data.csv')
        Locations = pd.read_csv('Locations_data.csv')
        load(Vehicles, 'Vehicles data', '1', '101')
        load(Motocycles, 'Motocycles data', '2', '102')
        load(Locations, 'Locations data', '3', '103')
    else:
        st.error("Veuillez d'abord scraper les données.")

elif Choices == 'Dashboard of the data': 
    if all(os.path.exists(f) for f in ['Vehicles_data.csv','Motocycles_data.csv','Locations_data.csv']):
        df1 = pd.read_csv('Vehicles_data.csv')
        df2 = pd.read_csv('Motocycles_data.csv')
        df3 = pd.read_csv('Locations_data.csv')

        col1, col2, col3 = st.columns(3)
        with col1:
            plt.figure(figsize=(10,6))
            plt.bar(df1.marque.value_counts()[:5].index, df1.marque.value_counts()[:5].values, color=(0.2,0.4,0.2,0.6))
            plt.title('Top 5 véhicules')
            st.pyplot(plt.gcf())
        with col2:
            plt.figure(figsize=(10,6))
            plt.bar(df2.marque.value_counts()[:5].index, df2.marque.value_counts()[:5].values, color=(0.5,0.7,0.9,0.6))
            plt.title('Top 5 motos')
            st.pyplot(plt.gcf())
        with col3:
            plt.figure(figsize=(10,6))
            plt.bar(df3.marque.value_counts()[:5].index, df3.marque.value_counts()[:5].values, color=(0.9,0.5,0.5,0.6))
            plt.title('Top 5 locations')
            st.pyplot(plt.gcf())

    else:
        st.error("Veuillez d'abord scraper les données pour voir le dashboard.")

else :  # Evaluate
    st.markdown("<h3 style='text-align: center;'>Give your Feedback</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('[Kobo Evaluation Form](https://ee.kobotoolbox.org/i/y3pfGxMz)', unsafe_allow_html=True)
    with col2:
        st.markdown('[Google Forms Evaluation](https://docs.google.com/forms/d/e/XXXXXXXXX/viewform?usp=sf_link)', unsafe_allow_html=True)
