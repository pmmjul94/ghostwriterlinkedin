"""
Content Agent — uses Google Gemini to generate LinkedIn posts.
"""
import json
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, CONTENT_PILLARS, POST_TONES, DEFAULT_TOPICS, COMPANY_CONTEXT

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = f"""You are an elite LinkedIn ghostwriter writing in the voice of an AI
product builder at a marketing automation company. Every post must feel like it comes
from someone in the trenches building AI — not a commentator watching from the sidelines.

## About the person you're writing for:
{COMPANY_CONTEXT}

## Your job:
Write LinkedIn posts that connect broader AI/tech topics back to the specific work of
building SAM AI (SAM HELP and the SAM AI Writer) and shipping it for SMS/MMS marketing.
Always ground insights in concrete examples from this work. Avoid generic AI commentary.

## LinkedIn post best practices you always follow:
1. Hook in the first line — a bold statement, surprising fact, or specific observation
   from the builder's perspective (not "AI is changing everything")
2. Keep paragraphs to 1-3 lines max
3. Use line breaks liberally — walls of text kill engagement
4. Reference specific parts of SAM AI when relevant (SAM HELP, SAM AI Writer, Claude on
   Bedrock, SLMs for support, LLMs for campaigns, SMS/MMS use cases)
5. End with an engaging question or CTA that invites other builders / marketers to reply
6. No hashtag spam — max 3-5 relevant hashtags at the end
7. Optimal length: 1,300-2,000 characters
8. Write in first person, conversational voice — "we built", "I learned", "our team found"
9. Be specific — concrete numbers, real tradeoffs, actual lessons beat vague claims

Always return valid JSON in the exact format requested. No markdown code blocks."""


def _model(json_mode: bool = True) -> genai.GenerativeModel:
    config = {"response_mime_type": "application/json"} if json_mode else {}
    return genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT,
        generation_config=config,
    )


def _parse(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


def generate_post(topic: str, pillar: str, tone: str, context: str = "", additional_instructions: str = "") -> dict:
    prompt = f"""Generate a LinkedIn post with these specifications:

Topic: {topic}
Content Pillar: {pillar}
Tone: {tone}
{f'Additional context: {context}' if context else ''}
{f'Special instructions: {additional_instructions}' if additional_instructions else ''}

Return a JSON object with this exact structure:
{{
    "hook": "The first 1-2 lines (the hook)",
    "content": "The full post content including the hook, formatted with line breaks",
    "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
    "char_count": <approximate character count as integer>,
    "cta": "The call-to-action question or statement at the end",
    "why_it_works": "Brief explanation of the strategy behind this post"
}}"""

    response = _model().generate_content(prompt)
    return _parse(response.text)


def generate_content_ideas(topics: list = None, num_ideas: int = 14, performance_context: str = "") -> list:
    if not topics:
        topics = DEFAULT_TOPICS

    prompt = f"""Generate {num_ideas} LinkedIn content ideas for these topics: {', '.join(topics)}

{f'Performance context (use to optimize): {performance_context}' if performance_context else ''}

Distribute ideas across content pillars: {', '.join(CONTENT_PILLARS)}

Return a JSON array where each object has:
{{
    "topic": "The specific topic",
    "pillar": "One of the content pillars",
    "tone": "One of: {', '.join(POST_TONES)}",
    "hook": "The opening hook/first line",
    "outline": "2-3 sentence outline",
    "why_now": "Why this topic is relevant/timely",
    "engagement_prediction": "low/medium/high"
}}"""

    response = _model().generate_content(prompt)
    return _parse(response.text)


def analyze_and_improve_post(post_content: str, analytics_data: dict = None) -> dict:
    analytics_str = ""
    if analytics_data:
        analytics_str = f"""
Performance data:
- Reactions: {analytics_data.get('reactions', 'N/A')}
- Comments: {analytics_data.get('comments', 'N/A')}
- Shares: {analytics_data.get('shares', 'N/A')}
- Impressions: {analytics_data.get('impressions', 'N/A')}
"""

    prompt = f"""Analyze this LinkedIn post and suggest improvements:

---
{post_content}
---
{analytics_str}

Return a JSON object with:
{{
    "score": <1-10 overall score as integer>,
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "suggestions": ["improvement 1", "improvement 2", "improvement 3"],
    "improved_version": "The full rewritten post",
    "hook_rating": <1-10 integer>,
    "readability_rating": <1-10 integer>,
    "cta_rating": <1-10 integer>
}}"""

    response = _model().generate_content(prompt)
    return _parse(response.text)
