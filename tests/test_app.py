import pytest
from agent import ModelError
from app import build_demo


def test_real_gradio_interface_builds_and_callback_passes_memory():
    import gradio as gr
    class Agent:
        def respond(self, message, history):
            assert message == "follow-up" and history[0]["content"] == "Earlier"
            return "Connected callback"
    demo = build_demo(Agent())
    assert isinstance(demo, gr.ChatInterface)
    assert demo.fn("follow-up", [{"role": "user", "content": "Earlier"}]) == "Connected callback"
    demo.close()


def test_no_key_ui_message(monkeypatch):
    import app
    def fail():
        raise ModelError("Set OPENAI_API_KEY in C3/.env to enable real model replies.")
    monkeypatch.setattr(app, "create_agent", fail)
    demo = build_demo()
    assert "OPENAI_API_KEY" in demo.fn("hello", [])
    demo.close()
