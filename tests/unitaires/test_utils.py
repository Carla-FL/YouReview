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
class TestUrl2Id:
# _______URL COURT VALIDE__________
    def test_url2id_url_court(self):
        """ test une url au format court et vérifie que la fonction url2id extrait correctement l'id de la vidéo."""
        # Arrange 
        url = "https://youtu.be/68QYq9jcEIQ"
        # Act
        result = url2id(url)
        # Assert
        assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

    def test_url2id_url_court_taille_id(self):
        """ test une url au format court et vérifie que la fonction url2id extrait bien un id de taille 11"""
        url = "https://youtu.be/68QYq9jcEIQ"
        result = url2id(url)
        assert len(result) == 11, f"Expected id length of 11 but got {len(result)}"

    # _______URL LONG VALIDE__________
    def test_url2id_url_longue(self):
        """ test une url au format long et vérifie que la fonction url2id extrait correctement l'id de la vidéo."""
        url = "https://www.youtube.com/watch?v=68QYq9jcEIQ"
        result = url2id(url)
        assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

    def test_url2id_url_longue_taille_id(self):
        """ test une url au format long et vérifie que la fonction url2id extrait bien un id de taille 11"""
        url = "https://www.youtube.com/watch?v=68QYq9jcEIQ"
        result = url2id(url)
        assert len(result) == 11, f"Expected id length of 11 but got {len(result)}"
    
    def test_url2id_url_longue_avec_parametres(self):
        """ test une url au format long qui contient des paramètres supplémentaires, comme le nombre de secondes déjà visioné de la vidéo (ex: https://www.youtube.com/watch?v=Wfr3Ks4A2IM&t=281s) et vérifie que la fonction url2id extrait correctement l'id de la vidéo sans être affectée par les paramètres supplémentaires."""
        url = "https://www.youtube.com/watch?v=68QYq9jcEIQ&t=30s"
        result = url2id(url)
        assert result == "68QYq9jcEIQ", f"Expected '68QYq9jcEIQ' but got {result}"

    # _______URL INVALIDE__________
    def test_url2id_url_vide(self):
        """ test une url vide et vérifie que la fonction url2id lève une exception ValueError, indiquant que l'URL est invalide."""
        with pytest.raises(ValueError): # on s'assure que la fonction me donne bien l'erreur attendu et programmé
            url2id("")


    # _______URL COURT INVALIDE__________
    def test_url2id_url_court_http(self):
        """ test une url au format court mais avec http au lieu de https et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("http://youtu.be/68QYq9jcEIQ")

    def test_url2id_url_court_id_invalide(self):
        """ test une url au format court mais avec un id de vidéo invalide (trop long) et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("https://youtu.be/68QYq9jcEIbvjhvjhvjvcQ")

    def test_url2id_url_court_non_youtube(self):
        """ test une url au format court qui ne correspond pas à un format YouTube valide et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("https://youtube.com/68QYq9jcEIQ")

    def test_url2id_url_court_sans_id(self):
        """ test une url au format court qui ne contient pas d'id de vidéo et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("https://www.youtu.be/")


    # _______URL LONG INVALIDE__________
    def test_url2id_url_long_http(self):
        """ test une url au format long mais avec http au lieu de https et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("http://www.youtube.com/watch?v=68QYq9jcEIQ")

    def test_url2id_url_longue_id_invalide(self):
        """ test une url au format long mais avec un id de vidéo invalide (trop long) et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("https://www.youtube.com/watch?v=68QYq9jcEIbvjhvjhvjvcQ")


    def test_url2id_url_long_non_youtube(self):
        """ test une url au format long qui ne correspond pas à un format YouTube valide et vérifie que la fonction lève une exception ValueError."""
        with pytest.raises(ValueError):
            url2id("https://www.youtu.be/watch?v=68QYq9jcEIQ")


    def test_url2id_url_long_sans_id(self):
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
class TestInitializeSessionState:

    def test_initialize_session_state_vide(self):
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
        assert not at.session_state["authenticated"] # on s'assure que la variable authenticated est bien initialisée à False
        assert at.session_state["url_inputed"]== ""  # on s'assure que la variable url_inputed est bien initialisée à None (affiché comme une chaîne vide)
        assert at.session_state["videoid"] is None  # on s'assure que la variable videoid est bien initialisée à None

    def test_initialize_session_state_deja_initialise(self):
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
        assert at.session_state["authenticated"] # on s'assure que la variable authenticated n'est pas réinitialisée à False
        assert at.session_state["url_inputed"] == "https://www.youtube.com/watch?v=68QYq9jcEIQ"  # on s'assure que la variable url_inputed n'est pas réinitialisée à None
        assert at.session_state["videoid"] == "68QYq9jcEIQ" # on s'assure que la variable videoid n'est pas réinitialisée à None

