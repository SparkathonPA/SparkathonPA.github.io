from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import base64
import requests
from markdown import markdown
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Make sure upload folder exists
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create upload folder: {e}")


# OpenAI API Key
api_key = "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"

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_confidence(response_text):
    match = re.search(r'confidence.*?(\d+)%', response_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0

def get_allergen_info(image_path, allergies):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Can you identify this food? What ingredients might it contain and are there any possible food allergens in it? Known allergies: {allergies}. Also, provide a confidence score (0-100%) on how certain you are about the ingredients and allergens. If unsure, still provide likely ingredients based on common dishes."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 400
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        confidence_score = extract_confidence(content)

        if confidence_score < 99:
            explanation = "The AI is not fully confident about all ingredients and allergens in this dish. This may be due to factors such as blended sauces, enclosed food (e.g., burritos), or visually ambiguous ingredients. Below is a possible list of ingredients and allergens, but please verify manually."
            return f"**Possible Ingredients and Allergens:**\n{content}\n\n**Uncertain Identification:**\n\n{explanation}"
        else:
            return content
    else:
        return "Error processing the image. Please try again."

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    allergies = request.form.get('allergies')  # <-- Fixed here

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        result = get_allergen_info(file_path, allergies)
        result_html = markdown(result)
        return render_template('result.html', result=result_html)
    else:
        flash('Invalid file type or no file uploaded')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
