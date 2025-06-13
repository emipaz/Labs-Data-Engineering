import base64
import json
import logging
import os
import random
from typing import Any

import urllib3

# URL del Lambda de inferencia, se obtiene de las variables de entorno
URL_LAMBDA_INFERENCE = os.getenv(
    "URL_LAMBDA_INFERENCE",
    "",
)

# Límite de artículos a recomendar, también de las variables de entorno
ITEM_LIMIT = os.getenv(
    "ITEM_LIMIT",
    5,
)

# Semilla para la aleatoriedad, se utiliza para garantizar resultados reproducibles
RANDOM_SEED = os.getenv("RANDOM_SEED", 42)

random.seed(RANDOM_SEED)

# Configuración del logger para registrar información
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def decode_record(record: bytes) -> dict:
    """Decodifica el registro leído desde el flujo de datos de Kinesis.
    
    Args:
        record (bytes): Registro leído desde el flujo de datos de Kinesis.
    
    Returns:
        dict: Datos decodificados.
    """
    string_data = base64.b64decode(record).decode("utf-8")
    return json.loads(string_data)


def get_user_embedding(
    url: str,
    data: list[dict],
) -> Any:
    """Llama a la función Lambda de inferencia con el endpoint de embeddings de usuario para obtener
    el embedding de un usuario.
    
    Args:
        url (str): URL para la Lambda de Inferencia.
        data (list[dict]): Lista con los datos del usuario.
    
    Returns:
        Any: Diccionario con el vector de embedding del usuario solicitado.
    """

    url_call = f"{url}/user_embeddings"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    http = urllib3.PoolManager()

    response = http.request(
        "POST",
        url_call,
        headers=headers,
        body=json.dumps(data).encode("utf-8"),  # Envía los datos en formato JSON
    )
    # Devuelve la respuesta como un diccionario
    return json.loads(response.data)


def get_item_from_user(url: str, data: dict, item_limit: int) -> Any:
    """Recibe un embedding de usuario y llama al endpoint items_from_user de la Lambda de inferencia
    para devolver una lista de artículos recomendados.
    
    Args:
        url (str): URL para la Lambda de Inferencia.
        data (dict): Diccionario con el vector de embedding del usuario.
        item_limit (int): Número máximo de artículos a recomendar.
    
    Returns:
        Any: Lista de diccionarios con las recomendaciones de artículos. 
              El formato para cada artículo es id y score.
    """

    url_call = f"{url}/items_from_user?limit={item_limit}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    http = urllib3.PoolManager()

    response = http.request(
        "POST",
        url_call,
        headers=headers,
        body=json.dumps(data).encode("utf-8"),
    )

    return json.loads(response.data)


def get_item_from_item(url: str, item_id: str, item_limit: int) -> Any:
    """Usando un ID de artículo, recomienda los más similares.
    
    Args:
        url (str): URL para la Lambda de Inferencia.
        item_id (str): ID del artículo para encontrar similares.
        item_limit (int): Número máximo de artículos a recomendar.
    
    Returns:
        Any: Lista de artículos similares al artículo dado.
    """
    # Construye la URL para la llamada
    url_call = f"{url}/items_from_item?item_id={item_id}&limit={item_limit}"

    headers = {
        "accept": "application/json",
    }

    # Crea un gestor de conexiones HTTP
    http = urllib3.PoolManager()
    
    # Realiza una solicitud GET
    response = http.request("GET", url_call, headers=headers)

    # Decodifica la respuesta JSON
    decoded_response = json.loads(response.data)

    # Devuelve la respuesta decodificada
    return decoded_response


def lambda_handler(event, context):
    """Función principal que maneja el evento de Lambda.
    
    Args:
        event: Contiene los registros de entrada.
        context: Proporciona información sobre la ejecución de la función Lambda.
    
    Returns:
        dict: Diccionario con los registros procesados.
    """
    
    logger.info(
        f"Manejador de transformación de órdenes invocado con registros {event['records'][:2]}"
    )

    # Lista para almacenar los registros de salida
    output = [] 
    
    for record in event["records"]:
        # Decodifica el registro
        payload = decode_record(record["data"])

        usr_dict = [
            {
                "city": payload.get("city"),                # Obtiene la ciudad del usuario
                "country": payload.get("country"),          # Obtiene el país del usuario
                "creditlimit": payload.get("credit_limit"), # Obtiene el límite de crédito del usuario
            }
        ]

        # Obtiene el embedding del usuario
        usr_emb = get_user_embedding(url=URL_LAMBDA_INFERENCE, data=usr_dict)

        # Recomendando artículos para el usuario
        recommended_items = get_item_from_user(
            url=URL_LAMBDA_INFERENCE,
            data=usr_emb[0],
            item_limit=int(ITEM_LIMIT),
        )

        # Eligiendo uno de los artículos que el usuario tiene en su historial y encontrando artículos similares para recomendar
        
        # Selecciona un artículo al azar del historial
        selected_item = random.choice(payload["browse_history"])

        similar_items = get_item_from_item(
            url=URL_LAMBDA_INFERENCE,
            item_id=selected_item["product_code"], # ID del artículo seleccionado
            item_limit=int(ITEM_LIMIT), 
        )

        # Agrega las recomendaciones y artículos similares al payload
        payload["recommended_items"] = recommended_items
        payload["similar_items"] = {
            "product_code": selected_item["product_code"],
            "similar_items": similar_items,
        }

        # Crea un registro de salida
        output_record = {
            "recordId": record["recordId"],
            "result": "Ok",
            "data": base64.b64encode(json.dumps(payload).encode("utf-8")),
        }
        output.append(output_record) # Agrega el registro de salida a la lista

        # Registra los primeros registros procesados
        logger.info(f"Registros procesados {output[:2]}")

    #   Devuelve los registros procesados
    return {"records": output}
