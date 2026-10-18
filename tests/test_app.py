from agent import ModelError
from app import build_demo, launch_options


def test_real_gradio_interface_builds_and_callback_passes_memory():
    import gradio as gr
    class Agent:
        def respond(self, message, history):
            assert message == "follow-up" and history[0]["content"] == "Earlier"
            return "Connected callback"
    demo = build_demo(Agent(), show_evidence=False)
    assert isinstance(demo.chat_interface, gr.ChatInterface)
    assert demo.chat_interface.fn("follow-up", [{"role": "user", "content": "Earlier"}]) == "Connected callback"
    demo.close()


def test_no_key_ui_message(monkeypatch):
    import app
    def fail():
        raise ModelError("Set OPENAI_API_KEY in C3/.env to enable real model replies.")
    monkeypatch.setattr(app, "create_agent", fail)
    demo = build_demo(show_evidence=False)
    assert "OPENAI_API_KEY" in demo.chat_interface.fn("hello", [])
    demo.close()


def test_local_evidence_is_this_turn_and_hosted_default_hides_it(monkeypatch):
    class Agent:
        def respond(self, message, history, *, return_trace=False):
            assert return_trace
            return "Recorded.", {"input": message, "tool_events": []}
    demo = build_demo(Agent(), show_evidence=True)
    assert demo.chat_interface.fn("my turn", []) == ("Recorded.", {"input": "my turn", "tool_events": []})
    demo.close()
    monkeypatch.setenv("SPACE_ID", "example/cedarbridge")
    monkeypatch.setenv("SPACE_ACCESS_PASSWORD", "test-only-password")
    demo = build_demo()
    assert not demo.chat_interface.additional_outputs
    assert launch_options()["server_name"] == "0.0.0.0"
    demo.close()
