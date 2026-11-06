from enum import Enum

class AssistantState(Enum):
    IDLE = "IDLE"           # Waiting for "Hey Jarvis"
    LISTENING = "LISTENING" # Recording user command
    THINKING = "THINKING"   # Generating LLM response
    SPEAKING = "SPEAKING"   # TTS playing audio out loud
