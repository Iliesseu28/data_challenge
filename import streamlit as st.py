import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Analyse Métiers LV", layout="wide")

# Chargement des données (à adapter avec ton fichier Excel)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('donnees_sondage.xlsx')  # Remplace par ton chemin de fichier
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# Sidebar pour les filtres
with st.sidebar:
    st.header("Filtres")
    filiere = st.multiselect("Filière d'études", options=df['Q1'].unique())
    niveau_etudes = st.multiselect("Niveau d'études", options=df['Q2'].unique())
    
    # Application des filtres
    if filiere:
        df = df[df['Q1'].isin(filiere)]
    if niveau_etudes:
        df = df[df['Q2'].isin(niveau_etudes)]

# Fonctions de visualisation
def plot_cross_tab(col1, col2, title):
    ct = pd.crosstab(df[col1], df[col2], normalize='index')*100
    fig = px.bar(ct, 
                 barmode='group', 
                 title=title,
                 labels={'value': 'Pourcentage (%)', 'variable': ''})
    st.plotly_chart(fig, use_container_width=True)

def plot_radar_chart(col, title):
    data = df[col].value_counts().reset_index()
    fig = px.line_polar(data, 
                        r='count', 
                        theta=col,
                        line_close=True,
                        title=title)
    st.plotly_chart(fig, use_container_width=True)

# Page principale
st.title("Analyse de l'attractivité des métiers Industrie/Supply Chain")

# Section 1: Croisements filière × connaissances
with st.expander("1. Analyse par filière d'études", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        plot_cross_tab('Q1', 'Q4', 'Connaissance des métiers par filière')
    with col2:
        plot_cross_tab('Q1', 'Q3', 'Intention de postuler par filière')

# Section 2: Analyse des perceptions
with st.expander("2. Perception des métiers"):
    col1, col2 = st.columns(2)
    with col1:
        plot_radar_chart('Q5', 'Adjectifs associés aux métiers')
    with col2:
        plot_cross_tab('Q4', 'Q6', 'Perception des opportunités par niveau de connaissance')

# Section 3: Analyse secteur luxe
with st.expander("3. Analyse spécifique au secteur du luxe"):
    col1, col2, col3 = st.columns(3)
    with col1:
        plot_cross_tab('Q8', 'Q9', 'Perception de la valorisation dans le luxe')
    with col2:
        plot_cross_tab('Q1', 'Q11', 'Motivations par filière')
    with col3:
        plot_cross_tab('Q12', 'Q13', 'Canaux vs Initiatives souhaitées')

# Section 4: Tableau de bord interactif
with st.expander("Exploration des données brutes"):
    st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
    st.download_button(
        label="Télécharger les données filtrées",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='donnees_filtrees.csv',
        mime='text/csv'
    )

# Instructions pour lancer l'app
st.markdown("""
**Comment utiliser cette application :**
1. Installez les dépendances : `pip install streamlit pandas matplotlib seaborn plotly openpyxl`
2. Lancez avec : `streamlit run nom_du_fichier.py`
3. Utilisez les filtres dans la sidebar pour affiner les analyses
""")
