import os
import gradio as gr
from google import genai

# ---------------------------------------
# Gemini Client
# ---------------------------------------

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"


# ---------------------------------------
# Blog Generator
# ---------------------------------------

def generate_blog(topic, audience, tone, words, keywords):

    if not topic.strip():
        return "Please enter a blog topic."

    if not audience.strip():
        return "Please enter the target audience."

    prompt = f"""
You are an expert SEO content writer.

Write a blog post with the following requirements.

Topic:
{topic}

Target Audience:
{audience}

Tone:
{tone}

Length:
Approximately {int(words)} words

SEO Keywords:
{keywords}

Instructions:
- Create a catchy SEO-friendly title.
- Write an engaging introduction.
- Use clear headings and subheadings.
- Include practical examples where appropriate.
- Write in simple, readable language.
- Naturally integrate the SEO keywords.
- Bold (**keyword**) each target keyword the first time it appears.
- End with a concise conclusion.
- Format everything neatly using Markdown.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------
# UI
# ---------------------------------------

with gr.Blocks(title="AI Blog Generator") as demo:

    gr.Markdown("# ✍️ AI Blog Generator")
    gr.Markdown(
        "Generate structured, SEO-friendly blog posts using Gemini."
    )

    topic = gr.Textbox(
        label="Blog Topic",
        placeholder="e.g. Remote Work Productivity"
    )

    audience = gr.Textbox(
        label="Target Audience",
        placeholder="e.g. Freelancers and Tech Managers"
    )

    tone = gr.Dropdown(
        choices=[
            "Professional",
            "Casual",
            "Formal",
            "Funny",
            "Inspirational"
        ],
        value="Professional",
        label="Writing Tone"
    )

    words = gr.Slider(
        minimum=200,
        maximum=1000,
        value=500,
        step=100,
        label="Approximate Word Count"
    )

    keywords = gr.Textbox(
        label="SEO Keywords",
        placeholder="time management, remote work, productivity"
    )

    generate_btn = gr.Button("🚀 Generate Blog")

    output = gr.Markdown()

    generate_btn.click(
        fn=generate_blog,
        inputs=[
            topic,
            audience,
            tone,
            words,
            keywords
        ],
        outputs=output
    )

demo.launch()
