import re
import os
import time
import pandas as pd
import streamlit as st

from src.extraction import APIInteraction,DatabaseInteraction

def initialize_session_state():
    """Initialise les variables de session si elles n'existent pas"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if 'url_inputed' not in st.session_state:
        st.session_state.url_inputed = ""
    if 'videoid' not in st.session_state:
        st.session_state.videoid = None


def get_url():
    """Formulaire pour saisir l'URL de la vidéo YouTube et valider son format.

    Returns:
        str: l'id de la vidéo
        str: l'url de la vidéo
    """
    with st.form("url_form"):
        url = st.text_input(label="L'url de la vidéo", value=st.session_state.url_inputed,  placeholder="https://www.youtube.com/watch..........", key="url_input") #key="url",
        submit_button = st.form_submit_button("Analyser") # création du boutton
    ##
    if submit_button : #st.button("Analyser"):
        if url == "":
            st.error("Veuillez entrer une URL YouTube valide.")
            return None, None
        else :
            try :
                video_id = url2id(url)
                st.session_state.url_inputed = url
                return url, video_id
            except Exception as e:
                st.error(f"Une erreur est survenue lors de la validation de l'URL : {e}")
                return None, None
            # st.write(f"Analyse de la vidéo : {url}")
    return st.session_state.url_inputed, st.session_state.videoid


def authenticate_user(username, password):
    """Vérifie les identifiants de l'utilisateur
    
    Args:
        username (str): Le nom d'utilisateur
        password (str): Le mot de passe"""
    
    # Page de connexion
    # st.subheader("Connexion 🔐")
    # st.write("Veuillez vous connecter pour accéder à l'application.")
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


# récupérer l'id de la vidéo à partir de l'URL
def url2id(video_url:str) -> str:
    """ Convertit une URL YouTube en ID de vidéo si l'URL est valide.
    Args:
        video_url (str): L'URL de la vidéo YouTube
    Returns:
        str: L'ID de la vidéo YouTube"""

    long_pattern = r'^((https:\/\/www\.youtube\.com\/watch\?v=).{11}\&)|((https:\/\/www\.youtube\.com\/watch\?v=).{11}$)' #r'^(https:\/\/www\.youtube\.com\/watch\?v=).{11}\&' # pattern pour les URL classiques de YouTube (quand on le récupère à partir de la miniature)
    short_pattern = r'^(https:\/\/youtu.be/).{11}$' # pattern pour les URL courtes de YouTube (quand on regarde la vidéo)
    
    if re.match(short_pattern, video_url) :
        print("Valid YouTube URL")
        video_id = video_url[-11:] #  code pour extraire l'id de la vidéo à partir de l'URL courte
        return video_id
    if re.match(long_pattern, video_url) :
        print("Valid YouTube URL")
        video_id = video_url.split("v=")[-1][:11]  #  code pour extraire l'id de la vidéo à partir de l'URL longue
        return video_id
    else:
        raise ValueError('Error : invalid YouTube URL')


class DataCollector :
    """
    Classe d'extraction des données YouTube à partir d'une URL de vidéo.
    
    Args:
        video_url (str): L'URL de la vidéo YouTube à analyser

    """
    def __init__(self, video_url:str="", video_id:str="", maxresults:int=100):
        
        self.api_key = os.getenv('DEVELOPER_KEY')
        self.maxresults = maxresults
        self.video_url = video_url
        self.video_id = video_id
        self.channel_id = None
        self.language = None
        self.nb_comments = None
        self.video_title = None
        self.maxresults = maxresults



    def get_info_video(self):
        """
        Utilise la classe APIInteraction pour récupérer les informations d'une vidéo YouTube en utilisant l'API YouTube Data v3.
        Ici on récupère l'id de la chaîne, la langue de la vidéo, le nombre de commentaires et le titre de la vidéo.
        """
        with APIInteraction() as api_interaction :
            response = api_interaction.api_client.videos().list(
            part="snippet,statistics",
            id=self.video_id,
            maxResults=1).execute()
        if not response.get("items"):
            raise ValueError(f"Vidéo introuvable : {self.video_id}")
        item = response["items"][0]
        self.channel_id = item["snippet"]["channelId"]
        self.language = item["snippet"].get("defaultLanguage", "")
        self.nb_comments = int(item["statistics"].get("commentCount", 0))
        self.video_title = item["snippet"]["title"]


    def control_conformity(self) -> bool:
        """
        Cette méthode vérifie que la vidéo respecte les critères de conformité : langue française et au moins 200 commentaires.
        On utilise les informations récupérées par la méthode get_info_video pour effectuer ces vérifications.

        Returns:
            booleen: le résultat du test de fonromité True ou False
        """
        # Vérifier la langue et le nombre de commentaires
        if self.language == 'fr' and self.nb_comments >= 200 :
            return True
        else:
            return False
        

    def get_data(self):
        # on récupère les infos si pas encore fait
        if self.channel_id is None:
            self.get_info_video()

        if not self.control_conformity() :
            raise ValueError("La vidéo ne respecte pas les critères de conformité : langue française et au moins 200 commentaires.")
        else :
            # Paramètres initiaux pour la requête
            comments_data = []
            next_page_token = None

            with APIInteraction() as api_interaction :
                while True:
                    response = api_interaction.api_client.commentThreads().list(
                    part="snippet",
                    videoId=self.video_id,
                    maxResults=self.maxresults,
                    order="time",
                    textFormat="plainText",
                    pageToken=next_page_token
                    ).execute()
                    # Ajouter les commentaires récupérés à la liste
                    extraction_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    for item in response.get("items", []):
                        comment_info = item["snippet"]["topLevelComment"]["snippet"]
                        author_channel_id = comment_info.get("authorChannelId", {}).get("value")
                        # Vérifier si le commentaire est celui de l'auteur de la vidéo :
                        if self.channel_id == author_channel_id: 
                            # si le commentaire est celui de l'auteur de la vidéo, on ne le prend pas en compte pour l'analyse
                            continue # on passe au suivant 
                        
                        comments_data.append({
                            "url": self.video_url,
                            "id": item["id"],
                            "titre" : self.video_title,
                            "channelId": comment_info.get("channelId"),
                            "videoId": comment_info.get("videoId"),	
                            "publishedAt": comment_info.get("publishedAt"),
                            "comment": comment_info.get("textOriginal"),
                            "likeCount": comment_info.get("likeCount"),
                            "extractedAt": extraction_date
                        })

                    # Vérifier s'il y a une page suivante
                    # time.sleep(5)
                    next_page_token = response.get("nextPageToken")
                    if not next_page_token:
                        break
                    time.sleep(0.5)

            print(f'data uploaded : {len(comments_data)} commentaires au total')
            return comments_data

    # Fonction pour créer un DataFrame à partir des données collectées
    def to_data_table(self)-> pd.DataFrame:
        # Création du DataFrame à partir des données collectées
        df = pd.DataFrame(self.get_data())
        # print(df.head())
        print(f"Total de commentaires récupérés : {df.shape[0]}")
        return df
    

    def main_extraction(self):
        df = self.to_data_table()
        return df, self.channel_id
    
