from .message_model import Message

class Chat(list[Message]):
    
    def to_json(self):
        """
        Convierte el objeto Chat a un diccionario JSON.
        
        Returns:
            dict: Un diccionario que representa el objeto Chat.
        """
        return [message.to_json() for message in self]
    
