import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your Google API key
GOOGLE_API_KEY = "AIzaSyCyu_KdUnR8wV3LLpuJE67IL8W2htwGcT0"  # Replace this with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# HTML template for the front end with enhanced styling and loading animation
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Me Chat Bot</title>
    <style>
        body { font-family: 'Roboto', sans-serif; background-color: #eaeff1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; padding: 0; color: #333; }
        #chatContainer { width: 90%; max-width: 500px; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); padding: 15px 20px; box-sizing: border-box; display: flex; flex-direction: column; }
        h1 { font-size: 1.5em; color: #444; text-align: center; margin-bottom: 20px; }
        #messages { flex: 1; overflow-y: auto; height: 400px; padding-right: 10px; margin-bottom: 15px; }
        .message { display: flex; align-items: center; padding: 8px 10px; margin: 8px 0; border-radius: 18px; font-size: 0.95em; line-height: 1.5; max-width: 75%; position: relative; word-wrap: break-word; }
        .user { background-color: #dcf8c6; color: #333; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background-color: #f1f0f0; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; }
        .avatar { width: 30px; height: 30px; border-radius: 50%; margin: 0 10px; }
        .bot .avatar { background: #dfe3e6; }
        .typing { width: 10px; height: 10px; background: #b0b3b5; border-radius: 50%; display: inline-block; margin: 0 2px; animation: blink 0.8s linear infinite alternate; }
        @keyframes blink { from { opacity: 1; } to { opacity: 0.3; } }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #dee2e6; border-radius: 20px; margin-top: 5px; font-size: 1em; }
        button { width: 100%; padding: 10px; border: none; background-color: #128c7e; color: white; font-size: 1em; font-weight: bold; border-radius: 20px; cursor: pointer; margin-top: 10px; }
        button:hover { background-color: #075e54; }
        #clearBtn { background-color: #d9534f; margin-top: 5px; }
        #clearBtn:hover { background-color: #c9302c; }
    </style>
</head>
<body>
    <div id="chatContainer">
        <h1>Ask Abdul Hajees</h1>
        <div id="messages"></div>
        <input type="text" id="prompt" placeholder="Type your question...">
        <button id="generateBtn">Send</button>
        <button id="clearBtn">Clear Chat</button>
    </div>

    <script>
        function loadChatHistory() {
            const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
            chatHistory.forEach(({ content, sender }) => addMessage(content, sender));
        }

        function saveMessage(content, sender) {
            const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
            chatHistory.push({ content, sender });
            localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        }

        document.getElementById('clearBtn').addEventListener('click', () => {
            localStorage.removeItem('chatHistory');
            document.getElementById('messages').innerHTML = '';
        });

        function addMessage(content, sender) {
            const messagesElement = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            const text = document.createElement('span');
            text.className = 'message-content';
            text.textContent = content.trim();
            messageDiv.appendChild(text);
            messagesElement.appendChild(messageDiv);
            messagesElement.scrollTop = messagesElement.scrollHeight;
        }

        async function sendMessage() {
            const prompt = document.getElementById('prompt').value.trim();
            if (!prompt) return;

            addMessage(prompt, 'user');
            saveMessage(prompt, 'user');
            document.getElementById('prompt').value = '';

            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot';
            typingDiv.innerHTML = '<div class="typing"></div><div class="typing"></div><div class="typing"></div>';
            document.getElementById('messages').appendChild(typingDiv);

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: prompt }),
            });

            document.getElementById('messages').removeChild(typingDiv);

            if (response.ok) {
                const data = await response.json();
                addMessage(data.response, 'bot');
                saveMessage(data.response, 'bot');
            } else {
                addMessage('Error: Could not retrieve response.', 'bot');
            }
        }

        document.getElementById('prompt').addEventListener('keypress', function(event) {
            if (event.key === 'Enter') sendMessage();
        });

        document.getElementById('generateBtn').addEventListener('click', sendMessage);
        loadChatHistory();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

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

