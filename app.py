"""Local Gradio entry point. No keys or paid requests needed to start the UI."""
import os
import gradio as gr
from agent import ModelError, create_agent


def build_demo(agent=None):
    def chat(message, history):
        try:
            current_agent = agent if agent is not None else create_agent()
            return current_agent.respond(message, history)
        except ModelError as exc:
            return str(exc)
        except (OSError, ValueError):
            return "Business configuration is unavailable. Check the PDF, summary, and local file permissions."

    return gr.ChatInterface(
        fn=chat, title="CedarBridge Learning Studio",
        description="Ask Mira about project coaching or request staff follow-up. Fictional classroom business. "
                    "Use invented contact details: chat is sent to OpenAI and local tool/trace logs are stored on this computer. "
                    "A request does not confirm a booking or send email.",
        examples=["What does Prototype Clinic cost?", "I'd like staff to contact me about Team Sprint.",
                  "What is your refund policy?", "Feedback: please add evening sessions."],
        cache_examples=False, save_history=False, analytics_enabled=False,
    )


if __name__ == "__main__":
    build_demo().launch(server_name="127.0.0.1", server_port=int(os.getenv("PORT", "7860")), share=False)
