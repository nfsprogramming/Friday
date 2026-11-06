# F.R.I.D.A.Y - Vision

## Fully Responsive Intelligent Digital Assistant for You

F.R.I.D.A.Y is a 100% local, hardware-aware AI assistant modeled after Tony Stark's AI, built specifically to run on an Acer Predator PHN16-72 (RTX 4050, i7-14700HX). It is designed to be highly competent, composed, and efficient, avoiding the typical constraints of cloud APIs or heavy abstractions like LangChain.

### Core Philosophy
- **100% Local**: Zero cloud dependencies. No data leaves the machine.
- **Hardware-Bound Design**: Consciously built within a 6GB VRAM budget. Quantized models (Q4/Q5) are a design constraint, not a limitation.
- **Low Latency**: Employs streaming TTS to achieve JARVIS-level perceived latency (<1.5s end-to-end), starting to speak before the LLM finishes generating the response.
- **Safety First**: Implements a strict SAFE/WARNING/DANGEROUS permission model for all tool executions.
- **Terminal First**: The terminal brain and backend must be perfect before any UI is developed. 

### Personality
- **Tone**: Competent, composed, slightly dry wit (like MCU FRIDAY).
- **Style**: Short responses for commands, deeper answers only when asked. Directly states "I don't have that data" rather than hallucinating or apologizing.
- **Context**: Knows the user (Nifras, AI & Data Science student), their machine, games, and projects.

### What F.R.I.D.A.Y is NOT
- Not a generic chatbot.
- Not a wrapper for cloud APIs.
- Not slowed down by LangChain or LlamaIndex abstractions.
- Not a generic roadmap with vague goals.
