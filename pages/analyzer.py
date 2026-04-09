import streamlit as st
from src.utils import initialize_session_state, authenticate_user, get_url
# from src.extraction import DatabaseInteraction

# Initialize session state for authentication
initialize_session_state()


st.title("YOU REVIEW ")
st.subheader("L'Analyse automatisée de vos commentaires YouTube", divider="gray")

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
        st.success(f"URL validée ! ID de la vidéo : {video_id, url}")

        st.write("Test de la connexion à la base de données ")
        # with st.spinner("Wait for it...", show_time=True):
        #     with DatabaseInteraction() as db:
        #         st.success("Connexion à la base de données réussie !")
        #         pass

