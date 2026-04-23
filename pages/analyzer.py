import streamlit as st
from src.utils import initialize_session_state, authenticate_user, get_url, DataCollector, DataMedaillonStorage
# import time
# from src.extraction import DatabaseInteraction

# Initialize session state for authentication
initialize_session_state()


st.title("YOU REVIEW ")
st.subheader("L'Analyse automatisée de vos commentaires YouTube", divider="gray")
st.subheader("Connexion 🔐")
st.write("Veuillez vous connecter pour accéder à l'application.")

if not st.session_state.authenticated:
    with st.empty():
        try :
            authenticate_user(None, None)
        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'authentification : {e}")

if st.session_state.authenticated:
    url, video_id = get_url()
    if url and video_id:
        st.session_state.videoid = video_id
        st.session_state.url_inputed = url
        # st.success(f"URL validée ! ID de la vidéo : {video_id, url}")

        st.write("La vidéo")
        with st.spinner("Chargement de la vidéo...", show_time=True):
            # Afficher la vidéo
            st.video(url)
        with st.spinner("Chargement des données....", show_time=True):
            
            # on regarde si les données sont déjà dans la base de données
            dc_ = DataCollector(url, video_id)
            dc_.get_info_video()
            channel_id = dc_.channel_id
            with DataMedaillonStorage(channel_id=channel_id, video_id=video_id) as data_storage:
                
                # si oui on affiche les insights
                if not data_storage.check_existing_video("bronze"):
                    
                    st.info("Données non présentes dans la base de données. Extraction en cours...")
                    # Extraction des données
                    data = dc_.get_data()
                    data_storage.db_insert(data, "bronze")
                else :
                    pass
            
        

