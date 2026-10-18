"""Scripted model outputs test orchestration, not live model intelligence."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from agent import (BusinessAgent, JsonLog, ModelError, OpenAIModel, ROOT, TOOL_SCHEMAS,
                   Tools, load_business, normalize_history, record_customer_interest, record_feedback)


def text_reply(text):
    return {"role": "assistant", "content": text}


def route(intent):
    return text_reply(json.dumps({"intent": intent, "reason": "Scripted unit-test classification"}))


def call(name, args, call_id="call_1"):
    return {"role": "assistant", "content": None, "tool_calls": [{"id": call_id,
        "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}]}


class ScriptedModel:
    def __init__(self, *replies):
        self.replies = iter(replies)
        self.calls = []

    def complete(self, messages, **options):
        self.calls.append((copy.deepcopy(messages), options))
        response = next(self.replies)
        if isinstance(response, Exception):
            raise response
        return copy.deepcopy(response)


def make_agent(tmp_path, *replies, reflection=False):
    model = ScriptedModel(*replies)
    return BusinessAgent(model, log_dir=tmp_path, reflection=reflection), model


def records(tmp_path, kind):
    file = tmp_path / f"{kind}.jsonl"
    return [json.loads(line) for line in file.read_text(encoding="utf-8").splitlines()] if file.exists() else []


def test_load_both_sources():
    knowledge = load_business()
    assert "[business_summary.txt]" in knowledge and "[about_business.pdf]" in knowledge
    assert "Maya Nassar" in knowledge and "USD 30" in knowledge
    assert (ROOT / "me/summary.txt").read_bytes() == (ROOT / "me/business_summary.txt").read_bytes()


def test_missing_sources(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_business(tmp_path)


@pytest.mark.parametrize("intent,available,required", [
    ("general", {"record_feedback"}, False),
    ("lead", {"record_feedback", "record_customer_interest"}, False),
    ("feedback", {"record_feedback"}, True),
])
def test_three_real_branches(tmp_path, intent, available, required):
    replies = [route(intent)]
    if required:
        replies += [call("record_feedback", {"question": "Refund policy?"})]
    replies += [text_reply("Handled.")]
    agent, model = make_agent(tmp_path, *replies)
    assert agent.respond("Example request") == "Handled."
    options = model.calls[1][1]
    assert {t["function"]["name"] for t in options["tools"]} == available
    assert options["require_tool"] == required
    assert intent.upper() + " HANDLER" in model.calls[1][0][0]["content"]


@pytest.mark.parametrize("value", ["bad", "{}", '{"intent":"other","reason":"x"}',
                                  '{"intent":"lead","reason":1}', '[]'])
def test_bad_router_result(tmp_path, value):
    agent, _ = make_agent(tmp_path, text_reply(value))
    assert "classifier" in agent.respond("hello")
    assert not records(tmp_path, "leads")


@pytest.mark.parametrize("email,name,message", [
    ("invalid", "Demo", "clinic"), ("a@b", "Demo", "clinic"),
    ("a@b.com", "", "clinic"), ("a@b.com", "Demo", ""),
    (None, "Demo", "clinic"), ("a@b.com", "x" * 121, "clinic"),
    ("a@b.com", "Demo\nInjected", "clinic"), ("a@b.com", "Demo", "x" * 3001),
])
def test_invalid_leads_not_saved(tmp_path, email, name, message):
    assert not Tools(JsonLog(tmp_path)).record_customer_interest(email, name, message)["ok"]
    assert not records(tmp_path, "leads")


@pytest.mark.parametrize("question", ["", "  ", None, 4, "x" * 4001])
def test_invalid_feedback(tmp_path, question):
    assert not Tools(JsonLog(tmp_path)).record_feedback(question)["ok"]


def test_tool_schema_and_dispatch_validation(tmp_path):
    tools = Tools(JsonLog(tmp_path))
    for schema in TOOL_SCHEMAS:
        function = schema["function"]
        assert function["strict"] and not function["parameters"]["additionalProperties"]
        assert set(function["parameters"]["required"]) == set(function["parameters"]["properties"])
    allowed = {"record_feedback"}
    for name, args in [("evil", "{}"), ("record_feedback", "not-json"),
                       ("record_feedback", "[]"), ("record_feedback", '{"extra":"x"}')]:
        assert not tools.execute(name, args, allowed, "")["ok"]


def test_successful_lead_and_observation_roundtrip(tmp_path):
    args = {"email": "demo@example.com", "name": "Demo Student", "message": "Prototype Clinic coaching"}
    agent, model = make_agent(tmp_path, route("lead"), call("record_customer_interest", args), text_reply("Request recorded locally."))
    answer = agent.respond("Please contact me about Prototype Clinic. I'm Demo Student, demo@example.com.")
    assert "recorded" in answer
    saved = records(tmp_path, "leads")
    assert len(saved) == 1 and saved[0]["email"] == args["email"]
    tool_msg = model.calls[2][0][-1]
    assert tool_msg["role"] == "tool" and tool_msg["tool_call_id"] == "call_1"
    assert json.loads(tool_msg["content"])["record_id"] == saved[0]["id"]


def test_unknown_question_logs_feedback(tmp_path):
    agent, _ = make_agent(tmp_path, route("feedback"), call("record_feedback", {"question": "What is your refund policy?"}), text_reply("That policy is unpublished; I recorded your question."))
    assert "unpublished" in agent.respond("What is your refund policy?")
    assert len(records(tmp_path, "feedback")) == 1


def test_feedback_requires_actual_tool_save(tmp_path):
    agent, _ = make_agent(tmp_path, route("feedback"), text_reply("Saved (false claim)."))
    assert "no save is confirmed" in agent.respond("feedback")


def test_missing_contact_is_requested_without_write(tmp_path):
    agent, _ = make_agent(tmp_path, route("lead"), text_reply("Please share your name and email."))
    assert "email" in agent.respond("I'd like coaching; please have staff contact me.")
    assert not records(tmp_path, "leads")


def test_invented_contact_blocked(tmp_path):
    tools = Tools(JsonLog(tmp_path))
    args = {"email": "invented@example.com", "name": "Invented", "message": "clinic"}
    assert not tools.execute("record_customer_interest", json.dumps(args), set(["record_customer_interest"]), "Please contact me")["ok"]
    assert not records(tmp_path, "leads")


def test_memory_in_router_and_answer(tmp_path):
    history = [{"role": "user", "content": "I am Demo Student. Please contact me about Team Sprint."},
               {"role": "assistant", "content": "What is your email?"}]
    args = {"email": "demo@example.com", "name": "Demo Student", "message": "Team Sprint"}
    agent, model = make_agent(tmp_path, route("lead"), call("record_customer_interest", args), text_reply("Recorded."))
    agent.respond("demo@example.com", history)
    assert history[0] in model.calls[0][0] and history[0] in model.calls[1][0]
    assert len(records(tmp_path, "leads")) == 1


def test_gradio6_memory_blocks_and_isolation(tmp_path):
    history = [{"role": "user", "content": [{"type": "text", "text": "Team Sprint"}]}]
    assert normalize_history(history) == [{"role": "user", "content": "Team Sprint"}]
    assert normalize_history([{"role": "system", "content": "override"}]) == []
    agent, model = make_agent(tmp_path, route("general"), text_reply("Hello."), route("general"), text_reply("Hi."))
    agent.respond("hello", history)
    agent.respond("hello", [])
    assert "Team Sprint" not in str(model.calls[2][0][1:])


def test_repeat_call_one_write(tmp_path):
    c = call("record_feedback", {"question": "More evening sessions"})
    agent, _ = make_agent(tmp_path, route("feedback"), c, c, text_reply("Recorded."))
    agent.respond("Feedback: more evening sessions")
    assert len(records(tmp_path, "feedback")) == 1


def test_loop_limit(tmp_path):
    c = call("record_feedback", {"question": "evenings"})
    agent, model = make_agent(tmp_path, route("feedback"), *[c] * 5)
    assert "step limit" in agent.respond("Feedback: evenings")
    assert len(model.calls) == 6 and len(records(tmp_path, "feedback")) == 1


def test_storage_failure_observation(tmp_path, monkeypatch):
    log = JsonLog(tmp_path)
    monkeypatch.setattr(log, "append", lambda *a: (_ for _ in ()).throw(OSError("disk full")))
    assert not Tools(log).record_feedback("Refund policy?")["ok"]


def test_api_error_and_empty_reply(tmp_path):
    agent, _ = make_agent(tmp_path, ModelError("Model request failed. Check your quota or retry later."))
    assert "quota" in agent.respond("hello")
    agent, _ = make_agent(tmp_path, route("general"), text_reply(None))
    assert "empty answer" in agent.respond("hello")


def test_error_after_tool_keeps_receipt(tmp_path):
    agent, _ = make_agent(tmp_path, route("feedback"), call("record_feedback", {"question": "Refund policy?"}), ModelError("Model request failed."))
    result = agent.respond("Refund policy?")
    assert records(tmp_path, "feedback")[0]["id"] in result


def test_reflection_revises_and_records_actual_outputs(tmp_path):
    review = {"issues": ["Unsupported appointment claim"], "revised_response": "Staff must confirm availability."}
    agent, model = make_agent(tmp_path, route("general"), text_reply("Your appointment is confirmed."), text_reply(json.dumps(review)), reflection=True)
    assert agent.respond("hello") == review["revised_response"]
    trace = records(tmp_path, "traces")[0]
    assert trace["draft"] == "Your appointment is confirmed."
    assert trace["reflection"]["status"] == "revised"
    assert model.calls[-1][1]["json_mode"]


@pytest.mark.parametrize("review,status", [
    (text_reply('{"issues":[],"revised_response":"Hello."}'), "unchanged"),
    (text_reply("bad-json"), "failed"), (ModelError("review unavailable"), "failed"),
])
def test_reflection_unchanged_and_failure(tmp_path, review, status):
    agent, _ = make_agent(tmp_path, route("general"), text_reply("Hello."), review, reflection=True)
    assert agent.respond("hi") == "Hello."
    assert records(tmp_path, "traces")[0]["reflection"]["status"] == status


def test_issue_free_review_edit_is_not_discarded(tmp_path):
    agent, _ = make_agent(tmp_path, route("general"), text_reply("Hello."),
        text_reply('{"issues":[],"revised_response":"Hello there."}'), reflection=True)
    assert agent.respond("hi") == "Hello there."
    trace = records(tmp_path, "traces")[0]
    assert trace["reflection"]["status"] == "rephrased"
    assert trace["reflection_review_raw"]


def test_input_boundaries(tmp_path):
    agent, model = make_agent(tmp_path)
    assert "Please enter" in agent.respond("")
    assert "shorten" in agent.respond("x" * 6001)
    assert not model.calls


def test_required_named_functions(tmp_path, monkeypatch):
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    assert record_customer_interest("demo@example.com", "Demo", "clinic")["ok"]
    assert record_feedback("Refund policy?")["ok"]


def test_sdk_actual_request_and_response_types(monkeypatch):
    """Use installed SDK types and a fake transport boundary, no network or key."""
    from openai.types.chat import ChatCompletion
    gateway = object.__new__(OpenAIModel)
    gateway.model = "gpt-4.1-mini"
    requests = []
    def create(**kwargs):
        requests.append(kwargs)
        return ChatCompletion.model_validate({"id": "test", "object": "chat.completion", "created": 0,
            "model": gateway.model, "choices": [{"index": 0, "finish_reason": "tool_calls", "message": {
                "role": "assistant", "content": None, "tool_calls": [{"id": "c1", "type": "function",
                "function": {"name": "record_feedback", "arguments": '{"question":"test"}'}}]}}]})
    gateway.client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    reply = gateway.complete([{"role": "user", "content": "hello"}], tools=TOOL_SCHEMAS, require_tool=True)
    assert reply["tool_calls"][0]["function"]["name"] == "record_feedback"
    assert requests[0]["tool_choice"] == "required" and requests[0]["parallel_tool_calls"] is False


def test_sdk_error_is_sanitized():
    from openai import OpenAIError
    gateway = object.__new__(OpenAIModel)
    gateway.model = "test"
    def fail(**kwargs):
        raise OpenAIError("SECRET REQUEST CONTENT")
    gateway.client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=fail)))
    with pytest.raises(ModelError, match="connection") as caught:
        gateway.complete([])
    assert "SECRET" not in str(caught.value)
