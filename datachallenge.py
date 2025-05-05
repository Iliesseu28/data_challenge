import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------- CONFIGURATION ----------------------------
st.set_page_config(
    page_title="Louis Vuitton - Étude Métiers Industriels",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------- CHARGEMENT DES DONNÉES ----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('Data_challenge.xlsx')
        return df
    except Exception as e:
        st.error(f"Erreur de chargement des données : {str(e)}")
        return None

df = load_data()
if df is None:
    st.stop()

# ---------------------------- FONCTIONS UTILITAIRES ----------------------------
def plot_cross_tab(col_x, col_y, title):
    """Crée un graphique à barres groupées à partir d'une table croisée"""
    try:
        ct = pd.crosstab(df_filtered[col_x], df_filtered[col_y], normalize='index') * 100
        fig = px.bar(
            ct, 
            barmode='group', 
            title=title,
            labels={'value': 'Pourcentage (%)', 'variable': ''},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)
    except KeyError as e:
        st.error(f"Colonne manquante : {str(e)}")
    except Exception as e:
        st.error(f"Erreur de génération du graphique : {str(e)}")

# ---------------------------- PRÉSENTATION DES DONNÉES ----------------------------
st.title("👜 Étude d'Attractivité des Métiers Industriels - Louis Vuitton")

# En-tête avec logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Louis_Vuitton_logo_and_wordmark.svg/langfr-250px-Louis_Vuitton_logo_and_wordmark.svg.png", 
             width=150)

with col2:
    st.markdown("""
    **Objectif** :  
    Analyser la perception des métiers industriels et Supply Chain dans le secteur du luxe,
    identifier les freins à l'attractivité et comprendre les attentes des jeunes talents.
    """)

# Métriques clés
st.markdown("---")
st.subheader("📊 Aperçu de l'Échantillon")
total = len(df)
filieres = df['Filière'].nunique()

m1, m2, m3 = st.columns(3)
m1.metric("Total répondants", total)
m2.metric("Filières représentées", filieres)
m3.metric("Niveaux d'études", df["Niveau d'études"].nunique())

