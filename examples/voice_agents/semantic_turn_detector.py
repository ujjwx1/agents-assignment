from livekit.plugins.turn_detector.multilingual import MultilingualModel
import re

IGNORE_WORDS = {"yeah", "ok", "okay", "hmm", "uh-huh", "right"}
INTERRUPT_WORDS = {"stop", "wait", "no", "cancel", "hold"}


class SemanticTurnDetector(MultilingualModel):
    def should_take_turn(self, transcript: str, agent_is_speaking: bool) -> bool:
        text = re.sub(r"[^\w\s-]", "", transcript.lower()).strip()

        words = text.split()

        # Guard against empty / noise transcripts
        if not words:
            return False if agent_is_speaking else True

        if agent_is_speaking:
            if any(w in words for w in INTERRUPT_WORDS):
                return True   # HARD INTERRUPT

            if all(w in IGNORE_WORDS for w in words):
                return False  # IGNORE BACKCHANNEL

            return True       # real sentence → interrupt

        return True           # agent silent → normal behavior
