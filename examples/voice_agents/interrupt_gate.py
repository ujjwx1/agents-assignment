import time
import os

IGNORE_WORDS = set(os.getenv("IGNORE_WORDS", "yeah,ok,okay,hmm,uh-huh,right").split(","))
INTERRUPT_WORDS = set(os.getenv("INTERRUPT_WORDS", "stop,wait,no,cancel,hold").split(","))
VALIDATION_MS = int(os.getenv("INTERRUPTION_VALIDATION_MS", "200"))


class InterruptGate:
    def __init__(self, session):
        self.session = session
        self.pending = False
        self.vad_time = None

    def on_vad(self):
        # VAD fired while agent may be speaking
        if not self.session.is_speaking:
            return
        self.pending = True
        self.vad_time = time.time() * 1000

    async def on_stt_final(self, transcript: str):
        if not self.pending:
            return

        words = transcript.lower().split()

        if any(w in INTERRUPT_WORDS for w in words):
            await self.session.interrupt()
            self.pending = False
            return

        if all(w in IGNORE_WORDS for w in words):
            # Backchannel → cancel interruption
            self.pending = False
            return

        # Any real sentence → interrupt
        await self.session.interrupt()
        self.pending = False

    async def on_timeout(self):
        if not self.pending:
            return
        await self.session.interrupt()
        self.pending = False
