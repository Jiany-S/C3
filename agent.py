"""C3: grounded assistant with routing, native tool calls, and short-term memory.

No agent framework: C4 remains a separate, unauthorised phase.
"""
from __future__ import annotations

import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader
from prompts import ROUTER_INSTRUCTIONS, ROUTE_POLICY, system_prompt

ROOT = Path(__file__).resolve().parent
WRITE_LOCK = threading.Lock()


class ModelError(RuntimeError):
    """Safe-to-display model failure, without request content or credentials."""


def load_business(root=ROOT):
    folder = Path(root) / "me"
    summary = (folder / "business_summary.txt").read_text(encoding="utf-8").strip()
    reader = PdfReader(folder / "about_business.pdf")
    pdf = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    if not summary or not pdf:
        raise ValueError("Business PDF and summary must both contain readable text.")
    return f"[business_summary.txt]\n{summary}\n\n[about_business.pdf]\n{pdf}"


class JsonLog:
    """One local JSON object per line. Single-process thread-safe writes."""
    def __init__(self, folder):
        self.folder = Path(folder)

    def append(self, category, payload):
        record = {"id": str(uuid.uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(), **payload}
        with WRITE_LOCK:
            self.folder.mkdir(parents=True, exist_ok=True)
            with (self.folder / f"{category}.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record["id"]


def schema(name, description, properties):
    return {"type": "function", "function": {"name": name, "description": description,
        "strict": True, "parameters": {"type": "object", "properties": {
            key: {"type": "string", "description": detail} for key, detail in properties.items()},
            "required": list(properties), "additionalProperties": False}}}


TOOL_SCHEMAS = [
    schema("record_customer_interest", "Save a requested follow-up after name, email and notes are supplied.", {
        "email": "Customer-supplied valid email address", "name": "Customer-supplied name",
        "message": "Project/service interest or follow-up notes supplied by the customer"}),
    schema("record_feedback", "Save customer feedback or a business question missing from the sources.", {
        "question": "Customer feedback or unanswered business question"}),
]


class Tools:
    def __init__(self, log):
        self.log = log

    def record_customer_interest(self, email, name, message):
        """Return {ok, record_id, kind}, or {ok:false, error}; save only valid data."""
        values = {"email": email, "name": name, "message": message}
        if any(not isinstance(v, str) or not v.strip() for v in values.values()):
            return {"ok": False, "error": "Name, email, and project notes are required."}
        email, name, message = (v.strip() for v in (email, name, message))
        if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+", email):
            return {"ok": False, "error": "Please provide a valid email address."}
        if len(name) > 120 or len(message) > 3000 or any(c in email + name for c in "\r\n"):
            return {"ok": False, "error": "Name or project notes exceed the allowed format or length."}
        return self._save("leads", {"email": email, "name": name, "message": message})

    def record_feedback(self, question):
        """Persist feedback/unknown question and return a structured observation."""
        if not isinstance(question, str) or not question.strip() or len(question) > 4000:
            return {"ok": False, "error": "A nonempty question of at most 4000 characters is required."}
        return self._save("feedback", {"question": question.strip()})

    def _save(self, category, payload):
        try:
            record_id = self.log.append(category, payload)
            return {"ok": True, "record_id": record_id, "kind": category, "storage": "local JSONL"}
        except OSError:
            return {"ok": False, "error": "Local storage unavailable; nothing confirmed as recorded."}

    def execute(self, name, arguments, allowed, user_text):
        """Validate names, JSON shape and lead provenance before allowing a write."""
        if name not in allowed:
            return {"ok": False, "error": "Tool not available on this route."}
        try:
            args = json.loads(arguments)
        except (ValueError, TypeError):
            return {"ok": False, "error": "Tool arguments must be valid JSON."}
        keys = {"record_customer_interest": {"email", "name", "message"}, "record_feedback": {"question"}}
        if not isinstance(args, dict) or set(args) != keys[name]:
            return {"ok": False, "error": "Tool arguments have missing or unexpected fields."}
        if name == "record_customer_interest":
            # Exact customer-supplied name/email: model cannot silently invent a contact.
            for field in ("email", "name"):
                if not isinstance(args[field], str) or args[field].strip().casefold() not in user_text.casefold():
                    return {"ok": False, "error": f"Ask the customer for their {field}; it was not supplied."}
        return getattr(self, name)(**args)


def record_customer_interest(email, name, message):
    """Required standalone function; same implementation used by model dispatch."""
    return Tools(JsonLog(default_log_dir())).record_customer_interest(email, name, message)


def record_feedback(question):
    """Required standalone function; use temporary Tools instances in tests."""
    return Tools(JsonLog(default_log_dir())).record_feedback(question)


def default_log_dir():
    folder = Path(os.getenv("LOG_DIR", "logs"))
    return folder if folder.is_absolute() else ROOT / folder


class OpenAIModel:
    """The only provider-specific code. No fabricated offline responses."""
    def __init__(self):
        from dotenv import load_dotenv
        from openai import OpenAI
        load_dotenv(ROOT / ".env")
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key or key.startswith("your-"):
            raise ModelError("Set OPENAI_API_KEY in C3/.env to enable real model replies.")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=key, timeout=45.0, max_retries=1)

    def complete(self, messages, *, tools=None, json_mode=False, require_tool=False):
        from openai import OpenAIError
        options = {"model": self.model, "messages": messages, "temperature": 0.2,
                   "max_completion_tokens": 800}
        if tools:
            options.update(tools=tools, tool_choice="required" if require_tool else "auto", parallel_tool_calls=False)
        if json_mode:
            options["response_format"] = {"type": "json_object"}
        try:
            result = self.client.chat.completions.create(**options)
        except OpenAIError as exc:
            status = getattr(exc, "status_code", None)
            detail = {401: "Check your API key.", 429: "Check your quota or retry later.",
                      400: "Check that the configured model supports tools, JSON mode, and these parameters."}.get(status, "Check your connection and retry later.")
            raise ModelError(f"Model request failed. {detail}") from None
        if not result.choices or result.choices[0].finish_reason in {"length", "content_filter"}:
            raise ModelError("The model response was incomplete; please retry with a shorter request.")
        msg = result.choices[0].message
        return {"role": "assistant", "content": msg.content, **({"tool_calls": [
            {"id": c.id, "type": "function", "function": {"name": c.function.name, "arguments": c.function.arguments}}
            for c in msg.tool_calls]} if msg.tool_calls else {})}


def normalize_history(history):
    """Accept current Gradio text blocks and standard OpenAI-style text messages."""
    result = []
    for item in (history or [])[-24:]:
        if not isinstance(item, dict) or item.get("role") not in {"user", "assistant"}:
            continue
        content = item.get("content", "")
        if isinstance(content, list):
            content = "\n".join(block.get("text", "") for block in content
                                if isinstance(block, dict) and block.get("type") == "text")
        if isinstance(content, str) and content.strip():
            result.append({"role": item["role"], "content": content[:6000]})
    return result


class BusinessAgent:
    def __init__(self, model, *, root=ROOT, log_dir=None, reflection=True):
        self.model = model
        self.knowledge = load_business(root)
        self.system_prompt = system_prompt(self.knowledge)
        self.log = JsonLog(log_dir if log_dir is not None else default_log_dir())
        self.tools = Tools(self.log)
        self.reflection = reflection

    def route(self, message, history):
        response = self.model.complete([
            {"role": "system", "content": ROUTER_INSTRUCTIONS + "\nBUSINESS FACTS\n" + self.knowledge},
            *history, {"role": "user", "content": message}], json_mode=True)
        try:
            decision = json.loads(response["content"])
            if set(decision) != {"intent", "reason"} or decision["intent"] not in ROUTE_POLICY or not isinstance(decision["reason"], str):
                raise ValueError
            return decision
        except (KeyError, ValueError, TypeError):
            raise ModelError("The intent classifier returned an invalid result; please retry.") from None

    def respond(self, message, history=None):
        """No shared conversation state: the UI supplies each session's own history."""
        if not isinstance(message, str) or not message.strip():
            return "Please enter a business question or follow-up request."
        if len(message) > 6000:
            return "Please shorten your message to 6000 characters or fewer."
        history = normalize_history(history)
        trace = {"mode": "live" if isinstance(self.model, OpenAIModel) else "mock",
                 "input": message, "tool_events": [], "reflection": {"status": "not_run"}}
        try:
            decision = self.route(message, history)
            trace["route"] = decision
            intent = decision["intent"]
            allowed = {"record_feedback"}
            if intent == "lead":
                allowed.add("record_customer_interest")
            declarations = [s for s in TOOL_SCHEMAS if s["function"]["name"] in allowed]
            messages = [{"role": "system", "content": self.system_prompt + "\n\n" + ROUTE_POLICY[intent]},
                        *history, {"role": "user", "content": message}]
            user_text = "\n".join(m["content"] for m in messages if m["role"] == "user")
            seen = {}
            for step in range(5):
                reply = self.model.complete(messages, tools=declarations,
                                            require_tool=intent == "feedback" and step == 0)
                calls = reply.get("tool_calls") or []
                if not calls:
                    draft = reply.get("content")
                    if not isinstance(draft, str) or not draft.strip():
                        raise ModelError("The model returned an empty answer; please retry.")
                    if intent == "feedback" and not any(e["observation"].get("ok") for e in trace["tool_events"]):
                        raise ModelError("Feedback could not be recorded. Please retry; no save is confirmed.")
                    trace["draft"] = draft
                    final = self.reflect(messages, draft, trace) if self.reflection else draft
                    if not self.reflection:
                        trace["reflection"] = {"status": "disabled"}
                    break
                if len(calls) > 4:
                    raise ModelError("Too many tool requests in one step; please retry.")
                messages.append(reply)
                for call in calls:
                    function = call["function"]
                    signature = (function["name"], function["arguments"])
                    if signature in seen:
                        observation = seen[signature]
                    else:
                        observation = self.tools.execute(*signature, allowed, user_text)
                        seen[signature] = observation
                    trace["tool_events"].append({"call_id": call["id"], "name": function["name"],
                        "arguments": function["arguments"], "observation": observation})
                    messages.append({"role": "tool", "tool_call_id": call["id"], "content": json.dumps(observation)})
            else:
                raise ModelError("The tool step limit was reached. Please retry; recorded actions remain saved.")
            trace["final"] = final
        except ModelError as exc:
            final = str(exc)
            saved = [e["observation"]["record_id"] for e in trace["tool_events"] if e["observation"].get("ok")]
            if saved:
                final += " Local records were saved before this error: " + ", ".join(dict.fromkeys(saved)) + ". No appointment or email is confirmed."
            trace.update(error=final, final=final)
        try:
            self.log.append("traces", trace)
        except OSError:
            final += " Diagnostic logging is unavailable."
        return final

    def reflect(self, messages, draft, trace):
        """One actual review call; records correction or explicit review failure."""
        review_prompt = """Review the draft against the system policy, business sources, conversation and
tool observations. Return JSON with exactly issues (a list of brief policy violations) and
revised_response (the corrected customer reply, or the draft verbatim if no issues).
Check unsupported facts, requests for missing lead fields, tool success versus claims,
and booking/email promises. Brief service/project notes already in history are sufficient;
do not demand that they be repeated. If any tool observation has ok=true, the reply must
explicitly acknowledge the local save, and must not ask whether to save that item again.
Do not invent actions or call tools. If an unknown question
was not logged, acknowledge that logging has not happened; do not claim it has.
Provide policy findings, not private chain-of-thought."""
        try:
            result = self.model.complete([*messages, {"role": "assistant", "content": draft},
                {"role": "system", "content": review_prompt}], json_mode=True)
            trace["reflection_review_raw"] = result.get("content")
            review = json.loads(result["content"])
            if set(review) != {"issues", "revised_response"} or not isinstance(review["issues"], list) or not all(isinstance(i, str) for i in review["issues"]) or not isinstance(review["revised_response"], str) or not review["revised_response"].strip():
                raise ValueError
            changed = review["revised_response"] != draft
            # An issue-free stylistic edit is observable but is not called a policy correction.
            status = ("revised" if review["issues"] else "rephrased") if changed else "unchanged"
            trace["reflection"] = {"status": status, **review}
            return review["revised_response"]
        except (ModelError, ValueError, TypeError, KeyError):
            trace["reflection"] = {"status": "failed", "error": "Review unavailable or malformed; original draft retained."}
            return draft


def create_agent():
    model = OpenAIModel()  # Loads the project .env before reading remaining configuration.
    return BusinessAgent(model, reflection=os.getenv("ENABLE_REFLECTION", "true").lower() == "true")
