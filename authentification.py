""" 
Streamlit login page :

Permet de s'assure que seul les utilisateurs authentifiés peuvent accéder à l'application.
Il s'agit ici des influenceurs YouTube qui doivent se connecter avec leurs comptes Google pour utiliser l'application.
Ainsi, seuls les influenceurs propriétaire du contenu peuvent accéder à la l'analyse lié aux commenteur de leurs vidéos.
"""

import streamlit as st
from src.utils import initialize_session_state
# import bcrypt
# pour le hash des mots de passe

# Initialize session state for authentication


def authenticate_user(username, password):
    """Vérifie les identifiants de l'utilisateur
    
    Args:
        username (str): Le nom d'utilisateur
        password (str): Le mot de passe"""
    
    initialize_session_state()
    # Page de connexion
    if not st.session_state.authenticated:
        st.title("Connexion 🔐")
        st.write("Veuillez vous connecter pour accéder à l'application.")
        # st.write("Veuillez vous connecter avec votre compte Google pour accéder à l'application.")
        with st.form("login_form"):
            username = st.text_input(label="Nom de la chaine YouTube",placeholder=" @Squeezie / @SEB / @LenaSituations" ) # création du champ de saisie pour le nom d'utilisateur
            password = st.text_input("Mot de passe", type="password") # création du champ de saisie pour le mot de passe
            submit_button = st.form_submit_button("Se connecter") # création du boutton

            if submit_button: # si le boutton est cliqué
                if username == st.secrets.admin.username and password == st.secrets.admin.password: # vérification des identifiants et mot de passe
                    st.session_state.authenticated = True # mise à jour de l'état de la session
                    st.session_state.user = username # stockage du nom d'utilisateur dans la session
                    st.success("Connexion réussie ! Vous pouvez maintenant accéder à l'application.")
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")
    else :  
        # st.write("Vous êtes déjà connecté. La page principale de l'application s'affichera ici bientôt.")
        st.error("Pour des raisons de sécurité vous devez vous authentifier pour accéder à l'application.")
