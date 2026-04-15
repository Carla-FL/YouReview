import os
import pytest
from src.utils import url2id
from unittest.mock import patch, MagicMock
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

class TestAPIInteraction :
    """
        Tests unitaires pour APIInteraction.
        
        On teste UNIQUEMENT la logique de la classe :
        - est-ce que __enter__ crée bien self.api_client ?
        - est-ce que __exit__ ferme bien la connexion ?
        - est-ce que les erreurs sont bien propagées ?
        
        On ne teste PAS YouTube — on mock build().
        """
    
    @patch("src.extraction.build")
    def test_enter_cree_api_client(self, mock_build):
        """
        __enter__ doit créer self.api_client en appelant build().
        
        Pourquoi @patch("src.extraction.build") ?
            → build() est importé DANS extraction.py
            → il faut patcher là où il est utilisé, pas là où il est défini
            → "src.extraction.build" = le build() tel qu'il existe dans ce module
        
        Pourquoi mock_build en paramètre ?
            → @patch injecte automatiquement le mock comme dernier argument
            → le nom du paramètre n'a pas d'importance, par convention "mock_build"
        """

        # Arrange — on configure ce que build() doit retourner
        mock_youtube_client = MagicMock() # MagicMock() simule un client YouTube qui accepte n'importe quel appel
        mock_build.return_value = mock_youtube_client

        # Act — on utilise APIInteraction comme dans le vrai code
        # patch.dict remplace os.environ pendant le test, restauré après
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.extraction import APIInteraction
            with APIInteraction() as api:

                # Assert — à l'intérieur du "with", api_client doit exister
                assert api.api_client is not None

                # build() a bien été appelé avec les bons arguments
                mock_build.assert_called_once_with(
                    "youtube", "v3", developerKey="fake_key"
                )


    @patch("src.extraction.build")
    def test_exit_ferme_connexion(self, mock_build):
        """
        __exit__ doit appeler .close() sur api_client.
        
        Pourquoi tester ça ?
            → Si close() n'est pas appelé, la connexion reste ouverte
            → Avec des centaines d'appels, ça peut épuiser les ressources
        """

        # Arrange
        mock_youtube_client = MagicMock()
        mock_build.return_value = mock_youtube_client

        # Act — on entre ET on sort du bloc with
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.extraction import APIInteraction
            with APIInteraction():
                pass  # on ne fait rien, on veut juste tester __exit__

        # Assert — après le "with", close() doit avoir été appelé
        # assert_called_once() vérifie que close() a été appelé exactement 1 fois
        # (pas 0 fois = oubli, pas 2 fois = bug)
        mock_youtube_client.close.assert_called_once()


    @patch("src.extraction.build")
    def test_build_echoue_propage_exception(self, mock_build):
        """
        Si build() lève une exception, APIInteraction doit la propager.
        
        Pourquoi ?
            → On veut que les erreurs soient visibles, pas silencieuses
            → Si build() plante et qu'on l'ignore, le code continue
            avec un api_client None → crash obscur plus loin
        """

        # Arrange — on configure build() pour qu'il plante
        mock_build.side_effect = Exception("Clé API invalide")
        #          ↑ side_effect = au lieu de retourner une valeur,
        #            build() va lever cette exception

        # Act + Assert — on vérifie que l'exception remonte bien
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.extraction import APIInteraction
            with pytest.raises(Exception, match="Clé API invalide"):
                with APIInteraction():
                    pass


# ========================================= TEST DatabaseInteractio ================================================================================
class TestDatabaseInteraction:
    pass

