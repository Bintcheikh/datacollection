import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components




st.markdown("<h1 style='text-align: center; color: black;'>MY BEST DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app performs webscraping of data from dakar-auto over multiples pages. And we can also
download scraped data from the app directly without scraping them.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Expat-Dakar](https://www.expat-dakar.com/) -- [Dakar-Auto](https://dakar-auto.com/senegal/voitures-4).
""")


# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Web scraping of Vehicles data on expat-dakar
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def load(dataframe, title, key, key1) :
    # Créer 3 colonnes avec celle du milieu plus large
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(title, key1):
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)

            csv = convert_df(dataframe)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='Data.csv',
                mime='text/csv',
                key = key)
# def load(dataframe, title, key, key1) :
    
#     st.markdown("""
#     <style>
#     div.stButton {text-align:center}
#     </style>""", unsafe_allow_html=True)
#     # define some styles rely to the box
#     st.markdown('''<style> .stButton>button {
#         font-size: 12px;
#         height: 3em;
#         width: 25em;
#     }</style>''', unsafe_allow_html=True)
    
#     if st.button(title,key1):
#         # st.header(title)

#         st.subheader('Display data dimension')
#         st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
#         st.dataframe(dataframe)

#         csv = convert_df(dataframe)

#         st.download_button(
#             label="Download data as CSV",
#             data=csv,
#             file_name='Data.csv',
#             mime='text/csv',
#             key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction for web scraping vehicle data
def load_vehicle_data(mul_page):
    # create a empty dataframe df
    df = pd.DataFrame()
    # loop over pages indexes
    for p in range(1, int(mul_page)+1): 
        url = f'https://dakar-auto.com/senegal/voitures-4?&page={p}'
        # get the html code of the page using the get function requests
        res = get(url)
        # store the html code in a beautifulsoup objet with a html parser (a parser allows to easily navigate through the html code)
        soup = bs(res.text , 'html.parser')
        # get all containers that contains the informations of each car
        containers = soup.find_all('div', class_ = 'listings-cards__list-item mb-md-3 mb-3')
        # scrape data from all the containers
        data = []
        for container in containers: 
            try:
                # scrape the car brand, model and the year
                gen_inf = container.find('h2', class_ ='listing-card__header__title mb-md-2 mb-0').text.strip().split()
                # get the brand
                brand = gen_inf[0]
                # get the model
                model = ' '.join( gen_inf[1: len(gen_inf) - 1])
                # get the year
                year = gen_inf[-1]
                # Scrape the reference, kilometer driven, fuel type and gearbox type
                gen_inf2 = container.find_all('li', class_  = 'listing-card__attribute list-inline-item')
                
                # get reference
                reference = gen_inf2[0].text.strip().replace("Ref. ", "")
                # get kilometer driven
                kms_driven = gen_inf2[1].text.strip().replace(' km', '')
                # get gearbox type
                gearbox = gen_inf2[2].text.strip()
                # get fuel type
                fuel_type= gen_inf2[3].text.strip()
        
                # scrape the price
                price = container.find('h3', class_ = 'listing-card__header__price font-weight-bold text-uppercase mb-0').text
                price = price.strip().replace('\u202f', '').replace(' F CFA', '')
                dic = {'brand': brand, 
                      'model': model, 
                      'year':year, 
                      'reference': reference, 
                      'kms_driven':kms_driven, 
                      'gearbox': gearbox, 
                      'fuel_type':fuel_type, 
                      'price':price}
                data.append(dic)
            except: 
                pass
        
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True) 
    return df   

