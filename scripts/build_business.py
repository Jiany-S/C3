"""Build the fictional business sources from one consistent fact sheet."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    ("Mission and audience", "CedarBridge Learning Studio is a fictional, independent student project coaching business in Beirut, Lebanon. We help university students learn to plan, build, test, and explain their own software projects. We are not affiliated with AUB or any university and cannot give official academic advice or approve course choices."),
    ("Services and published prices", "Project Clarity: one 30-minute online scoping consultation, USD 15 per student. Prototype Clinic: one 60-minute online debugging and testing coaching session, USD 30 per student. Team Sprint: one 90-minute online project planning workshop for up to four students, USD 60 per team. Prices are fictional teaching data, not real offers. No other prices, discounts, or bundles are published."),
    ("How sessions work", "Sessions take place online in English or Arabic. Service hours are Monday to Friday, 10:00-18:00, Asia/Beirut. Customers can request a consultation by sharing their name, email, and a short description of their project and desired service. Staff aim to respond within two business days. A recorded lead is a request for follow-up, not a confirmed appointment, payment, or sent email. The assistant has no live calendar or payment access."),
    ("Fictional team", "Maya Nassar, co-founder and learning lead, designs project scoping exercises and coaches students to explain their choices. Karim Haddad, co-founder and engineering lead, teaches testing, API integration, and small prototype design. Rania Saleh, client coordinator, reviews consultation requests and routes questions to the appropriate coach. All names and profiles are invented for this assignment."),
    ("What makes us useful", "Students bring their own work. Each session focuses on one concrete blocker and ends with a short next-step checklist. We explain tradeoffs and review tests with the student; we do not ghostwrite graded submissions, guarantee grades, or impersonate university staff. We provide coaching rather than accredited qualifications."),
    ("Known limits and customer feedback", "There is no published refund policy, weekend service, scholarship, internship placement, certification, or guaranteed admission offer. Availability on a specific date is unknown until staff confirm it. The assistant must acknowledge missing information and record the unanswered question using record_feedback. Suggestions and complaints are recorded with the same tool. Contact requests use record_customer_interest only after the customer supplies name, email, and notes and asks for follow-up."),
    ("Data handling in the classroom prototype", "Contact details and notes are saved locally as JSONL lead records. Feedback and execution traces are also stored locally. No email is sent and no external CRM is connected. Use invented names and example.com addresses for demonstrations. Do not provide sensitive information. The prototype has no automatic retention or deletion service; its operator must remove local logs when no longer needed."),
]

def build():
    folder = ROOT / "me"
    folder.mkdir(exist_ok=True)
    styles = getSampleStyleSheet()
    styles["Title"].textColor = colors.HexColor("#134E4A")
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 14
    story = [Paragraph("CedarBridge Learning Studio", styles["Title"]),
             Paragraph("Fictional business profile | EECE 503P/798S | C3", styles["BodyText"]), Spacer(1, 15)]
    for heading, body in SECTIONS:
        story += [Paragraph(heading, styles["Heading2"]), Paragraph(body, styles["BodyText"]), Spacer(1, 5)]
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.drawString(42, 25, "Classroom simulation - all business and staff details are fictional")
        canvas.drawRightString(553, 25, str(doc.page))
    SimpleDocTemplate(str(folder / "about_business.pdf"), rightMargin=42, leftMargin=42,
                      topMargin=38, bottomMargin=40).build(story, onFirstPage=footer, onLaterPages=footer)
    summary = "\n\n".join([SECTIONS[0][1], SECTIONS[1][1], SECTIONS[2][1],
        "Team: Maya Nassar (learning), Karim Haddad (engineering), Rania Saleh (coordination). All are fictional. " + SECTIONS[4][1],
        SECTIONS[5][1], SECTIONS[6][1]]) + "\n"
    (folder / "business_summary.txt").write_text(summary, encoding="utf-8")
    # The PDF's task text says summary.txt; its tree/checklist says business_summary.txt.
    (folder / "summary.txt").write_text(summary, encoding="utf-8")
    print("Built PDF and consistent summaries")

if __name__ == "__main__":
    build()
