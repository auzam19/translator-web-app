from flask import Flask, render_template, request, jsonify
from translations import translate_text
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
app.config['AUDIO_FOLDER'] = 'static/audio'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')
    
    translated = translate_text(text, target_lang)
    return jsonify({'translated': translated})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    tts = gTTS(text=text, lang=lang)
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(app.config['AUDIO_FOLDER'], filename)
    tts.save(filepath)

    return jsonify({'audio_path': f"/static/audio/{filename}"})

if __name__ == '__main__':
    if not os.path.exists(app.config['AUDIO_FOLDER']):
        os.makedirs(app.config['AUDIO_FOLDER'])
    # Bind to 0.0.0.0 for Railway deployment
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
