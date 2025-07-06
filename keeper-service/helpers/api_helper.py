import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()
class FirestoreAPI:
    """
    Una clase de ayuda para interactuar con Firebase Firestore.
    """

    def __init__(self, credentials_path):
        """
        Inicializa la conexión con Firebase Firestore.

        Args:
            credentials_path (str): La ruta al archivo JSON de credenciales de Firebase.
        """
        try:
            # Evita la reinicialización si ya existe una app
            if not firebase_admin._apps:
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("✅ Conexión con Firestore establecida exitosamente.")
        except Exception as e:
            print(f"🔥 Error al inicializar Firebase: {e}")
            self.db = None

    def create_document(self, collection_id, data, document_id=None):
        """
        Crea un nuevo documento en una colección específica.

        Args:
            collection_id (str): El nombre de la colección.
            data (dict): Un diccionario con los datos del documento.
            document_id (str, optional): El ID personalizado para el documento. 
                                        Si es None, Firestore generará uno automáticamente.

        Returns:
            str: El ID del documento creado o None si hubo un error.
        """
        try:
            if document_id:
                doc_ref = self.db.collection(collection_id).document(document_id)
                doc_ref.set(data)
                return doc_ref.id
            else:
                # Firestore genera un ID automáticamente
                doc_ref = self.db.collection(collection_id).add(data)
                return doc_ref[1].id # add() retorna una tupla (timestamp, doc_ref)
        except Exception as e:
            print(f"🔥 Error al crear el documento: {e}")
            return None

    def read_document(self, collection_id, document_id):
        """
        Lee un documento específico de una colección.

        Args:
            collection_id (str): El nombre de la colección.
            document_id (str): El ID del documento a leer.

        Returns:
            dict: Los datos del documento o None si no se encuentra o hay un error.
        """
        try:
            doc_ref = self.db.collection(collection_id).document(document_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                print(f"ℹ️ No se encontró el documento con ID: {document_id}")
                return None
        except Exception as e:
            print(f"🔥 Error al leer el documento: {e}")
            return None

    def update_document(self, collection_id, document_id, data):
        """
        Actualiza un documento existente en una colección.

        Args:
            collection_id (str): El nombre de la colección.
            document_id (str): El ID del documento a actualizar.
            data (dict): Un diccionario con los campos a actualizar.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        try:
            doc_ref = self.db.collection(collection_id).document(document_id)
            doc_ref.update(data)
            return True
        except Exception as e:
            print(f"🔥 Error al actualizar el documento: {e}")
            return False

    def delete_document(self, collection_id, document_id):
        """
        Elimina un documento de una colección.

        Args:
            collection_id (str): El nombre de la colección.
            document_id (str): El ID del documento a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        try:
            self.db.collection(collection_id).document(document_id).delete()
            return True
        except Exception as e:
            print(f"🔥 Error al eliminar el documento: {e}")
            return False

    def filter_documents(self, collection_id, field, operator, value):
        """
        Filtra documentos en una colección basados en una condición.

        Args:
            collection_id (str): El nombre de la colección.
            field (str): El campo por el cual filtrar.
            operator (str): El operador de comparación (ej. '==', '<', '>', etc.).
            value: El valor a comparar.

        Returns:
            list: Una lista de diccionarios, cada uno representando un documento que cumple la condición.
                  Retorna una lista vacía si no hay coincidencias o hay un error.
        """
        try:
            docs = self.db.collection(collection_id).where(field, operator, value).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"🔥 Error al filtrar documentos: {e}")
            return []
        
# Obtiene la ruta de las credenciales desde una variable de entorno,
# con un valor por defecto para desarrollo local.
credentials_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH", "key/keeper-buddy-eac2edfeddc3.json")
db = FirestoreAPI(credentials_path)