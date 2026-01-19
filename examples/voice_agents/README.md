# Voice Agents Examples


---

## ⚠️ Assignment Submission (Important)

This repository includes an **assignment-specific implementation of semantic, state-aware
interruption handling** as required by the campus assignment.

👉 **Start here:**  
- **Code:** `examples/voice_agents/realtime_turn_detector.py`  
- **Logic:** `semantic_turn_detector.py`  
- **Explanation:** Scroll to **“Assignment: Intelligent Interruption Handling”** at the end of this README.

This section explains the design, behavior, and how the requirements are satisfied.

---

This directory contains a comprehensive collection of voice-based agent examples demonstrating various capabilities and integrations with the LiveKit Agents framework.

## 📋 Table of Contents

### 🚀 Getting Started

- [`basic_agent.py`](./basic_agent.py) - A fundamental voice agent with metrics collection

### 🛠️ Tool Integration & Function Calling

- [`annotated_tool_args.py`](./annotated_tool_args.py) - Using Python type annotations for tool arguments
- [`dynamic_tool_creation.py`](./dynamic_tool_creation.py) - Creating and registering tools dynamically at runtime
- [`raw_function_description.py`](./raw_function_description.py) - Using raw JSON schema definitions for tool descriptions
- [`silent_function_call.py`](./silent_function_call.py) - Executing function calls without verbal responses to user
- [`long_running_function.py`](./long_running_function.py) - Handling long running function calls with interruption support

### ⚡ Real-time Models

- [`weather_agent.py`](./weather_agent.py) - OpenAI Realtime API with function calls for weather information
- [`realtime_video_agent.py`](./realtime_video_agent.py) - Google Gemini with multimodal video and voice capabilities
- [`realtime_joke_teller.py`](./realtime_joke_teller.py) - Amazon Nova Sonic real-time model with function calls
- [`realtime_load_chat_history.py`](./realtime_load_chat_history.py) - Loading previous chat history into real-time models
- [`realtime_turn_detector.py`](./realtime_turn_detector.py) - Using LiveKit's turn detection with real-time models
- [`realtime_with_tts.py`](./realtime_with_tts.py) - Combining external TTS providers with real-time models

### 🎯 Pipeline Nodes & Hooks

- [`fast-preresponse.py`](./fast-preresponse.py) - Generating quick responses using the `on_user_turn_completed` node
- [`flush_llm_node.py`](./flush_llm_node.py) - Flushing partial LLM output to TTS in `llm_node`
- [`structured_output.py`](./structured_output.py) - Structured data and JSON outputs from agent responses
- [`speedup_output_audio.py`](./speedup_output_audio.py) - Dynamically adjusting agent audio playback speed
- [`timed_agent_transcript.py`](./timed_agent_transcript.py) - Reading timestamped transcripts from `transcription_node`
- [`inactive_user.py`](./inactive_user.py) - Handling inactive users with the `user_state_changed` event hook
- [`resume_interrupted_agent.py`](./resume_interrupted_agent.py) - Resuming agent speech after false interruption detection
- [`toggle_io.py`](./toggle_io.py) - Dynamically toggling audio input/output during conversations

### 🤖 Multi-agent & AgentTask Use Cases

- [`restaurant_agent.py`](./restaurant_agent.py) - Multi-agent system for restaurant ordering and reservation management
- [`multi_agent.py`](./multi_agent.py) - Collaborative storytelling with multiple specialized agents
- [`email_example.py`](./email_example.py) - Using AgentTask to collect and validate email addresses

### 🔗 MCP & External Integrations

- [`web_search.py`](./web_search.py) - Integrating web search capabilities into voice agents
- [`langgraph_agent.py`](./langgraph_agent.py) - LangGraph integration
- [`mcp/`](./mcp/) - Model Context Protocol (MCP) integration examples
  - [`mcp-agent.py`](./mcp/mcp-agent.py) - MCP agent integration
  - [`server.py`](./mcp/server.py) - MCP server example
- [`zapier_mcp_integration.py`](./zapier_mcp_integration.py) - Automating workflows with Zapier through MCP

### 💾 RAG & Knowledge Management

- [`llamaindex-rag/`](./llamaindex-rag/) - Complete RAG implementation with LlamaIndex
  - [`chat_engine.py`](./llamaindex-rag/chat_engine.py) - Chat engine integration
  - [`query_engine.py`](./llamaindex-rag/query_engine.py) - Query engine used in a function tool
  - [`retrieval.py`](./llamaindex-rag/retrieval.py) - Document retrieval

### 🎵 Specialized Use Cases

- [`background_audio.py`](./background_audio.py) - Playing background audio or ambient sounds during conversations
- [`push_to_talk.py`](./push_to_talk.py) - Push-to-talk interaction
- [`tts_text_pacing.py`](./tts_text_pacing.py) - Pacing control for TTS requests
- [`speaker_id_multi_speaker.py`](./speaker_id_multi_speaker.py) - Multi-speaker identification

### 📊 Tracing & Error Handling

- [`langfuse_trace.py`](./langfuse_trace.py) - LangFuse integration for conversation tracing
- [`error_callback.py`](./error_callback.py) - Error handling callback
- [`session_close_callback.py`](./session_close_callback.py) - Session lifecycle management

## 📖 Additional Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [Agents Starter Example](https://github.com/livekit-examples/agent-starter-python)
- [More Agents Examples](https://github.com/livekit-examples/python-agents-examples)

---

## 🧠 Assignment: Intelligent Interruption Handling

### Problem
In voice conversations, users often provide short backchannel utterances such as
“yeah”, “ok”, or “hmm” while an agent is speaking.  
Default VAD-based interruption handling incorrectly treats these as true interruptions,
causing the agent to stop speaking mid-response.

This breaks conversational flow and results in a poor user experience.

---

### Solution
This solution implements a **semantic, state-aware interruption policy** using LiveKit’s
turn detection system.

Key principles:
- Voice Activity Detection (VAD) is left completely unchanged.
- Interruption decisions are made in **text space**, using STT output.
- Backchannel utterances are ignored **only while the agent is speaking**.
- Explicit interruption commands (e.g., “stop”, “wait”, “no”) immediately interrupt the agent.
- No pause/resume or buffering logic is used.

---

### How It Works
A custom `SemanticTurnDetector` extends LiveKit’s `MultilingualModel` and overrides the
turn decision logic.

- While the agent is speaking:
  - Pure backchannel utterances do **not** trigger a turn.
  - Interruption commands immediately trigger a turn.
- When the agent is silent:
  - All user input is handled normally.

Because the logic is implemented inside the turn detection layer, the solution is
deterministic, low-latency, and does not interfere with audio playback.

---

### Why This Meets the Requirements
- No VAD kernel modification
- No pause / resume or stutter
- State-aware handling of short utterances
- Modular, configurable logic
- Fully aligned with LiveKit’s agent architecture

---

### How to Run
```bash
python examples/voice_agents/realtime_turn_detector.py
