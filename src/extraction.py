
from pymongo.mongo_client import MongoClient
from googleapiclient.discovery import build
from pymongo.server_api import ServerApi
from contextlib import contextmanager
from dotenv import load_dotenv
import certifi
import os
load_dotenv()



class DatabaseInteraction:
    """
    DATA BASE INTERACTION :

    Classe permettant d'interagir avec la base de données MongoDB Atlas, notamment pour établir une connexion sécurisée et gérer les ressources de manière efficace.
    Cette classe est destinée à être utilisée dans un contexte de gestion de ressources (avec l'instruction "with") pour garantir que la connexion à la base de données est correctement fermée après utilisation, même en cas d'erreur.

    Paramètres
    ----------
    - **username** : (str)
        Le nom d'utilisateur pour se connecter à la base de données, 
        récupéré à partir des variables d'environnement.
    - **password** : (str)
        Le mot de passe pour se connecter à la base de données, 
        également récupéré à partir des variables d'environnement.
    
    Exemple d'utilisation
    ---------------------
    ::

        with DatabaseInteraction() as db_interaction:
            # Utiliser db_interaction.client pour interagir avec la base de données
            # Par exemple, accéder à une collection :
            collection = db_interaction.client['nom_de_la_base']['nom_de_la_collection']
            # Effectuer des opérations sur la collection...
        
        # Fin du bloc "with" : la connexion est automatiquement fermée
        # grâce à la méthode __exit__ de la classe DatabaseInteraction.
    """

    def __init__(self):
        self.username = os.getenv('MDB_USERNAME')
        self.password = os.getenv('MDB_PASSWORD')


    def __enter__(self):
        """
        Connexion à la base de données MongoDB Atlas :
        Cette fonction établit une connexion à la base de données MongoDB Atlas en utilisant l'URI de connexion fourni.

        """
        # création du client
        uri = f"mongodb+srv://{self.username}:{self.password}@cluster1.n9aag2m.mongodb.net/?appName=Cluster1"
        
        # try:
        #     self.client = MongoClient(uri, server_api=ServerApi('1'))
            
        # except Exception as e:
        try :
            self.client = MongoClient(uri, tlsCAFile=certifi.where())

        except Exception as e:
            print(f"Erreur lors de la création du client MongoDB Atlas : {e}")
            raise
        # Test de connexion
        try:
            self.client.admin.command('ping')
            print("Connexion MongoDB Atlas réussie")
            return self
            # return client
        except Exception as e:
            print(f"Erreur de connexion à MongoDB Atlas : {e}")
            raise


    def __exit__(self, exc_type, exc_val, exc_tb):
        # Fermer la connexion à la base de données
        if self.client:
            self.client.close()
            print("Connexion MongoDB Atlas fermée")
        return False


# @contextmanager
# option à tester


class APIInteraction:
    """
    API INTERACTION :

    Classe destinée à gérer les interactions avec une API, notamment pour établir une connexion sécurisée et gérer les ressources de manière efficace.
    Cette classe est conçue pour être utilisée dans un contexte de gestion de ressources (avec l'instruction "with") afin de garantir que les connexions à l'API sont correctement fermées après utilisation, même en cas d'erreur.

    Paramètres
    ----------
    - **api_key** : (str)
        La clé d'API nécessaire pour authentifier les requêtes auprès de l'API, 
        récupérée à partir des variables d'environnement.
    
    Exemple d'utilisation
    ---------------------
    ::

        with APIInteraction() as api_interaction:
            # Utiliser api_interaction.api_key pour interagir avec l'API
            # Par exemple, effectuer une requête API :
            response = response = api_interaction.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="time",
            textFormat="plainText",
            pageToken=next_page_token
            ).execute()
            # Traiter la réponse...
        
        # Fin du bloc "with" : la connexion à l'API est automatiquement fermée
        # grâce à la méthode __exit__ de la classe APIInteraction.
    """

    def __init__(self):
        self.api_key = os.getenv('DEVELOPER_KEY')

    def __enter__(self):

        try :
            self.api_client = build("youtube", "v3", developerKey=self.api_key)
        except Exception as e:
            print(f"Erreur lors de la création du client API : {e}")
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.api_client:
            self.api_client.close()
            print("Connexion à l'API fermée")
        return False