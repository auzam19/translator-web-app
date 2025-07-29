async function translateText() {
    const text = document.getElementById("inputText").value;
    const targetLang = document.getElementById("languageSelect").value;

    const response = await fetch('/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, target_lang: targetLang })
    });

    const data = await response.json();
    document.getElementById("outputText").innerText = data.translated;

    // Save translated text for speech
    window.latestTranslation = {
        text: data.translated,
        lang: targetLang
    };
}

function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // fallback to English
    recognition.interimResults = false;

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById("inputText").value = transcript;
    };

    recognition.onerror = function(event) {
        alert("Voice input error: " + event.error);
    };

    recognition.start();
}

async function playVoiceOutput() {
    if (!window.latestTranslation) {
        alert("Please translate something first.");
        return;
    }

    const response = await fetch('/speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: window.latestTranslation.text,
            lang: window.latestTranslation.lang
        })
    });

    const data = await response.json();
    const audio = new Audio(data.audio_path);
    audio.play();
}
