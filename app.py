import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Google API key
GOOGLE_API_KEY = "AIzaSyCyu_KdUnR8wV3LLpuJE67IL8W2htwGcT0"
genai.configure(api_key=GOOGLE_API_KEY)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    model = genai.GenerativeModel(model_name="gemini-pro")
    response_content = model.generate_content(prompt)
    bot_response = response_content.text

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
