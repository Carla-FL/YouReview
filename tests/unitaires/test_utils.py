import pytest
from src.utils import url2id
from streamlit.testing.v1 import AppTest

# AAA (Arrange, Act, Assert)

def test_url2id():

    # arrange prépare les données d'entrée et les résultats attendus
    url = "https://youtu.be/68QYq9jcEIQ"

    # act exécute la fonction à tester
    result = url2id(url)

    # assert vérifie que le résultat correspond à ce qui est attendu
    assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

def test_url2id_erreur():
    with pytest.raises(ValueError): # on s'assure que la fonction me donne bien l'erreur attendu et programmé
        url2id("https://youtube/68QYq9jcEIQ")
        url2id("http://youtu.be/68QYq9jcEIQ")
        url2id("https://youtube/68QYq9jcEIbvjhvjhvjvcQ")
        url2id("")

def test_get_url():
    pass

def test_authenticate_user():

    app_scrit = """
    import streamlit as st
    
"""
    pass
#     app_script = """
#     import streamlit as st

#     with st.form("url_form"):
#         url = st.text_input(label="L'url de la vidéo", value=st.session_state.url_inputed,  placeholder="https://www.youtube.com/watch..........", key="url_input") #key="url",
#         submit_button = st.form_submit_button("Analyser") # création du boutton
#     ##
#     if submit_button : #st.button("Analyser"):
#         if url == "":
#             st.error("Veuillez entrer une URL YouTube valide.")
#             return None, None
#         else :
#             try :
#                 video_id = url2id(url)
#                 st.session_state.url_inputed = url
#                 return url, video_id
#             except Exception as e:
#                 st.error(f"Une erreur est survenue lors de la validation de l'URL : {e}")
#                 return None, None
#             # st.write(f"Analyse de la vidéo : {url}")
#     return st.session_state.url_inputed, st.session_state.videoid

    
#     """

#     at = AppTest.from_string(app_script)
#     at.secrets["url_unput"]
    # at = AppTest.from_file("src/utils.py").run()

    # at.text_input("url_input").enter("https://youtu.be/68QYq9jcEIQ").run()
    # at.button("submit_button").click().run()
