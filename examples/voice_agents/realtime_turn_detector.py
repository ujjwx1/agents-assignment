import logging

from dotenv import load_dotenv
from google.genai import types  # noqa: F401

from livekit.agents import Agent, AgentServer, AgentSession, JobContext, JobProcess, cli
from livekit.plugins import deepgram, google, openai, silero  # noqa: F401
from livekit.plugins.turn_detector.multilingual import MultilingualModel


IGNORE_WORDS = {"yeah", "ok", "okay", "hmm", "uh-huh", "right"}
INTERRUPT_WORDS = {"stop", "wait", "no", "cancel", "hold"}


class SemanticInterruptAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_user_message(self, message: str, session: AgentSession):
        text = message.lower()

        if any(word in text for word in INTERRUPT_WORDS):
            await session.interrupt()   # HARD STOP
            return message

        if session.is_speaking and all(word in IGNORE_WORDS for word in text.split()):
            # Ignore backchanneling while speaking
            return None

        return message



logger = logging.getLogger("realtime-turn-detector")
logger.setLevel(logging.INFO)

load_dotenv()

## This example demonstrates how to use LiveKit's turn detection model with a realtime LLM.
## Since the current turn detection model runs in text space, it will need to be combined
## with a STT model, even though the audio is going directly to the Realtime API.
## In this example, speech is being processed in parallel by both the STT and the realtime API

server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(
        allow_interruptions=False,
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        # To use OpenAI Realtime API
        llm=openai.realtime.RealtimeModel(
            voice="alloy",
            # it's necessary to turn off turn detection in the OpenAI Realtime API in order to use
            # LiveKit's turn detection model
            turn_detection=None,
            input_audio_transcription=True,  # we use Deepgram STT instead
        ),
        # To use Gemini Live API
        # llm=google.realtime.RealtimeModel(
        #     realtime_input_config=types.RealtimeInputConfig(
        #         automatic_activity_detection=types.AutomaticActivityDetection(
        #             disabled=True,
        #         ),
        #     ),
        #     input_audio_transcription=None,
        # ),
    )
    await session.start(agent=SemanticInterruptAgent(instructions="You are a helpful assistant."), room=ctx.room)


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm

if __name__ == "__main__":
    cli.run_app(server)
