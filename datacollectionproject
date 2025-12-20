import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ================= TITRE =================
st.markdown("<h1 style='text-align: center;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs web scraping of data from Dakar-Auto over multiple pages.
You can also download previously scraped data.
""")

# ================= BACKGROUND =================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ================= CSV CACHE =================
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

# ================= AFFICHAGE DATA =================
def load(dataframe, title, key, key1):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(title, key1):
            st.write(f"Data dimension: {dataframe.shape}")
            st.dataframe(dataframe)

            st.download_button(
                "Download CSV",
                convert_df(dataframe),
                "data.csv",
                "text/csv",
                key=key
            )

# ================= SCRAPING VEHICULES =================
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
                brand = title[0]
                model = " ".join(title[1:-1])
                year = title[-1]

                infos = c.find_all("li")
                reference = infos[0].text.replace("Ref. ", "")
                kms = infos[1].text.replace(" km", "")
                gearbox = infos[2].text
                fuel = infos[3].text

                price = c.find("h3").text.replace(" F CFA", "").replace("\u202f", "")

                data.append({
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "kms_driven": kms,
                    "gearbox": gearbox,
                    "fuel_type": fuel,
                    "price": price
                })
            except:
                pass

        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    return df

# ================= SIDEBAR =================
st.sidebar.header("User Input")
pages = st.sidebar.selectbox("Number of pages", range(2, 50))
choice = st.sidebar.selectbox(
    "Options",
    ["Scrape data", "Download data", "Dashboard", "Evaluate App"]
)

# ================= BACKGROUND (OPTIONNEL) =================
# add_bg_from_local("img_file3.jpg")

# ================= OPTIONS =================
if choice == "Scrape data":
    vehicles = load_vehicle_data(pages)
    load(vehicles, "Show Vehicles Data", "v1", "v2")

elif choice == "Download data":
    vehicles = pd.read_csv("Vehicles_data.csv")
    load(vehicles, "Vehicles CSV", "v3", "v4")

elif choice == "Dashboard":
    df = pd.read_csv("vehicles_clean_data.csv")

    fig = plt.figure(figsize=(10, 5))
    df["brand"].value_counts()[:5].plot(kind="bar")
    plt.title("Top 5 vehicle brands")
    st.pyplot(fig)

else:
    st.markdown("### Give your Feedback")
    if st.button("Kobo Form"):
        st.markdown(
            '<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/i/y3pfGxMz">',
            unsafe_allow_html=True
        )
