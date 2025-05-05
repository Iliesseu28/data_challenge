import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------- CONFIGURATION ----------------------------
st.set_page_config(
    page_title="Louis Vuitton - Attractivité Métiers Industriels", 
    layout="wide",
    page_icon="👜",
    initial_sidebar_state="expanded"
)

# ---------------------------- VARIABLES PERSONNALISABLES ----------------------------
COL_AGE = "Age"
COL_GENRE = "Genre" 
COL_PAYS = "Pays"
COL_FILIERE = "Filière"
COL_NIVEAU = "Niveau d'études"
COL_CONNAISSANCE = "Niveau de connaissance"
COL_FREINS = "Raisons de ne pas postuler"
COL_INITIATIVES = "Initiatives motivantes"
COL_INTERET = "Intérêt pour le luxe"

# ---------------------------- CHARGEMENT DONNÉES ----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('Data_challenge.xlsx')
        required_columns = [COL_FILIERE, COL_NIVEAU]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.error(f"Colonnes manquantes: {', '.join(missing)}")
            return None
        return df
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return None

df = load_data()
if df is None:
    st.stop()

# ---------------------------- PRÉSENTATION DONNÉES ----------------------------
st.title("👜 Louis Vuitton - Étude d'Attractivité des Métiers Industriels")
st.markdown("---")

# Métriques clés
total = len(df)
age_info = df[COL_AGE].mean() if COL_AGE in df.columns else "Non disponible"
genre_info = (df[COL_GENRE].value_counts(normalize=True).get('Femme', 0)*100).round(1) if COL_GENRE in df.columns else "Non disponible"

col1, col2, col3 = st.columns(3)
col1.metric("Total répondants", total)
col2.metric("Âge moyen", f"{age_info:.1f} ans" if isinstance(age_info, float) else age_info)
col3.metric("Part de femmes", f"{genre_info}%" if isinstance(genre_info, float) else genre_info)

# ---------------------------- FILTRES ----------------------------
with st.sidebar:
    st.header("🔎 Filtres")
    filieres = st.multiselect("Filière", options=df[COL_FILIERE].unique())
    niveaux = st.multiselect("Niveau d'études", options=df[COL_NIVEAU].unique())

df_filtered = df.copy()
if filieres:
    df_filtered = df_filtered[df_filtered[COL_FILIERE].isin(filieres)]
if niveaux:
    df_filtered = df_filtered[df_filtered[COL_NIVEAU].isin(niveaux)]

# ---------------------------- VISUALISATIONS ----------------------------
def plot_crosstab(col_x, col_y, title):
    ct = pd.crosstab(df_filtered[col_x], df_filtered[col_y], normalize='index')*100
    fig = px.bar(ct, barmode='group', title=title, labels={'value':'%'})
    st.plotly_chart(fig, use_container_width=True)

st.header("📊 Analyse Thématique")

tab1, tab2, tab3 = st.tabs(["Connaissance", "Freins", "Leviers"])
with tab1:
    plot_crosstab(COL_FILIERE, COL_CONNAISSANCE, "Connaissance des métiers par filière")
with tab2:
    plot_crosstab(COL_NIVEAU, COL_FREINS, "Freins principaux par niveau d'études")
with tab3:
    plot_crosstab(COL_FILIERE, COL_INITIATIVES, "Leviers d'attractivité par filière")

# ---------------------------- ANALYSE QUALITATIVE ----------------------------
st.markdown("---")
st.header("🎤 Témoignages Clés")

profils = {
    "Émilie (Bac Pro)": {
        "contexte": "Étudiante en maintenance prête à entrer sur le marché du travail",
        "citations": [
            "Je ne savais pas que LV recrutait des techniciens...",
            "Une visite d'atelier changerait complètement ma perception !"
        ]
    },
    "Raj (Master)": {
        "contexte": "Diplômé international en logistique",
        "citations": [
            "Les offres en anglais seraient essentielles pour attirer les talents étrangers",
            "La dimension internationale des supply chains n'est pas assez mise en avant"
        ]
    }
}

selected_profile = st.selectbox(
    "Sélectionner un profil type",
    options=list(profils.keys()),
    index=0  # Garantit une sélection valide par défaut
)

if selected_profile in profils:
    st.subheader(f"Profil : {selected_profile}")
    st.write(f"**Contexte** : {profils[selected_profile]['contexte']}")
    st.write("**Citations clés** :")
    for citation in profils[selected_profile]['citations']:
        st.markdown(f"- *{citation}*")
else:
    st.error("Profil non trouvé")

# ---------------------------- SYNTHÈSE ----------------------------
st.markdown("---")
st.header("💡 Recommandations Stratégiques")
st.markdown("""
1. **Campagne de sensibilisation** dans les lycées professionnels et CFA
2. **Programme de visites virtuelles** des sites de production
3. **Portail de recrutement multilingue** avec témoignages vidéo
4. **Parcours de formation intégrés** pour les reconversions professionnelles
""")

# ---------------------------- FOOTER ----------------------------
st.markdown("---")
st.caption("© 2023 - Étude réalisée par [Votre Nom] - Données confidentielles")
 