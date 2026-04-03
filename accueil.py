"""
    Page d'accueil :

    Cette page présente, "l'entrepise", l'application, son objectif...
    Elle est la première page que voit l'utilisateur avant s'être connecté.
    Elle doit être claire pour le l'utilisateur comprenne rapidement l'intérêt de l'application et son utilisation.
"""
import streamlit as st

# st.set_page_config(page_title="Accueil",
#                 page_icon="🏠",
#                 layout="centered",
#                 )

st.set_page_config(
    page_title="YOU REVIEW 🔎",
    page_icon="🔎",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.title("✨DONNEZ DE LA VALEUR À VOS COMMENTAIRES YOUTUBE✨")
st.subheader("Analysez et optimisez l'engagement de votre audience grâce à You Review")
st.write("""
Bienvenue sur **You Review**, l'outil ultime pour les créateurs de contenu YouTube souhaitant maximiser l'impact de leurs vidéos grâce à une analyse approfondie des commentaires.
Avec You Review, plongez au cœur des interactions de votre audience et découvrez des insights précieux pour inspirer et faire évoluer votre contenu tout en renforcant votre communauté. 
""")

st.header("Pourquoi analyser les commentaires YouTube ?")
st.write("""
Les commentaires sur vos vidéos YouTube sont une mine d'or d'informations. Ils reflètent les opinions, les préférences et les attentes de votre audience. En analysant ces commentaires, vous pouvez :
- Comprendre ce que votre audience aime ou n'aime pas.
- Identifier les tendances et les sujets populaires.
- Améliorer l'engagement en répondant aux besoins de votre communauté.
- Optimiser votre stratégie de contenu pour attirer plus de spectateurs.
""")
st.header("Fonctionnalités de You Review")
st.write("""
- **Analyse de Sentiment** : Découvrez le ton général des commentaires (positif, négatif, neutre) pour mieux comprendre les réactions de votre audience.
- **Mots-clés et Tendances** : Identifiez les mots et phrases les plus utilisés pour repérer les sujets d'intérêt.
- **Visualisations Intuitives** : Profitez de graphiques et de tableaux interactifs pour une analyse facile et rapide.

**Et d'autres à venir😉...**
""") # - **Recommandations Personnalisées** : Recevez des conseils sur mesure pour améliorer votre contenu en fonction des retours de votre audience.
st.header("Comment ça marche ?")
st.write("""
1. **Connexion** : Connectez-vous avec votre compte Google pour accéder à l'application.
2. **Importation des Vidéos** : Sélectionnez les vidéos YouTube que vous souhaitez analyser.
3. **Analyse des Commentaires** : Laissez You Review faire le travail en analysant les commentaires de vos vidéos.
4. **Visualisation des Résultats** : Explorez les insights à travers des visualisations claires et interactives.
5. **Optimisation du Contenu** : Utilisez les recommandations pour ajuster et améliorer votre stratégie de contenu.
""")
st.header("Prêt à transformer vos commentaires en opportunités ? 🫵🏾 ")