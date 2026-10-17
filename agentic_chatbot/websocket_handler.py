import uuid
import logging

from fastapi import WebSocket, WebSocketDisconnect
from langchain_core.messages import HumanMessage
from audio_services import groq_asr_bytes, murf_tts
from llm_service import create_graph, create_basic_graph

logger = logging.getLogger("voicebot")


async def handle_websocket_connection(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected.")

    try:
        initial_data = await websocket.receive_json()
        if 'user_id' in initial_data:
            thread_id = initial_data.get('user_id')
            graph = create_graph()
            logger.info(f"Authenticated session started for user: {thread_id[:8]}...")
        else:
            graph = create_basic_graph()
            thread_id = str(uuid.uuid4())
            logger.info(f"Anonymous session started: {thread_id[:8]}...")
    except Exception:
        graph = create_basic_graph()
        thread_id = str(uuid.uuid4())
        logger.warning(f"No initial handshake data received, falling back to anonymous session.")

    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            data = await websocket.receive_json()
            if data.get("type") == "end_call":
                logger.info("Call ended by client")
                await websocket.close()
                break

            lang = data.get("lang", "english").lower()
            audio_bytes = await websocket.receive_bytes()

            # --- ASR ---
            transcription = await groq_asr_bytes(audio_bytes)
            logger.debug(f"ASR transcription ({lang}): {transcription[:80]}...")
            await websocket.send_json({"type": "transcription", "text": transcription})
            
            # --- LangGraph LLM ---
            result = await graph.ainvoke(
                    {"messages": [HumanMessage(content=transcription)]},
                    config=config
                )
            llm_response = result["messages"][-1].content
            await websocket.send_json({"type": "llm_response", "text": llm_response})

            # --- TTS ---
            audio_stream = await murf_tts(llm_response)
            await websocket.send_json({"type": "tts_start"})
            await websocket.send_bytes(audio_stream)
            await websocket.send_json({"type": "tts_end"})

        except WebSocketDisconnect:
            logger.info("WebSocket disconnected.")
            break
        except Exception as e:
            logger.exception(f"Error during voice pipeline: {e}")
            await websocket.send_json({"error": str(e)})
            break
