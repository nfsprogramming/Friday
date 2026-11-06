import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional

from app.llm.client import ollama_client
from app.llm.session import session_manager
from app.llm.prompts import build_messages
from app.llm.rag import store_memory, retrieve_memories
from app.llm.extractor import should_store_memory
from app.core.logger import logger

# Tool Integrations
from app.tools.registry import registry
from app.tools.executor import ToolExecutor
import app.tools.applications.open_app
import app.tools.system.system_info
import app.tools.files.search_file
import app.tools.files.advanced_search
import app.tools.files.open_file
import app.tools.browser.open_url
import app.tools.browser.search_google
import app.tools.browser.search_youtube
import app.tools.browser.extract_content
import app.tools.browser.website_actions
import app.tools.desktop.mouse_tools
import app.tools.desktop.keyboard_tools
import app.tools.desktop.window_tools
import app.tools.desktop.screenshot_tools
import app.tools.desktop.application_tools
import app.tools.desktop.vision_tools
import app.tools.desktop.composite_tools

router = APIRouter()
executor = ToolExecutor(speech_q=None)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    stream: bool = False

async def extract_intents(user_text: str) -> list:
    schemas = registry.get_all_tool_schemas()
    # Simplify the schemas to just name and description to help the small LLM
    simplified_tools = [{"name": s["name"], "description": s["description"]} for s in schemas]
    
    prompt = f"""You are a Multi-Intent Extractor for a Desktop Agent.
User Request: "{user_text}"
Available Tools: {json.dumps(simplified_tools)}

Does the user request match one or more available tools?
If YES, output ONLY a JSON array of objects representing the sequence of actions: [{{"intent": "tool_name", "parameters": {{"param_name": "value"}}}}, ...]
If NO, output ONLY: [{{"intent": "chat", "parameters": {{}}}}]

EXAMPLES:
User: "Open notepad and type hello" -> [{{"intent": "open_and_type", "parameters": {{"app_name": "notepad", "text": "hello"}}}}]
User: "Search youtube for cats" -> [{{"intent": "search_youtube", "parameters": {{"query": "cats"}}}}]
User: "What is my cpu usage?" -> [{{"intent": "system_info", "parameters": {{}}}}]
User: "Find my internship dataset" -> [{{"intent": "semantic_file_search", "parameters": {{"query": "internship dataset"}}}}]
User: "Open the internship dataset file" -> [{{"intent": "open_file", "parameters": {{"filepath": "internship_dataset_2025.csv"}}}}]
User: "Open it" -> [{{"intent": "open_file", "parameters": {{"filepath": "internship_dataset_2025.csv"}}}}]
"""
    messages = [{"role": "system", "content": prompt}]
    result = await ollama_client.chat_json(messages)
    
    if isinstance(result, dict):
        if "intent" in result:
            intents = [result]
        else:
            intents = [{"intent": "chat", "parameters": {}}]
    elif isinstance(result, list):
        intents = result
    else:
        intents = [{"intent": "chat", "parameters": {}}]
        
    # Hardcoded overrides for stubborn LLM
    text_lower = user_text.lower()
    
    # Handle "open all"
    if "open" in text_lower and "all" in text_lower:
        return [{"intent": "open_file", "parameters": {"filepath": "all"}}]
        
    # Handle internship dataset specifically
    if "open" in text_lower and "internship dataset" in text_lower:
        return [{"intent": "open_file", "parameters": {"filepath": "internship_dataset_2025.csv"}}]
                
    return intents

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    logger.info(f"[Session: {request.session_id}] User: {request.message}")
    
    # 1. Intent Extraction & Tool Execution
    intent_results = await extract_intents(request.message)
    logger.info(f"[Intent Extractor] Parsed Intents: {intent_results}")
    
    tool_result_str = ""
    for intent_obj in intent_results:
        intent = intent_obj.get("intent", "chat")
        if intent != "chat" and intent != "none":
            parameters = intent_obj.get("parameters", {})
            res = await executor.execute(intent, parameters)
            tool_result_str += f"{res}\n"
    
    # 2. Retrieve Memory
    memory = session_manager.get_session(request.session_id)
    history = memory.get_history()
    relevant_facts = retrieve_memories(request.session_id, request.message)
    
    # 3. Build context
    messages = build_messages(history, request.message, relevant_facts)
    
    # Inject tool result into context if a tool was executed
    if tool_result_str:
        messages.insert(1, {
            "role": "system", 
            "content": f"SYSTEM: You just executed a tool. Here is the result:\n{tool_result_str}\nInform the user of this outcome concisely."
        })
    
    # 4. Handle Streaming Response
    logger.info(f"[Context Debug] Sending messages to LLM: {messages}")
    if request.stream:
        async def stream_generator():
            full_response = ""
            async for token in ollama_client.chat_stream(messages):
                full_response += token
                yield token
            
            memory.add_message("user", request.message)
            memory.add_message("assistant", full_response)
            
            if should_store_memory(request.message):
                store_memory(request.session_id, request.message)
                
            logger.info(f"[Session: {request.session_id}] FRIDAY: {full_response}")
            
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    
    # 5. Handle Sync Response
    else:
        response_text = await ollama_client.chat_sync(messages)
        memory.add_message("user", request.message)
        memory.add_message("assistant", response_text)
        
        if should_store_memory(request.message):
            store_memory(request.session_id, request.message)
            
        logger.info(f"[Session: {request.session_id}] FRIDAY: {response_text}")
        return {"response": response_text}
