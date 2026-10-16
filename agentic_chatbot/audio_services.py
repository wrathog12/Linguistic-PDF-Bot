"""Audio Services Module

Provides ASR (Automatic Speech Recognition) and TTS (Text-to-Speech)
functionality using Groq Whisper and Murf AI respectively.
"""

from groq import AsyncGroq
from config import GROQ_API_KEY, ASR_MODEL, MURF_API_KEY
from murf import AsyncMurf

# Initialize async clients
groq = AsyncGroq(api_key=GROQ_API_KEY)



async def groq_asr_bytes(audio_bytes: bytes, model: str = ASR_MODEL, language: str = "en") -> str:
    """Transcribe audio bytes to text using Groq Whisper ASR.

    Args:
        audio_bytes: Raw audio data in WAV format.
        model: ASR model identifier (default: whisper-large-v3-turbo).
        language: Language code for transcription (default: "en").

    Returns:
        Transcribed text string.
    """
    resp = await groq.audio.transcriptions.create(
        model=model,
        file=("audio.wav", audio_bytes, "audio/wav"),
        response_format="text",
        language=language
    )
    return resp

murf_client = AsyncMurf(api_key=MURF_API_KEY)

async def murf_tts(text: str, voice_id: str = "en-US-natalie", format: str = "MP3") -> bytes:
    """Convert text to speech audio using Murf AI neural voices.

    Args:
        text: The text content to synthesize into speech.
        voice_id: Murf voice identifier (default: "en-US-natalie").
        format: Audio output format (default: "MP3").

    Returns:
        Complete audio data as bytes.
    """
    resp = murf_client.text_to_speech.stream(
        text=text,
        voice_id=voice_id,
        format=format,
        sample_rate=44100.0
    )
    chunks = [chunk async for chunk in resp]
    full_audio = b''.join(chunks)
    return full_audio
   