class DataMedaillonStorage :
    """
    Classe de stockage des données collectées dans une base de données MongoDB Atlas.
    Cette classe utilise un gestionnaire de contexte pour garantir que la connexion à la base de données est correctement fermée après utilisation, même en cas d'erreur.

    exemple d'utilisation :
    with DataMedaillonStorage(data, video_id, channel_id) as storage:
        storage.save_bronze(data)
        

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données à stocker
        video_id (str): L'ID de la vidéo YouTube associée aux données
        channel_id (str): L'ID de la chaîne YouTube associée aux données
    """
    def __init__(self, channel_id:str, video_id:str):
        self.channel_id = channel_id
        self.video_id = video_id
        self.db_interaction = None # instance de la classe DatabaseInteraction pour gérer les interactions avec la base de données MongoDB Atlas. # Cette variable sera initialisée dans la méthode __enter__ du gestionnaire de contexte, où la connexion à la base de données sera établie. En utilisant un gestionnaire de contexte, on s'assure que la connexion à la base de données est correctement fermée après utilisation, même en cas d'erreur.


    def __enter__(self):
        try :
            """Ouvre la connexion MongoDB et sélectionne la base de la chaîne."""
            self.db_interaction = DatabaseInteraction()
            self.db_interaction.__enter__() # ouvrir la connexion à la base de données
            # sélectionne (ou crée) la base de données de cette chaîne
            # MongoDB crée la DB automatiquement au premier insert
            self.db = self.db_interaction.client[self.channel_id]
            print(f"Connecté à la base : {self.channel_id}")
            return self
        
        except Exception as e:
            print(f"Erreur lors de l'établissement de la connexion à MongoDB Atlas : {e}")
            raise
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme la connexion MongoDB proprement."""
        if self.db_interaction:
            self.db_interaction.__exit__(exc_type, exc_val, exc_tb)
        return False
    

    def _get_collection(self, layer: str ):
        """
        Retourne la collection MongoDB pour une couche donnée.

        Args:
            layer: "bronze", "silver" ou "gold"
        Returns:
            collection MongoDB
        """
        if layer not in ("bronze", "silver", "gold"):
            raise ValueError(f"Couche invalide : {layer}. Choisir bronze, silver ou gold.")
        return self.db[layer]
    
    
    def check_existing_video(self, layer: str = "bronze") -> bool:
        """
        Vérifie si les données d'une vidéo existent déjà dans une couche.
        Évite les doublons lors des extractions répétées.

        Args:
            video_id: ID de la vidéo YouTube
            layer: couche à vérifier (défaut: bronze)
        Returns:
            True si des données existent déjà, False sinon
        """
        collection = self._get_collection(layer)
        count = collection.count_documents({"videoId": self.video_id})
        return True if count > 0 else False
    

    def add_metadata(self, data: list, layer: str) -> list:
        """
        Ajoute des métadonnées à chaque document avant l'insertion.

        Args:
            data: liste de documents à insérer
            layer: couche dans laquelle les données seront insérées (bronze, silver ou gold)
        Returns:
            liste de documents enrichis avec les métadonnées
        """
        for doc in data:
            if "metadata" not in doc:
                doc["metadata"] = {}
            doc["metadata"]["layer"]= layer
        return data
    

    def db_insert(self, data: list, layer: str ):

        if self.check_existing_video(layer=layer):
            print(f"Les données de la vidéo {self.video_id} existent déjà dans la couche {layer}. Insertion ignorée.")
            return
        
        collection = self._get_collection(layer)
        documents = self.add_metadata(data,layer)
        collection.insert_many(documents)


    def load_data(self, layer: str, video_id: str) -> list:
        """
        Charge les données d'une vidéo depuis une couche.

        Args:
            layer: couche à partir de laquelle charger les données (bronze, silver ou gold)
            video_id: ID de la vidéo YouTube
        Returns:
            liste de documents correspondant à la vidéo dans la couche spécifiée
        """
        if not self.check_existing_video(video_id=video_id, layer=layer) :
            print(f"Aucune donnée trouvée pour la vidéo {video_id} dans la couche {layer}.")
            return []
        collection = self._get_collection(layer)
        documents = list(collection.find({"videoId": video_id}))
        return documents

    def maj():
        pass

def etl():
    pass