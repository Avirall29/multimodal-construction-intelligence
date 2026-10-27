"""
Gemini Client Wrapper for Multimodal Construction Intelligence Platform
Supports Google GenAI SDK (gemini-2.5-flash / gemini-1.5-flash) with seamless
fallback to structured Demonstration Mode when no API key is supplied.
"""
import os
import json
import re
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image
import io

try:
    from google import genai
    from google.genai import types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

class GeminiClientWrapper:
    """Manages Gemini API requests with automatic fallback to high-fidelity demo mode."""

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
        self.model_name = model_name
        self.client = None
        self.is_live = False
        self.last_error: Optional[str] = None

        if self.api_key and HAS_GOOGLE_GENAI:
            try:
                self.client = genai.Client(api_key=self.api_key)
                self.is_live = True
            except Exception as e:
                self.last_error = f"Client initialization error: {str(e)}"
                self.is_live = False
        else:
            self.is_live = False

    def generate_multimodal(
        self,
        prompt: str,
        image_bytes: bytes,
        mime_type: str = "image/png",
        fallback_json: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], bool, Optional[str]]:
        """
        Sends an image + prompt to Gemini.
        Returns: (parsed_json_dict, is_live_call, error_or_status_message)
        """
        if not self.is_live or not self.client:
            return fallback_json or {}, False, "Demonstration Mode active (No API key or offline)"

        try:
            image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[image_part, prompt],
            )
            raw_text = response.text or ""
            parsed = self.extract_json(raw_text)
            if parsed:
                return parsed, True, None
            else:
                # If LLM didn't return pure JSON, try fallback
                if fallback_json:
                    fallback_json["raw_llm_response"] = raw_text
                    return fallback_json, True, "Warning: LLM returned non-JSON format; using structured schema."
                return {"raw_text": raw_text}, True, None

        except Exception as e:
            err_msg = str(e)
            self.last_error = err_msg
            # Graceful fallback to demonstration data
            if fallback_json:
                return fallback_json, False, f"API Error: {err_msg}. Switched to Demonstration Mode."
            return {"error": err_msg}, False, err_msg

    def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_instruction: str,
        fallback_reply: str
    ) -> Tuple[str, bool]:
        """
        Generates chat text response.
        Returns: (reply_text, is_live_call)
        """
        if not self.is_live or not self.client:
            return fallback_reply, False

        try:
            full_prompt = f"System Instruction:\n{system_instruction}\n\nConversation History:\n"
            for msg in messages:
                role = "User" if msg.get("role") == "user" else "Assistant"
                full_prompt += f"{role}: {msg.get('content', '')}\n"
            full_prompt += "\nAssistant:"

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
            )
            if response.text:
                return response.text.strip(), True
            return fallback_reply, False
        except Exception as e:
            self.last_error = str(e)
            return f"{fallback_reply}\n\n*(Note: Live API request encountered an error: {str(e)[:120]}... Used offline engineering knowledge base)*", False

    @staticmethod
    def extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Extracts and parses JSON from markdown or raw text."""
        if not text:
            return None
        # Try finding ```json ... ``` code fence
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        clean_text = json_match.group(1).strip() if json_match else text.strip()

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Try finding outermost { ... }
            curly_match = re.search(r"\{[\s\S]*\}", text)
            if curly_match:
                try:
                    return json.loads(curly_match.group(0))
                except json.JSONDecodeError:
                    pass
        return None
