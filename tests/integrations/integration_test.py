import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

# =========================================== Tests d'intégration pour DataCollector ===========================================
class TestIntegrationExtractionPipeline:
    """
    Tests d'intégration pour la pipeline complète :
    DataCollector.get_info_video() → control_conformity() → get_data() → to_data_table()
    
    Différence avec les tests unitaires :
        Unitaire  → une seule méthode, tout le reste mocké
        Intégration → plusieurs méthodes enchaînées, seul l'externe (API) est mocké
    
    On mock uniquement ce qui est externe (APIInteraction/build),
    pas les méthodes internes de DataCollector.
    """

    def _make_mock_api(self, langue="fr", nb_comments=500):
        """
        Helper : crée un mock YouTube complet avec réponses pour
        videos().list() ET commentThreads().list().
        Réutilisé dans tous les tests d'intégration.
        """
        mock_youtube = MagicMock()

        # réponse pour get_info_video()
        mock_youtube.videos().list().execute.return_value = {
            "items": [{
                "snippet": {
                    "channelId": "UC_channel_123",
                    "defaultLanguage": langue,
                    "title": "Ma super vidéo"
                },
                "statistics": {"commentCount": str(nb_comments)}
            }]
        }

        # réponse pour get_data() → commentThreads
        mock_youtube.commentThreads().list().execute.return_value = {
            "items": [{
                "id": "comment_001",
                "snippet": {
                    "topLevelComment": {
                        "snippet": {
                            "channelId": "UC_channel_123",
                            "authorChannelId": "UC_viewer_456",
                            "videoId": "68QYq9jcEIQ",
                            "publishedAt": "2024-01-01T00:00:00Z",
                            "textOriginal": "Super vidéo !",
                            "likeCount": 5
                        }
                    }
                }
            }]
            # pas de nextPageToken = une seule page
        }
        return mock_youtube
    
    @patch("src.extraction.build")
    def test_pipeline_complete_fr_retourne_dataframe(self, mock_build):
        """
        Test du flux complet :
        __init__ → get_info_video() → control_conformity() → get_data() → to_data_table()
        
        Le chemin : vidéo française, assez de commentaires.
        On vérifie que toutes les méthodes s'enchaînent sans erreur
        et produisent un DataFrame valide.
        """

        # Arrange
        mock_build.return_value = self._make_mock_api(langue="fr", nb_comments=500)

        # Act — pipeline complète, aucune méthode mockée
        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.utils import DataCollector
            collector = DataCollector(
                video_url="https://youtu.be/68QYq9jcEIQ",
                video_id="68QYq9jcEIQ"
            )
            collector.get_info_video()   # remplit channel_id, language, etc.
            df = collector.to_data_table()  # appelle get_data() en interne

        # Assert — le DataFrame final est valide
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] >= 1
        assert "comment" in df.columns
        # les infos de la vidéo ont bien été transmises
        assert df["titre"].iloc[0] == "Ma super vidéo"

    @patch("src.extraction.build")
    def test_pipeline_bloquee_si_langue_non_fr(self, mock_build):
        """
        Test du flux complet avec vidéo non conforme.
        
        get_info_video() remplit language="en"
        → control_conformity() retourne False
        → get_data() lève ValueError
        → to_data_table() ne doit jamais être atteint
        
        On vérifie que le rejet se produit au bon endroit.
        """

        mock_build.return_value = self._make_mock_api(langue="en", nb_comments=500)

        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.utils import DataCollector
            collector = DataCollector(
                video_url="https://youtu.be/68QYq9jcEIQ",
                video_id="68QYq9jcEIQ"
            )
            collector.get_info_video()

            # get_data() doit rejeter via control_conformity()
            with pytest.raises(ValueError, match="conformité"):
                collector.to_data_table()

    @patch("src.extraction.build")
    def test_get_data_appelle_get_info_video_si_channel_id_none(self, mock_build):
        """
        Test d'intégration du mécanisme lazy loading :
        si channel_id est None au moment de get_data(),
        get_data() doit appeler get_info_video() automatiquement.
        
        Ce test vérifie l'interaction entre get_data() et get_info_video().
        """

        mock_build.return_value = self._make_mock_api(langue="fr", nb_comments=500)

        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.utils import DataCollector
            collector = DataCollector(
                video_url="https://youtu.be/68QYq9jcEIQ",
                video_id="68QYq9jcEIQ"
            )
            # on ne fait PAS get_info_video() avant get_data()
            # channel_id est None → get_data() doit le gérer
            assert collector.channel_id is None

            result = collector.get_data()

            # get_info_video() a été appelé implicitement
            assert collector.channel_id == "UC_channel_123"
            assert isinstance(result, list)
    
    @patch("src.extraction.build")
    def test_main_extraction_retourne_tuple_complet(self, mock_build):
        """
        Test de main_extraction() qui orchestre tout.
        Elle doit retourner (DataFrame, video_id, channel_id).
        
        C'est le point d'entrée de la pipeline — on vérifie
        que le tuple de sortie est complet et cohérent.
        """

        mock_build.return_value = self._make_mock_api(langue="fr", nb_comments=500)

        with patch.dict(os.environ, {"DEVELOPER_KEY": "fake_key"}):
            from src.utils import DataCollector
            collector = DataCollector(
                video_url="https://youtu.be/68QYq9jcEIQ",
                video_id="68QYq9jcEIQ"
            )
            collector.get_info_video()
            df, channel_id = collector.main_extraction()

        # le tuple est complet
        assert isinstance(df, pd.DataFrame)
        assert channel_id == "UC_channel_123"