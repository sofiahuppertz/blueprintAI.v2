from flask import Flask, render_template, request, jsonify, send_file, redirect
from helpers import generate_image, make_image_prompt
import os
from openai import OpenAI
from queue import Queue
import requests
from threading import Thread


# Configure application
app = Flask(__name__)

image_queue = Queue()

building_description = ""

# OpenAI API Client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html"), 200



@app.route('/web', methods=['POST'])
def web():
    return redirect("https://imakro.cl", code=302)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    building_type = request.form.get("buildingType")
    height = request.form.get("heightStories")
    color_finishes = request.form.get("colorFinishes")
    primary_materials = request.form.get("primaryMaterials")
    location_context = request.form.get("locationContext")
    landscape_type = request.form.get("landscapeType")
    architectural_style = request.form.get("architecturalStyle")
    adiciones_ecologicas = request.form.get("adicionesEcologicas")
    additional_elements = request.form.get("additionalElements")

    prompt = make_image_prompt(building_type, height, color_finishes, primary_materials, location_context, landscape_type, architectural_style, adiciones_ecologicas, additional_elements)
    thread = Thread(target=generate_image, args=(prompt, client, image_queue))
    thread.start()
    return jsonify({'new_text': 'CARGANDO ...'})


@app.route("/check_image")
def check_image():
    if not image_queue.empty():
        image_url = image_queue.get()
        if image_url is None:
            print("No image URL available")
            return jsonify({'status': 'no image'}), 204
        else:
            print("Image URL: ", image_url)
            return jsonify({'status': 'image ready', 'image_url': image_url}), 302
    else:
        return jsonify({'status': 'no image'}), 204
    

@app.route('/download_image')
def download_image():
    image_url = request.args.get('image_url')
    response = requests.get(image_url, stream=True)
    return send_file(response.raw, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)