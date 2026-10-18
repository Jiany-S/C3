"""Start real Gradio, fetch its HTTP page/config, and exercise a mock callback."""
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import build_demo


def run():
    class Probe:
        def respond(self, message, history):
            return f"MOCK startup probe: {message}; history={len(history)}"
    demo = build_demo(Probe(), show_evidence=False)
    try:
        _, url, _ = demo.launch(server_name="127.0.0.1", server_port=7861,
            share=False, prevent_thread_lock=True, quiet=True)
        with urllib.request.urlopen(url, timeout=20) as response:
            page = response.read().decode()
            assert response.status == 200 and "CedarBridge" in page
        with urllib.request.urlopen(url + "config", timeout=20) as response:
            config = json.load(response)
            assert any(c.get("type") == "chatbot" for c in config["components"])
        from gradio_client import Client
        # Real queue/API path, with intentionally scripted model boundary.
        client = Client(url, verbose=False)
        output = client.predict("startup probe", api_name="/chat")
        assert "MOCK startup probe" in str(output)
        result = {"mode": "real Gradio server / MOCK model callback", "url": url,
                  "http_page": "PASS", "config_chatbot": "PASS", "queued_callback": "PASS",
                  "callback_output": output}
        folder = ROOT / "evidence"
        folder.mkdir(exist_ok=True)
        (folder / "gradio_smoke.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
    finally:
        demo.close()


if __name__ == "__main__":
    run()