def load_motocycle_data(mul_page):
    # create a empty dataframe df
    df=pd.DataFrame()
    # loop over pages indexes
    for page in range (1,int(mul_page)+1):
        url=f'https://dakar-auto.com/senegal/motos-and-scooters-3?&page={page}'
        #get the html code of the page using the get function reauests
        res=get(url)
        # store the html code in a beautifulsoup object zith a html panser
        soup=bs(res.text,'html.parser')
        # get all containers that contains the informations of each car
        containers=soup.find_all('div',class_='listing-card__content p-2')
        data=[]
        for container in containers:
            try:
    
                # scrape the moto brand, model and the year
                gen_inf=container.find ('h2',class_='listing-card__header__title mb-md-2 mb-0').text.strip().split()
    
                # get the brand
                brand=gen_inf[0]
                # get the model
                model=' '.join(gen_inf[1:-1])
    
                # get the year
                year=gen_inf[-1]
    
                # Scrape the reference, kilometer driven, address and price
                gen_inf2=container.find_all('li', class_='listing-card__attribute list-inline-item')
                # get reference
                reference=gen_inf2[0].text.strip().replace("Ref. ", "")
                # get kilometer driven
                kilometers=gen_inf2[1].text.strip().replace(" km", "")
                # scrape address
                address=container.find('div',class_='col-12 entry-zone-address').text.strip().replace("\n", "")
                # scrape the price
                price=container.find('h3',class_='listing-card__header__price font-weight-bold text-uppercase mb-0').text.strip().replace("\u202f", "").replace(" F CFA", "")
    
    
                dic={'brand': brand,
                      'model':model,
                      'year':year,
                      'reference':reference,
                      'kms_driven':kilometers,
                      'address':address,
                      'price':price}
    
                data.append(dic)
            except:
                pass
        DF=pd.DataFrame(data)
        df=pd.concat([df,DF], axis=0 ).reset_index(drop=True)

    return df   


st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 600)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Evaluate the App'])



add_bg_from_local('img_file3.jpg') 

local_css('style.css')  

if Choices=='Scrape data using beautifulSoup':

    Vehicles_data_mul_pag = load_vehicle_data(Pages)
    Motocycle_data_mul_pag = load_motocycle_data(Pages)
    
    load(Vehicles_data_mul_pag, 'Vehicles data', '1', '101')
    load(Motocycle_data_mul_pag, 'Motocycle data', '2', '102')

elif Choices == 'Download scraped data': 
    Vehicles = pd.read_csv('Vehicles_data.csv')
    Motocycles = pd.read_csv('Motocycles_data.csv') 

    load(Vehicles, 'Vehicles data', '1', '101')
    load(Motocycles, 'Motocycles data', '2', '102')

elif  Choices == 'Dashbord of the data': 
    df1 = pd.read_csv('vehicles_clean_data.csv')
    df2 = pd.read_csv('motocycles_clean_data.csv')

    col1, col2= st.columns(2)

    with col1:
        plot1= plt.figure(figsize=(11,7))
        color = (0.2, # redness
                 0.4, # greenness
                 0.2, # blueness
                 0.6 # transparency
                 )
        plt.bar(df1.marque.value_counts()[:5].index, df1.marque.value_counts()[:5].values, color = color)
        plt.title('cinq marque de vehicules les plus vendus')
        plt.xlabel('marque')
        st.pyplot(plot1)
2
    with col2:
        plot2 = plt.figure(figsize=(11,7))
        color = (0.5, # redness
         0.7, # greenness
         0.9, # blueness
         0.6 # transparency
         )
        plt.bar(df2.marque.value_counts()[:5].index, df2.marque.value_counts()[:5].values, color = color)
        plt.title('cinq marque de vehicules les plus vendus')
        plt.xlabel('marque')
        st.pyplot(plot2)
    
    col3, col4= st.columns(2)

    with col3:
        plot3= plt.figure(figsize=(11,7))
        sns.lineplot(data=df1, x="annee", y="prix", hue="etat")
        plt.title('Variation du prix suivant les années des catégories de vehicules')
        st.pyplot(plot3)

    with col4:
        plot4 = plt.figure(figsize=(11,7))
        sns.lineplot(data=df2, x="annee", y="prix", hue="etat")
        plt.title('Variation du prix suivant les années des catégories de motos')
        st.pyplot(plot4)



else :
    # components.html("""
    # <iframe src="https://ee.kobotoolbox.org/i/y3pfGxMz" width="800" height="1100"></iframe>
    # """,height=1100,width=800)
    st.markdown("<h3 style='text-align: center;'>Give your Feedback</h3>", unsafe_allow_html=True)

    # centrer les deux boutons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kobo Evaluation Form"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://ee.kobotoolbox.org/i/y3pfGxMz">',
                unsafe_allow_html=True
            )

    with col2:
        if st.button("Google Forms Evaluation"):
            st.markdown(
                '<meta http-equiv="refresh" content="0; url=https://docs.google.com/forms/d/e/XXXXXXXXX/viewform?usp=sf_link">',
                unsafe_allow_html=True
            )







 











