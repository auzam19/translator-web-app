from flask import Flask, render_template, request, jsonify
from translations import translate_text
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# Set audio folder path
AUDIO_FOLDER = 'static/audio'
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Translation route
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'en')

    translated = translate_text(text, target_lang)
    return jsonify({'translated': translated})

# Text-to-speech route
@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    # Fallback if unsupported language
    if lang not in ['en', 'si']:
        lang = 'en'

    try:
        # Ensure the audio folder exists
        if not os.path.exists(AUDIO_FOLDER):
            os.makedirs(AUDIO_FOLDER)

        # Generate a unique filename
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        # Generate speech (slower for clarity)
        tts = gTTS(text=text, lang=lang, slow=True)
        tts.save(filepath)

        return jsonify({'audio_path': f"/static/audio/{filename}"})
    except Exception as e:
        return jsonify({'error': str(e)})

# Run app with correct host/port
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