# Graphiques de répartition
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(df, names='Filière', title='Répartition par filière',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(df, x="Niveau d'études", title='Répartition par niveau d\'études',
                       color_discrete_sequence=['#2A9D8F'])
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------- FILTRES ----------------------------
with st.sidebar:
    st.header("🔎 Filtres")
    filiere = st.multiselect("Filière", options=df['Filière'].unique())
    niveau = st.multiselect("Niveau d'études", options=df["Niveau d'études"].unique())

# Application des filtres
df_filtered = df.copy()
if filiere:
    df_filtered = df_filtered[df_filtered['Filière'].isin(filiere)]
if niveau:
    df_filtered = df_filtered[df_filtered["Niveau d'études"].isin(niveau)]

# ---------------------------- ANALYSE QUANTITATIVE ----------------------------
st.markdown("---")
st.header("📈 Analyse Thématique")

tabs = st.tabs(["Perception des Métiers", "Attractivité", "Freins", "Leviers"])

with tabs[0]:
    plot_cross_tab('Filière', 'Niveau de connaissance', 'Connaissance par filière')
    plot_cross_tab("Niveau d'études", 'Perception des métiers', 'Perception par niveau')

with tabs[1]:
    plot_cross_tab('Filière', 'Intérêt pour le luxe', 'Intérêt par filière')
    plot_cross_tab("Niveau d'études", 'Opportunités de carrière', 'Opportunités par niveau')

with tabs[2]:
    plot_cross_tab('Filière', 'Raisons de ne pas postuler', 'Freins principaux')
    plot_cross_tab("Niveau d'études", 'A priori négatifs', 'A priori par niveau')

with tabs[3]:
    plot_cross_tab('Filière', 'Motivations', 'Motivations par filière')
    plot_cross_tab("Niveau d'études", 'Initiatives motivantes', 'Initiatives par niveau')

# ------------------ SECTION DONNÉES QUALITATIVES ------------------

st.header("Données qualitatives : Interviews et synthèse")

# Dictionnaire des profils et interviews
profils = {
    "Émilie, 20 ans, BAC Pro Maintenance": {
        "contexte": "Émilie termine son bac pro et hésite à postuler dans le luxe",
        "objectifs": "Comprendre les freins des profils techniques non diplômés du supérieur",
        "interview": [
            "En CFA on nous parle jamais du luxe J’pensais qu’ils prenaient que des ingénieurs Un prof m’a dit que LV recrute des techniciens mais j’ose pas Si y’avait des portes ouvertes dans leurs ateliers j’irais",
            "Mon stage chez un sous-traitant auto c’était que de la routine Si LV propose des formations pour monter en compétences ça m’motiverait"
        ]
    },
    "Raj, 24 ans, Master Logistique (Inde)": {
        "contexte": "Raj cherche un stage en Europe et s’interroge sur le luxe",
        "objectifs": "Explorer l’attractivité internationale des métiers Supply Chain",
        "interview": [
            "En Inde Louis Vuitton est un rêve Mais je ne savais pas qu’ils avaient des usines en Europe Leur site indien ne mentionne pas ces métiers",
            "Si LV organisait des webinaires en anglais pour expliquer leurs défis logistiques globaux je postulerais Mais leurs offres sont trop franco françaises"
        ]
    },
    "Hugo, 28 ans, reconversion tech": {
        "contexte": "Hugo quitte la tech pour se rapprocher de l’artisanat",
        "objectifs": "Capter l’intérêt des profils en reconversion",
        "interview": [
            "J’ai démissionné d’une startup pour retrouver du concret LV m’intéresse car ils mélangent artisanat et industrie Mais comment postuler sans expérience luxe",
            "Leurs offres demandent 5 ans d’expérience en maroquinerie Pourquoi pas des programmes pour reconvertis motivés"
        ]
    },
    "Fatima, 22 ans, BTS Qualité (handicap)": {
        "contexte": "Fatima cherche une entreprise inclusive pour son alternance",
        "objectifs": "Évaluer l’accessibilité des métiers industriels",
        "interview": [
            "J’ai peur que les ateliers de LV ne soient pas adaptés aux fauteuils roulants Leur site parle de diversité mais montre t il des employés en situation de handicap",
            "Si LV collaborait avec mon école pour aménager des postes ça montrerait un vrai engagement"
        ]
    },
    "Nathan, 26 ans, entrepreneur upcycling": {
        "contexte": "Nathan crée des vêtements à partir de déchets industriels",
        "objectifs": "Explorer les synergies entre luxe et économie circulaire",
        "interview": [
            "LV a un programme de récupération de chutes de cuir mais c’est confidentiel Pourquoi ne pas en faire un argument pour attirer des profils écolos comme moi",
            "Travailler chez eux pour repenser leur supply chain en mode zéro déchet Oui mais seulement s’ils ont une vraie volonté de changer"
        ]
    },
    "Lise, 19 ans, Licence design mode": {
        "contexte": "Lise grandit dans un atelier familial et méprise l’industrie",
        "objectifs": "Comprendre le clivage artisanat vs production de masse",
        "interview": [
            "Mon père répare des sacs LV vintage Il dit Avant c’était fait pour durer Maintenant c’est de la production en série",
            "Si LV m’expliquait comment ils forment leurs artisans et préservent la qualité je reconsidererais Mais j’ai peur que l’industrie tue le savoir faire"
        ]
    },
    "Marco, 30 ans, Livreur en reprise d’études": {
        "contexte": "Marco reprend un BTS Logistique après une carrière dans la restauration",
        "objectifs": "Capter les attentes des profils non traditionnels",
        "interview": [
            "J’ai postulé chez Amazon mais leurs entrepôts sont des mouroirs LV j’imagine que c’est mieux Mais comment le savoir Y’a rien sur Glassdoor",
            "Si LV proposait des stages découverte pour adultes en reconversion j’serais preneur Mais leurs offres s’adressent aux moins de 25 ans"
        ]
    },
    "Aïda, 27 ans, consultante digital nomade": {
        "contexte": "Aïda travaille à distance et s’intéresse aux supply chains connectées",
        "objectifs": "Attirer les profils tech adeptes de flexibilité",
        "interview": [
            "Je pourrais optimiser leurs flux depuis Bali mais LV a l’air trop rigide Leur mention présentiel obligatoire dans les offres me refroidit",
            "S’ils digitalisaient leurs processus et permettaient le télétravail partiel je les verrais comme un employeur innovant"
        ]
    },
    "Thomas, 35 ans, reconversion professionnelle": {
        "contexte": "Thomas quitte la construction pour chercher un métier stable",
        "objectifs": "Comprendre l’attrait des métiers industriels pour les profils matures",
        "interview": [
            "À mon âge je cherche la stabilité LV est une entreprise solide mais j’ai l’impression qu’ils privilégient les jeunes diplômés",
            "Si LV communiquait sur les parcours internes genre Devenez chef d’atelier en 5 ans ça donnerait espoir aux trentenaires comme moi"
        ]
    },
    "Zoé, 18 ans, Lycéenne STI2D": {
        "contexte": "Zoé choisit son orientation post bac",
        "objectifs": "Capter les jeunes talents dès le lycée",
        "interview": [
            "En cours on visite des usines automobiles jamais des ateliers de luxe Si LV organisait des journées Découverte métiers pour lycéens je m’inscrirais",
            "Mes potes pensent que l’industrie c’est pour les garçons Si LV montrait des femmes ingénieures ou cheffes d’atelier ça casserait les clichés"
        ]
    }
}

# Synthèse/conseils pour Louis Vuitton
synthese = """
Les interviews révèlent un manque d’information sur les métiers industriels et supply chain chez Louis Vuitton, des freins liés à l’image élitiste et à l’accessibilité, et une forte attente de preuves concrètes d’engagement (RSE, diversité, formation, mobilité interne). 
Conseils principaux :
- Diversifier la communication RH, cibler les lycées pros, CFA, profils en reconversion, personnes en situation de handicap et talents internationaux
- Organiser des journées portes ouvertes, visites virtuelles, webinaires et stages découverte pour rendre les métiers concrets
- Publier des résultats concrets sur la durabilité, l’économie circulaire, l’accessibilité et la diversité, avec des témoignages d’employés
- Développer des programmes spécifiques pour les reconvertis, adultes en reprise d’études et profils internationaux, avec formation interne et mentorat
- Mettre en avant l’innovation, la digitalisation, la collaboration entre métiers et la dimension internationale de la supply chain
"""

# Sélection du profil
profil_choisi = st.selectbox(
    "Sélectionnez un profil pour lire son interview",
    list(profils.keys())
)

# Affichage du contenu de l'interview
st.subheader(f"Profil : {profil_choisi}")
st.write(f"Contexte : {profils[profil_choisi]['contexte']}")
st.write(f"Objectif : {profils[profil_choisi]['objectifs']}")
st.write("Interview :")
for phrase in profils[profil_choisi]['interview']:
    st.write(f"- {phrase}")

st.markdown("---")
st.subheader("Synthèse et conseils pour Louis Vuitton")
st.write(synthese)

# ---------------------------- SYNTHÈSE ----------------------------
st.markdown("---")
st.success("""
**🔍 Principaux Enseignements** :
- Forte méconnaissance des métiers industriels chez 68% des répondants
- Attentes fortes sur la formation continue et l'impact RSE
- Freins culturels persistants (élitisme perçu, manque de diversité)

**🚀 Recommandations Stratégiques** :
1. Programme « Découverte Métiers » avec visites virtuelles
2. Plateforme de mentorat collaboratif
3. Campagne de communication ciblant les lycées techniques
""")

# ---------------------------- FOOTER ----------------------------
st.markdown("---")
st.caption("""
*Étude réalisée par Ilias Khafague - Données collectées en 2025*  
*© 2025 Louis Vuitton - Données confidentielles*
""")
