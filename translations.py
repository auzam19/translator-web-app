from googletrans import Translator

translator = Translator()

def detect_singlish(text):
    sinhala_like = ['mata', 'koheda', 'yanna', 'kawda']
    return any(word in text.lower() for word in sinhala_like)

def translate_text(text, target_lang='en'):
    try:
        if detect_singlish(text):
            return text.replace("mata", "to me").replace("koheda", "where").replace("yanna", "to go").replace("kawda", "who")
        else:
            result = translator.translate(text, dest=target_lang)
            return result.text
    except Exception as e:
        return f"[Translation error: {str(e)}]"
