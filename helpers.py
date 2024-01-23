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

    
def make_image_prompt(building_type, height, color_finishes, primary_materials, location_context, landscape_type, architectural_style, quality_tier, additional_elements):
    # Define the template for the building description
    template = (
        "You are a building visualizer. Your task is to generate an image with the following description with extreme accuracy."
        "The building type is: {building_type}. "
        "The building height is: {height} "
        "The building location context is (This describes the building's surroundings): {location_context}. "
        "The landscape type is: {landscape_type}. "
        "The building design quality is: {quality_tier}, where the available options are standard, premium and luxury. "
        "The architectural style is: {architectural_style}. "
        "The building facade is: {color_finishes}. "
        "The building materials are mostly: {primary_materials}. "
        "Here are some additional elements to add to the building: {additional_elements}. "
        "DO NOT WRITE TEXT ON THE IMAGE. "
        "Make the model high quality and high resolution. "
        "The view is from a higher angle than the building, so we can see the roof top, but also the facade and the street. "
        "The sky is blue, like a sunny and colorful day."
    )
    # Fill in the placeholders in the template with the form values
    prompt = template.format(
        height=height,
        building_type=building_type,
        color_finishes=color_finishes,
        location_context=location_context,
        landscape_type=landscape_type,
        architectural_style=architectural_style,
        quality_tier=quality_tier,
        primary_materials=primary_materials,
        additional_elements=additional_elements,
    )
    # Return the prompt
    return prompt