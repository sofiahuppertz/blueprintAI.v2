from requests import get
from cs50 import SQL
import sqlite3
import uuid

# Function to generate an image based on a prompt description
def generate_image(prompt_description, client, image_queue):
    try:
        # Generate an image using the OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_description,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        # Get the URL of the generated image
        image_url = response.data[0].url
        image_queue.put(image_url)
    except Exception as e:
        # If an error occurred, print the error and set image_url to None
        print(f"Error in generate_image: {str(e)}")
        
    return

    
def make_image_prompt(building_type, height, color_finishes, primary_materials, location_context, landscape_type, architectural_style, adiciones_ecologicas, additional_elements):
    # Define the template for the building description
    template = (
        "Eres un visualizador de edificios. Tu tarea es generar una imagen siguiendo la siguiente descripción con extrema precisión. "
        "El tipo de edificio es: {building_type}. "
        "La altura del edificio es: {height}. (Si es más alto que el costanera center, tiene que ser MUY alto, cómo los edificios más altos del mundo). "
        "El contexto de ubicación del edificio es (esto describe el entorno del edificio): {location_context}. "
        "El tipo de paisaje es: {landscape_type}. "
        "El estilo arquitectónico es: {architectural_style}. "
        "La fachada del edificio es: {color_finishes}. "
        "Los materiales principales del edificio son principalmente: {primary_materials}. "
        "La característica ecológica que debe ser visible y pertence al espacio del edificio (nota: un contendor es un basurero): {adiciones_ecologicas}. "
        "IMPORTANTE: Aquí hay algunos elementos adicionales para agregar al edificio: {additional_elements}. "
        "NO ESCRIBAS TEXTO EN LA IMAGEN. "
        "Haz que el modelo sea de alta calidad y alta resolución. "
        "La vista es desde un ángulo superior al del edificio, por lo que debe mostrar el techo, la fachada y la calle, y la característica ecológica adicional debe ser visible."
    )
    # Fill in the placeholders in the template with the form values
    prompt = template.format(
        height=height,
        building_type=building_type,
        color_finishes=color_finishes,
        location_context=location_context,
        landscape_type=landscape_type,
        architectural_style=architectural_style,
        adiciones_ecologicas=adiciones_ecologicas,
        primary_materials=primary_materials,
        additional_elements=additional_elements,
    )
    print(prompt)
    # Return the prompt
    return prompt