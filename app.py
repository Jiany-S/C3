"""CedarBridge's Gradio interface, with optional local classroom evidence."""
import os

import gradio as gr
from agent import ModelError, ROOT, create_agent

CSS = """
.gradio-container {max-width: 1220px !important; margin: auto;}
#studio-header {padding: 26px 0 18px; border-bottom: 1px solid var(--border-color-primary); margin-bottom: 20px;}
.studio-kicker {font-size: 11px; font-weight: 700; letter-spacing: .18em; color: #58776a;}
#studio-header h1 {font-size: clamp(30px, 4vw, 44px); line-height: 1.12; letter-spacing: -.035em; margin: 10px 0 12px;}
.studio-intro {font-size: 16px; max-width: 650px; opacity: .8; line-height: 1.6;}
.studio-card {border: 1px solid var(--border-color-primary); border-radius: 16px; padding: 20px; margin-bottom: 12px; background: var(--block-background-fill);}
.studio-card h3 {font-size: 17px; margin: 0 0 8px;}
.studio-card p {line-height: 1.6; margin: 0; opacity: .8; font-size: 14px;}
.service-label {font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: #58776a; margin: 17px 0 5px; font-weight: 700;}
.service-title {font-size: 14px; font-weight: 600; margin: 0 0 3px;}
.service-copy {font-size: 13px; line-height: 1.5; opacity: .75;}
.dark .studio-kicker, .dark .service-label {color: #97bfac;}
#studio-chat {border-radius: 18px; border: 1px solid var(--border-color-primary);}
#studio-note {font-size: 12px; line-height: 1.6; opacity: .72; padding: 8px 0;}
#chat-heading h2 {font-size: 21px; margin-bottom: 4px;}
#chat-heading p {opacity: .75; margin-bottom: 12px;}
footer {display:none !important;}
@media (max-width: 760px) {#studio-header {padding-top: 12px;} .studio-card {padding: 16px;}
#studio-sidebar {order: 2;} #studio-conversation {order: 1;}}
"""

THEME = gr.themes.Soft(
    primary_hue="emerald", secondary_hue="teal", neutral_hue="stone",
    font=["Segoe UI", "Arial", "sans-serif"],
).set(button_primary_background_fill="#17634b", button_primary_background_fill_hover="#124c3a")


def build_demo(agent=None, *, show_evidence=None):
    if show_evidence is None:
        show_evidence = not bool(os.getenv("SPACE_ID")) and os.getenv("SHOW_DEMO_EVIDENCE", "true").lower() == "true"

    def chat(message, history):
        try:
            current_agent = agent if agent is not None else create_agent()
            if show_evidence:
                return current_agent.respond(message, history, return_trace=True)
            return current_agent.respond(message, history)
        except ModelError as exc:
            error = str(exc)
        except (OSError, ValueError):
            error = "Business configuration is unavailable. Check the PDF, summary, and local file permissions."
        return (error, {"error": error}) if show_evidence else error

    with gr.Blocks(title="CedarBridge | Learning Studio", analytics_enabled=False) as demo:
        gr.HTML('''<header id="studio-header">
          <div class="studio-kicker">CEDARBRIDGE / LEARNING STUDIO</div>
          <h1>A clearer path for your next project.</h1>
          <p class="studio-intro">Thoughtful coaching for students who want to build, test,
          and understand their own work. Start a conversation with Mira.</p>
        </header>''')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=260, elem_id="studio-sidebar"):
                gr.HTML('''<aside>
                  <section class="studio-card"><h3>Find your next step</h3>
                    <p>Three ways to move your project forward.</p>
                    <div class="service-label">01 / Scope</div><div class="service-title">Project Clarity</div>
                    <div class="service-copy">Turn a broad idea into a focused plan.</div>
                    <div class="service-label">02 / Build</div><div class="service-title">Prototype Clinic</div>
                    <div class="service-copy">Work through debugging and testing blockers.</div>
                    <div class="service-label">03 / Collaborate</div><div class="service-title">Team Sprint</div>
                    <div class="service-copy">Plan the next steps together.</div>
                  </section>
                  <section class="studio-card"><h3>How follow-up works</h3>
                    <p>Tell Mira which service interests you. Share your name and email when
                    you are ready for staff to follow up. A request is not a confirmed booking.</p>
                  </section></aside>''')
                gr.DownloadButton("Read the studio profile", value=str(ROOT / "me/about_business.pdf"), size="sm")
            with gr.Column(scale=3, min_width=320, elem_id="studio-conversation"):
                gr.Markdown("## Meet Mira\nAsk about services, request follow-up, or share feedback.", elem_id="chat-heading")
                chatbot = gr.Chatbot(height=470, elem_id="studio-chat", label="Mira · CedarBridge", show_label=True,
                    placeholder="<strong>What would help your project today?</strong><br>Choose a starter below, or ask your own question.")
                evidence = gr.JSON(label="Execution record", value={"status": "Send a message to see actual evidence."}, open=True, render=False) if show_evidence else None
                interface = gr.ChatInterface(
                    fn=chat, chatbot=chatbot,
                    textbox=gr.Textbox(placeholder="Ask Mira a question…", show_label=False, container=False, max_lines=4, submit_btn=True),
                    examples=["What does Prototype Clinic cost?", "Please have staff contact me about Team Sprint.",
                              "What is your refund policy?", "Feedback: please add evening sessions."],
                    additional_outputs=[evidence] if evidence is not None else None,
                    cache_examples=False, save_history=False, analytics_enabled=False,
                )
                if evidence is not None:
                    with gr.Accordion("Classroom evidence · latest turn", open=False):
                        gr.Markdown("Actual intent, executed tool observations, draft, and reflection for **this chat turn**. No API keys or private reasoning are shown.")
                        evidence.render()
                gr.Markdown("Fictional classroom business · Online coaching in English and Arabic\n\n"
                    "Use invented contact details. Messages are sent to OpenAI; requests and diagnostic logs are saved by the prototype. "
                    "No email is sent. No university affiliation or grade guarantees.", elem_id="studio-note")
        demo.chat_interface = interface
    return demo


def launch_options():
    """Keep local runs on localhost; bind correctly inside a Space."""
    hosted = bool(os.getenv("SPACE_ID"))
    options = {"server_name": "0.0.0.0" if hosted else "127.0.0.1",
               "server_port": int(os.getenv("PORT", "7860")), "share": False,
               "theme": THEME, "css": CSS}
    if hosted:
        password = os.getenv("SPACE_ACCESS_PASSWORD", "")
        if not password:
            raise ValueError("Set the SPACE_ACCESS_PASSWORD secret before starting the hosted classroom demo.")
        options["auth"] = (os.getenv("SPACE_ACCESS_USER", "professor"), password)
        options["auth_message"] = "CedarBridge classroom demo. Enter the demo credentials shared by the project owner."
    return options


if __name__ == "__main__":
    build_demo().launch(**launch_options())
