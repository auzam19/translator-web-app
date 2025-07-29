@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    if lang not in ['en', 'si']:
        lang = 'en'

    try:
        if not os.path.exists(AUDIO_FOLDER):
            os.makedirs(AUDIO_FOLDER)

        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text=text, lang=lang, slow=True)  # Slowed down
        tts.save(filepath)

        return jsonify({'audio_path': f"/static/audio/{filename}"})
    except Exception as e:
        return jsonify({'error': str(e)})
