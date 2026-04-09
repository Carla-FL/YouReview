import pytest
from src.utils import url2id
# from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

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
# ici on utilise AppTest
# les tests avec AppTest suivent toujours ce schéma :
# 1 créer : 
# 2 configurer : ajouter des secrets, des entrées de formulaire, session state, etc.
# 3 lancer
# 4 intéragir : simuler l'utilisation
# 5 vérifier : inspecter ce qui s'affiche

def test_initialize_session_state_vide():
    """ la fonction initialize_session_state() est censée initialiser les variables de session state suivantes : authenticated, url_inputed, videoid. Ce test vérifie que ces variables sont bien initialisées à False ou None après l'appel de la fonction."""
    # 1
    app_script =  """
    import streamlit as st
    from src.utils import initialize_session_state
    initialize_session_state()
    st.write(str(st.session_state.authenticated))
    st.write(str(st.session_state.url_inputed))
    st.write(str(st.session_state.videoid))
    """
    # 3
    at = AppTest.from_string(app_script).run()

    # 5
    assert not at.exception # on s'assure que l'exécution de l'application ne génère pas d'exception, qu'elle n'a pas crashé
    assert len(at.markdown) == 3 # on s'assure que les 3 variables sont bien écrites dans l'application
    assert at.session_state["authenticated"]== False, "le session state autheticated doit être False" # on s'assure que la variable authenticated est bien initialisée à False
    assert at.session_state["url_inputed"]== ""  # on s'assure que la variable url_inputed est bien initialisée à None (affiché comme une chaîne vide)
    assert at.session_state["videoid"]== None  # on s'assure que la variable videoid est bien initialisée à None

def test_initialize_session_state_deja_initialise():
    """ ce test vérifie que si les variables de session state sont déjà initialisées (par exemple, authenticated est déjà à True), la fonction initialize_session_state() ne les réinitialise pas et conserve leurs valeurs actuelles."""
    app_script =  """
    import streamlit as st
    from src.utils import initialize_session_state
    st.session_state.authenticated = True
    st.session_state.url_inputed = "https://www.youtube.com/watch?v=68QYq9jcEIQ"
    st.session_state.videoid = "68QYq9jcEIQ"
    initialize_session_state()
    """
    at = AppTest.from_string(app_script).run()
    assert not at.exception
    assert at.session_state["authenticated"]== True, "le session state autheticated doit rester True" # on s'assure que la variable authenticated n'est pas réinitialisée à False
    assert at.session_state["url_inputed"] == "https://www.youtube.com/watch?v=68QYq9jcEIQ", "le session state url_inputed doit rester inchangé" # on s'assure que la variable url_inputed n'est pas réinitialisée à None
    assert at.session_state["videoid"] == "68QYq9jcEIQ", "le session state videoid doit rester inchangé" # on s'assure que la variable videoid n'est pas réinitialisée à None


def test_get_url():
    pass

def test_authenticate_user():

    app_script = """
    
    """

    at = AppTest.from_string(app_script)

#     at.secrets["url_unput"]
    # at = AppTest.from_file("src/utils.py").run()

    # at.text_input("url_input").enter("https://youtu.be/68QYq9jcEIQ").run()
    # at.button("submit_button").click().run()
