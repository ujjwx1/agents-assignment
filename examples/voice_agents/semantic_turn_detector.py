from livekit.plugins.turn_detector.multilingual import MultilingualModel

IGNORE_WORDS = {"yeah", "ok", "okay", "hmm", "uh-huh", "right"}
INTERRUPT_WORDS = {"stop", "wait", "no", "cancel", "hold"}


class SemanticTurnDetector(MultilingualModel):
    def should_take_turn(self, transcript: str, agent_is_speaking: bool) -> bool:
        text = transcript.lower().strip()

        words = text.split()

        if agent_is_speaking:
            if any(w in words for w in INTERRUPT_WORDS):
                return True   # HARD INTERRUPT

            if all(w in IGNORE_WORDS for w in words):
                return False  # IGNORE BACKCHANNEL

            return True       # real sentence → interrupt

        return True           # agent silent → normal behavior
