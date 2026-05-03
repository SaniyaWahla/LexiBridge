from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LexiBridge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LANGUAGES = {
    "auto":  "Auto Detect",
    "af":    "Afrikaans",
    "sq":    "Albanian",
    "am":    "Amharic",
    "ar":    "Arabic",
    "hy":    "Armenian",
    "az":    "Azerbaijani",
    "bn":    "Bengali",
    "bs":    "Bosnian",
    "bg":    "Bulgarian",
    "ca":    "Catalan",
    "zh-CN": "Chinese (Simplified)",
    "zh-TW": "Chinese (Traditional)",
    "hr":    "Croatian",
    "cs":    "Czech",
    "da":    "Danish",
    "nl":    "Dutch",
    "en":    "English",
    "et":    "Estonian",
    "tl":    "Filipino",
    "fi":    "Finnish",
    "fr":    "French",
    "gl":    "Galician",
    "ka":    "Georgian",
    "de":    "German",
    "el":    "Greek",
    "gu":    "Gujarati",
    "ht":    "Haitian Creole",
    "iw":    "Hebrew",
    "hi":    "Hindi",
    "hu":    "Hungarian",
    "is":    "Icelandic",
    "id":    "Indonesian",
    "ga":    "Irish",
    "it":    "Italian",
    "ja":    "Japanese",
    "kn":    "Kannada",
    "kk":    "Kazakh",
    "ko":    "Korean",
    "lv":    "Latvian",
    "lt":    "Lithuanian",
    "ms":    "Malay",
    "ml":    "Malayalam",
    "mt":    "Maltese",
    "mr":    "Marathi",
    "mn":    "Mongolian",
    "ne":    "Nepali",
    "no":    "Norwegian",
    "fa":    "Persian",
    "pl":    "Polish",
    "pt":    "Portuguese",
    "pa":    "Punjabi",
    "ro":    "Romanian",
    "ru":    "Russian",
    "sr":    "Serbian",
    "si":    "Sinhala",
    "sk":    "Slovak",
    "sl":    "Slovenian",
    "so":    "Somali",
    "es":    "Spanish",
    "sw":    "Swahili",
    "sv":    "Swedish",
    "tg":    "Tajik",
    "ta":    "Tamil",
    "te":    "Telugu",
    "th":    "Thai",
    "tr":    "Turkish",
    "uk":    "Ukrainian",
    "ur":    "Urdu",
    "uz":    "Uzbek",
    "vi":    "Vietnamese",
    "cy":    "Welsh",
    "yi":    "Yiddish",
    "zu":    "Zulu",
}


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"


class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str
    detected_lang: str | None = None
    detected_lang_name: str | None = None
    char_count: int


@app.get("/")
def root():
    return {"message": "Translation API is running", "version": "1.0.0"}


@app.get("/languages")
def get_languages():
    return {"languages": LANGUAGES}



@app.post("/translate", response_model=TranslationResponse)
def translate(request: TranslationRequest):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(request.text) > 5000:
        raise HTTPException(status_code=400, detail="Text too long. Max 5000 characters.")
    if request.target_lang not in LANGUAGES or request.target_lang == "auto":
        raise HTTPException(status_code=400, detail=f"Unsupported target language: {request.target_lang}")

    detected_lang = None
    detected_lang_name = None
    source = request.source_lang

    try:
        if request.source_lang == "auto":
            try:
                detected_lang = detect(request.text)
                detected_lang_name = LANGUAGES.get(detected_lang, detected_lang.upper())
            except LangDetectException:
                detected_lang = "en"
                detected_lang_name = "English"

        translator = GoogleTranslator(source=source, target=request.target_lang)
        translated = translator.translate(request.text)

        if not translated:
            raise HTTPException(status_code=500, detail="Translation returned empty result")

        return TranslationResponse(
            translated_text=translated,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            detected_lang=detected_lang,
            detected_lang_name=detected_lang_name,
            char_count=len(request.text),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get("/detect")
def detect_language(text: str):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    try:
        lang_code = detect(text)
        lang_name = LANGUAGES.get(lang_code, lang_code.upper())
        return {"language_code": lang_code, "language_name": lang_name}
    except LangDetectException:
        raise HTTPException(status_code=400, detail="Could not detect language")