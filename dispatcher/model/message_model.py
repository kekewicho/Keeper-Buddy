class Message:
    """
    Parsea un objeto Content JSON de Gemini para identificar rápidamente su tipo
    (texto, llamada a función, o respuesta de función) y acceder a sus datos.
    """

    def __init__(self, content_json: dict):
        """
        Inicializa el parser con el JSON de un objeto Content de Gemini.

        Args:
            content_json (dict): El diccionario JSON que representa una parte
                                 del contenido de la conversación (e.g., {'role': 'user', 'parts': [...]}).
        Raises:
            ValueError: Si el JSON de entrada no tiene la estructura esperada de 'parts'.
        """
        self._content_json = content_json
        self.is_text = False
        self.is_function_call = False
        self.is_function_response = False
        self.text_content = None
        self.function_call_data = None
        self.function_response_data = None
        self.raw_parts = []
        self.role = content_json.get("role", "unknown")

        if not isinstance(content_json, dict) or "parts" not in content_json:
            raise ValueError("El JSON de entrada debe ser un diccionario con una clave 'parts'.")
        
        self.raw_parts = content_json["parts"]
        self._parse_parts()

    def _parse_parts(self):
        """
        Método interno para analizar las 'parts' del contenido y determinar el tipo.
        """
        for part in self.raw_parts:
            if "text" in part and part["text"] is not None:
                self.is_text = True
                self.text_content = part["text"]
                break
            elif "function_call" in part and part["function_call"] is not None:
                self.is_function_call = True
                self.function_call_data = part["function_call"]
                break
            elif "function_response" in part and part["function_response"] is not None:
                self.is_function_response = True
                self.function_response_data = part["function_response"]
                break
            
    def __repr__(self):
        """Representación para depuración."""
        type_str = []
        if self.is_text: type_str.append("TEXT")
        if self.is_function_call: type_str.append("FUNCTION_CALL")
        if self.is_function_response: type_str.append("FUNCTION_RESPONSE")
        
        return (f"GeminiContentParser(type={'/'.join(type_str) or 'UNKNOWN'}, "
                f"text='{self.text_content}...' if self.text_content else '', "
                f"func_call={self.function_call_data}, "
                f"func_resp={self.function_response_data})")
    

    def to_json(self):
        """
        Convierte el objeto Message a un diccionario JSON.

        Returns:
            dict: Un diccionario que representa el objeto Message.
        """
        return self._content_json
