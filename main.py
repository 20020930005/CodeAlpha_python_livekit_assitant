import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from gtts import gTTS
import os

load_dotenv()

# Create a custom function to handle text-to-speech with gTTS
def gtts_tts(text: str, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")  # Saves the speech as an audio file
    os.system("start output.mp3")  # Plays the audio file using the default media player

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=( 
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    # Custom VoiceAssistant with gTTS instead of OpenAI TTS
    assistant = VoiceAssistant(
        vad=None,  # No VAD needed since we're not using silero
        stt=None,  # Not using STT for now, but you could add your preferred STT solution here
        llm=None,  # You can keep the LLM or modify it according to your use case
        tts=gtts_tts,  # Using gTTS for text-to-speech
        chat_ctx=initial_ctx,
        fnc_ctx=None,  # Modify as needed
    )

    assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hey, how can I help you today!", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