# ========================================= TEST DataCollector ================================================================================
# DataCollector a 4 méthodes à tester :
#   get_info_video()      → appel API videos().list()
#   control_conformity()  → logique pure, PAS d'appel API → pas de mock
#   get_data()            → appel API commentThreads().list() en boucle
#   to_data_table()       → appelle get_data() et construit un DataFrame
#
# Stratégie :
#   - get_info_video et get_data : on mock APIInteraction
#   - control_conformity : on injecte directement les attributs, pas de mock
#   - to_data_table : on mock get_data() directement
# =============================================================================================================================================
class TestDataCollector:
    def setup_method(self):
        """
        Tourne avant chaque test.
        On crée un DataCollector avec des valeurs fixes réutilisables.
        On ne fait AUCUN appel API ici.
        """
        # on instancie sans appel API car get_info_video() n'est plus dans __init__
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.utils import DataCollector
            self.collector = DataCollector(
                video_url="https://youtu.be/68QYq9jcEIQ",
                video_id="68QYq9jcEIQ"
            )
    

    @patch("src.extraction.build")
    def test_get_info_video_remplit_attributs(self, mock_build):
        """
        get_info_video() doit remplir channel_id, language,
        nb_comments et video_title à partir de la réponse API.
        
        Comment on simule la réponse API ?
            → On crée un dict qui ressemble exactement à ce que YouTube renvoie
            → On le branche sur mock_youtube.videos().list().execute()
            → Quand le code appelle .execute(), il reçoit notre dict
        """

        # Arrange — réponse API simulée (structure identique au vrai YouTube)
        fausse_reponse_api = {
            "items": [{
                "snippet": {
                    "channelId": "UC_channel_123",
                    "defaultLanguage": "fr",
                    "title": "Ma super vidéo"
                },
                "statistics": {
                    "commentCount": "500"
                }
            }]
        }

        # on configure la chaîne d'appels
        # api_client.videos().list().execute() → fausse_reponse_api
        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = fausse_reponse_api
        mock_build.return_value = mock_youtube

        # Act
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            self.collector.get_info_video()

        # Assert — les 4 attributs doivent être remplis correctement
        assert self.collector.channel_id == "UC_channel_123"
        assert self.collector.language == "fr"
        assert self.collector.nb_comments == 500   # converti en int
        assert self.collector.video_title == "Ma super vidéo"

    @patch("src.extraction.build")
    def test_get_info_video_video_introuvable(self, mock_build):
        """
        Si l'API retourne une liste vide, get_info_video() doit lever ValueError.
        
        Cas réel : video_id inexistant ou vidéo supprimée.
        """

        # Arrange — réponse avec items vide (vidéo introuvable)
        mock_youtube = MagicMock()
        mock_youtube.videos().list().execute.return_value = {"items": []}
        mock_build.return_value = mock_youtube

        # Act + Assert
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            with pytest.raises(ValueError, match="introuvable"):
                self.collector.get_info_video()

    def test_conformite_langue_fr_et_assez_commentaires(self):
        """
        Vidéo en français avec 500 commentaires → conforme.
        
        Pourquoi pas de mock ?
            → control_conformity() ne fait aucun appel API
            → elle lit juste self.language et self.nb_comments
            → on injecte directement ces valeurs dans l'objet
        """

        # Arrange — on injecte les attributs directement
        self.collector.language = "fr"
        self.collector.nb_comments = 500

        # Act
        result = self.collector.control_conformity()

        # Assert
        assert result

    def test_conformite_langue_non_fr(self):
        """Vidéo en anglais → non conforme même avec assez de commentaires."""
        self.collector.language = "en"
        self.collector.nb_comments = 500
        assert not self.collector.control_conformity() 

    def test_conformite_pas_assez_commentaires(self):
        """Vidéo française avec moins de 200 commentaires → non conforme."""
        self.collector.language = "fr"
        self.collector.nb_comments = 50
        assert not self.collector.control_conformity()

    def test_conformite_exactement_200_commentaires(self):
        """
        200 commentaires exactement → conforme (cas limite).
        
        Pourquoi tester ce cas limite ?
            → La condition est >= 200
            → 199 = non conforme, 200 = conforme
            → Ce genre d'erreur (> vs >=) est fréquent
        """
        self.collector.language = "fr"
        self.collector.nb_comments = 200
        assert self.collector.control_conformity()

    @patch("src.extraction.build")
    def test_get_data_retourne_liste_de_dicts(self, mock_build):
        """
        get_data() doit retourner une liste de dicts avec les bons champs.
        
        Comment on simule la pagination ?
            → Premier appel : items + nextPageToken = "page2"
            → Deuxième appel : items + nextPageToken = None (fin)
            → side_effect avec une liste = chaque appel consomme un élément
        """

        # Arrange — on pré-remplit les attributs pour éviter get_info_video()
        self.collector.channel_id = "UC_channel_123"
        self.collector.language = "fr"
        self.collector.nb_comments = 500
        self.collector.video_title = "Ma vidéo"

        # réponse simulée pour commentThreads
        def make_comment(comment_id, author_id):
            """Helper pour créer un commentaire simulé"""
            return {
                "id": comment_id,
                "snippet": {
                    "topLevelComment": {
                        "snippet": {
                            "channelId": "UC_channel_123",
                            "authorChannelId": author_id,
                            "videoId": "68QYq9jcEIQ",
                            "publishedAt": "2024-01-01T00:00:00Z",
                            "textOriginal": "Super vidéo !",
                            "likeCount": 5
                        }
                    }
                }
            }

        # page 1 → a un nextPageToken
        page_1 = {
            "items": [make_comment("comment_001", "UC_viewer_A")],
            "nextPageToken": "token_page_2"
        }
        # page 2 → pas de nextPageToken = fin de la pagination
        page_2 = {
            "items": [make_comment("comment_002", "UC_viewer_B")],
            # pas de nextPageToken → la boucle s'arrête
        }

        # side_effect = liste → premier appel retourne page_1,
        #                        deuxième appel retourne page_2
        mock_youtube = MagicMock()
        mock_youtube.commentThreads().list().execute.side_effect = [page_1, page_2]
        mock_build.return_value = mock_youtube

        # Act
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            result = self.collector.get_data()

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2   # 1 commentaire par page
        # les champs attendus sont présents
        champs = {"url", "id", "titre", "channelId", "videoId",
                "publishedAt", "comment", "likeCount", "extractedAt"}
        assert champs.issubset(result[0].keys())

    @patch("src.extraction.build")
    def test_get_data_ignore_commentaire_auteur(self, mock_build):
        """
        get_data() doit ignorer les commentaires postés par l'auteur de la vidéo.
        
        Cas réel : le créateur répond dans ses propres commentaires.
        Le channel_id de la vidéo = l'authorChannelId → on ignore.
        """

        self.collector.channel_id = "UC_channel_123"
        self.collector.language = "fr"
        self.collector.nb_comments = 500
        self.collector.video_title = "Ma vidéo"

        # commentaire posté par l'auteur lui-même
        commentaire_auteur = {
            "items": [{
                "id": "comment_auteur",
                "snippet": {
                    "topLevelComment": {
                        "snippet": {
                            "channelId": "UC_channel_123",
                            "authorChannelId": "UC_channel_123",  # ← même ID = auteur
                            "videoId": "68QYq9jcEIQ",
                            "publishedAt": "2024-01-01T00:00:00Z",
                            "textOriginal": "Merci pour vos commentaires !",
                            "likeCount": 100
                        }
                    }
                }
            }]
            # pas de nextPageToken
        }

        mock_youtube = MagicMock()
        mock_youtube.commentThreads().list().execute.return_value = commentaire_auteur
        mock_build.return_value = mock_youtube

        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            result = self.collector.get_data()

        # le commentaire de l'auteur doit être filtré → liste vide
        assert result == []

    @patch("src.extraction.build")
    def test_get_data_video_non_conforme_leve_erreur(self, mock_build):
        """
        get_data() doit lever ValueError si la vidéo n'est pas conforme.
        On ne fait aucun appel à commentThreads dans ce cas.
        """

        # Arrange — vidéo en anglais → non conforme
        self.collector.channel_id = "UC_channel_123"
        self.collector.language = "en"   # ← non conforme
        self.collector.nb_comments = 500

        # Act + Assert
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            with pytest.raises(ValueError, match="conformité"):
                self.collector.get_data()
    
    def test_to_data_table_retourne_dataframe(self):
        """
        to_data_table() doit retourner un DataFrame pandas.
        
        Pourquoi on mock get_data() ici et pas build() ?
            → to_data_table() appelle get_data()
            → get_data() est déjà testé séparément
            → ici on teste UNIQUEMENT que to_data_table() construit
            bien un DataFrame à partir de ce que get_data() retourne
            → on évite de re-tester toute la logique de get_data()
        
        C'est le principe d'isolation : chaque test teste une seule chose.
        """
        import pandas as pd

        # Arrange — on remplace get_data() par une version qui retourne
        # directement une liste, sans aucun appel API
        fausses_donnees = [
            {
                "url": "https://youtu.be/68QYq9jcEIQ",
                "id": "comment_001",
                "titre": "Ma vidéo",
                "channelId": "UC_channel_123",
                "videoId": "68QYq9jcEIQ",
                "publishedAt": "2024-01-01T00:00:00Z",
                "comment": "Super vidéo !",
                "likeCount": 5,
                "extractedAt": "2024-01-01 12:00:00"
            }
        ]

        # patch.object cible UNE méthode d'UNE instance spécifique
        # ici self.collector.get_data → retourne fausses_donnees
        with patch.object(self.collector, "get_data", return_value=fausses_donnees):
            result = self.collector.to_data_table()

        # Assert
        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == 1      # 1 ligne
        assert result.shape[1] == 9      # 9 colonnes
        assert "comment" in result.columns


