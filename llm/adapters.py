from google.genai import types

def json_to_part(json_data: list[dict]):
    """
    Convierte una lista de diccionarios JSON personalizados a una lista de
    objetos types.Content de la librería google.genai.
    """
    adapted_list = []

    for data in json_data:
        role = data['role']
        parts = data['parts']

        parts_adapted = []

        for part in parts:
            part_type = part.get("part_type")
            content = part.get("content")

            if part_type == "function_call":
                parts_adapted.append(
                    types.Part(
                        function_call=types.FunctionCall(**content)
                    )
                )
            elif part_type == "function_response":
                # from_function_response ya crea el Part con la respuesta correctamente
                parts_adapted.append(
                    types.Part.from_function_response(
                        name=content.get("name"),
                        response=content.get("response") # Asegurarse de pasar el diccionario de respuesta
                    )
                )
            elif part_type == "message":
                parts_adapted.append(
                    types.Part(
                        text=content.get("text")
                    )
                )
            else:
                # Manejar otros tipos de part_type si los hay, o lanzar un error
                print(f"Advertencia: Tipo de parte desconocido '{part_type}'. Se ignorará.")
                pass # O levanta un error si el tipo es inesperado

        adapted_list.append(
            types.Content(
                role=role,
                parts=parts_adapted
            )
        )
    
    return adapted_list

def part_to_json(parts_data: list[types.Content]):
    """
    Convierte una lista de objetos types.Content de la librería google.genai
    de vuelta a la estructura de diccionarios JSON personalizada.
    """
    json_list = []

    for content_obj in parts_data:
        role = content_obj.role
        json_parts = []

        for part_obj in content_obj.parts:
            json_part = {}
            if part_obj.function_call:
                json_part["part_type"] = "function_call"
                json_part["content"] = {
                    "name": part_obj.function_call.name,
                    "args": part_obj.function_call.args
                }
            elif part_obj.function_response:
                json_part["part_type"] = "function_response"
                json_part["content"] = {
                    "name": part_obj.function_response.name,
                    "response": part_obj.function_response.response
                }
            elif part_obj.text:
                json_part["part_type"] = "message"
                json_part["content"] = {
                    "text": part_obj.text
                }
            
            json_parts.append(json_part)
        
        json_list.append({
            "role": role,
            "parts": json_parts
        })
    
    return json_list