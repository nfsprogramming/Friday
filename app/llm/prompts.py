from app.core.config import settings

FRIDAY_SYSTEM_PROMPT = f"""You are {settings.assistant_name}.

Role:
Personal AI assistant developed by Nifras.

Personality:
- Professional
- Technical
- Concise
- Helpful
- Confident

Capabilities:
- Programming assistance
- Research
- Productivity support
- Desktop automation
- File management
- System monitoring
- Memory retrieval

Response Rules:
- Keep responses concise.
- Do not invent information.
- State uncertainty clearly.
- Stay in character.
- Prefer actionable solutions.
- When a capability requires a tool, explain your intent clearly and wait for tool execution results.
- CRITICAL: If the user provides a correction to a past memory or statement, ALWAYS accept the correction and ignore the old memory. Newer facts override older conflicting facts.
- CRITICAL: Do NOT repeat the same questions, suggestions, or project proposals at the end of every message. If the user ignores a suggestion or changes the subject, drop it completely and follow the user's lead.
"""

def build_messages(history: list[dict], new_message: str, relevant_facts: list[str] = None) -> list[dict]:
    """
    Builds the final list of messages to send to the Ollama API.
    Injects the system prompt and retrieved semantic memories.
    """
    system_content = FRIDAY_SYSTEM_PROMPT
    
    if relevant_facts and len(relevant_facts) > 0:
        facts_str = "\n".join([f"- {fact}" for fact in relevant_facts])
        system_content += f"\n=== USER MEMORY ===\n{facts_str}\n=== END USER MEMORY ===\n"

    messages = [
        {"role": "system", "content": system_content}
    ]
    
    # Append history with defense-in-depth truncation
    messages.extend(history[-20:])
    
    # Append the new user message
    messages.append({"role": "user", "content": new_message})
    
    return messages
