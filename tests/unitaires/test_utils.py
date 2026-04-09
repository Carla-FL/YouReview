import pytest
from src.utils import url2id
# from unittest.mock import patch, MagicMock
# from streamlit.testing.v1 import AppTest

# ========================================
# TESTS UNITAIRES pour les fonctions de utils.py
# fonctions pure, pas de dépendances
# Pattern AAA (Arrange, Act, Assert)
# ___AAA___
# Arrange : préparer les données d'entrée et les résultats attendus
# Act : exécuter la fonction à tester
# Assert : vérifier que le résultat correspond à ce qui est attendu
# ========================================


# ======================================== URL2ID ================================================================================
# _______URL COURT VALIDE__________
def test_url2id_url_court():
    """ test une url au format court et vérifie que la fonction url2id extrait correctement l'id de la vidéo."""
    # Arrange 
    url = "https://youtu.be/68QYq9jcEIQ"
    # Act
    result = url2id(url)
    # Assert
    assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

def test_url2id_url_court_taille_id():
    """ test une url au format court et vérifie que la fonction url2id extrait bien un id de taille 11"""
    url = "https://youtu.be/68QYq9jcEIQ"
    result = url2id(url)
    assert len(result) == 11, f"Expected id length of 11 but got {len(result)}"

# _______URL LONG VALIDE__________
def test_url2id_url_longue():
    """ test une url au format long et vérifie que la fonction url2id extrait correctement l'id de la vidéo."""
    url = "https://www.youtube.com/watch?v=68QYq9jcEIQ"
    result = url2id(url)
    assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

def test_url2id_url_longue_taille_id():
    """ test une url au format long et vérifie que la fonction url2id extrait bien un id de taille 11"""
    url = "https://www.youtube.com/watch?v=68QYq9jcEIQ"
    result = url2id(url)
    assert len(result) == 11, f"Expected id length of 11 but got {len(result)}"

# _______URL INVALIDE__________
def test_url2id_url_vide():
    """ test une url vide et vérifie que la fonction url2id lève une exception ValueError, indiquant que l'URL est invalide."""
    with pytest.raises(ValueError): # on s'assure que la fonction me donne bien l'erreur attendu et programmé
        url2id("")


# _______URL COURT INVALIDE__________
def test_url2id_url_court_http():
    """ test une url au format court mais avec http au lieu de https et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("http://youtu.be/68QYq9jcEIQ")

def test_url2id_url_court_id_invalide():
    """ test une url au format court mais avec un id de vidéo invalide (trop long) et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://youtu.be/68QYq9jcEIbvjhvjhvjvcQ")

def test_url2id_url_court_non_youtube():
    """ test une url au format court qui ne correspond pas à un format YouTube valide et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://youtube.com/68QYq9jcEIQ")

def test_url2id_url_court_sans_id():
    """ test une url au format court qui ne contient pas d'id de vidéo et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://www.youtu.be/")


# _______URL LONG INVALIDE__________
def test_url2id_url_long_http():
    """ test une url au format long mais avec http au lieu de https et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("http://www.youtube.com/watch?v=68QYq9jcEIQ")

def test_url2id_url_longue_id_invalide():
    """ test une url au format long mais avec un id de vidéo invalide (trop long) et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://www.youtube.com/watch?v=68QYq9jcEIbvjhvjhvjvcQ")


def test_url2id_url_long_non_youtube():
    """ test une url au format long qui ne correspond pas à un format YouTube valide et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://www.youtu.be/watch?v=68QYq9jcEIQ")


def test_url2id_url_long_sans_id():
    """ test une url au format long qui ne contient pas d'id de vidéo et vérifie que la fonction lève une exception ValueError."""
    with pytest.raises(ValueError):
        url2id("https://www.youtube.com/watch?v=")

# ======================================== INITIALIZE SESSION STATE ================================================================================
# def test_cles_creees_si_absentes():
#     """Les 3 clés de session sont créées si elles n'existent pas"""
#     # Arrange : app minimale qui appelle initialize_session_state
#     app_script = """
#     import streamlit as st
#     from src.utils import initialize_session_state
#     initialize_session_state()
#     st.write(str(st.session_state.authenticated))
#     st.write(str(st.session_state.url_inputed))
#     st.write(str(st.session_state.videoid))
#     """
#     # Act
#     at = AppTest.from_string(app_script).run()
#     # Assert
#     assert not at.exception
#     assert "False" in at.markdown[0].value or "False" in str(at.get("write"))


def test_get_url():
    pass

def test_authenticate_user():
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