# ======================================== AUTHENTICATE USER ================================================================================
class TestAuthenticateUser:
    def setup_method(self):
        self.app_script = """
        import streamlit as st
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        with st.form("login_form"):
            username = st.text_input(label="Nom de la chaine YouTube",placeholder=" @Squeezie / @SEB / @LenaSituations" ) # création du champ de saisie pour le nom d'utilisateur
            password = st.text_input("Mot de passe", type="password") # création du champ de saisie pour le mot de passe
            submit_button = st.form_submit_button("Se connecter") # création du boutton

        # st.write("Veuillez vous connecter avec votre compte Google pour accéder à l'application.")
        if submit_button: # si le boutton est cliqué
            if not st.session_state.authenticated:
                if username == st.secrets.admin.username and password == st.secrets.admin.password: # vérification des identifiants et mot de passe
                    st.session_state.authenticated = True # mise à jour de l'état de la session
                    st.session_state.user = username # stockage du nom d'utilisateur dans la session
                    st.success("Connexion réussie ! Vous pouvez maintenant accéder à l'application.")
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect.")
                """

    def test_authenticate_user_valide(self):
        """ la fonction authenticate_user affiche un formuler de connexion streamlit et l'utilisateur soumet le formulaire avec
            - username
            - password
            si username + password sont corrects -> autneticated = True
            on test que la fonction authenticate_user affiche bien le formulaire de connexion et que lorsque l'utilisateur soumet le formulaire avec des identifiants corrects, la variable authenticated est mise à True dans le session state. 
            """
        
        at = AppTest.from_string(self.app_script)

        at.secrets["admin"] = {"username": "testuser", "password": "testpass"}

        at = at.run()

        at.text_input[0].set_value("testuser").run()  # premier champ
        at.text_input[1].set_value("testpass").run()  # deuxième champ
        # at.form("login_form").submit().run()
        at.button[0].click().run()

        assert not at.exception
        assert at.session_state["authenticated"] 

    def test_authenticate_user_invalide(self):
        """ 
        On peut aussi tester que si les identifiants sont incorrects, authenticated reste à False et un message d'erreur s'affiche.
            """
        
        at = AppTest.from_string(self.app_script)

        at.secrets["admin"] = {"username": "testuser", "password": "testpass"}

        at = at.run()

        at.text_input[0].set_value("testuser").run()
        at.text_input[1].set_value("testpassinvalide").run()
        # at.form("login_form").submit().run()
        at.button[0].click().run()

        assert not at.exception
        assert not at.session_state["authenticated"]
        assert len(at.error) > 0

    def test_authenticate_user_vide(self):
        """ 
        On peut aussi tester que si les identifiants sont vides, authenticated reste à False et un message d'erreur s'affiche.
            """
        
        at = AppTest.from_string(self.app_script)

        at.secrets["admin"] = {"username": "testuser", "password": "testpass"}

        at = at.run()

        #at.form("login_form").submit().run()
        at.button[0].click().run()

        assert not at.exception
        assert not at.session_state["authenticated"]
        assert len(at.error) > 0

# ======================================== GET DATA COLLECTOR ================================================================================

