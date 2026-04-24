"""
LinkedIn Bot — one-shot script for GitHub Actions.
Generates a post with Gemini and publishes it to LinkedIn, then exits.

Usage:
    python bot.py              # auto-generate and post
    python bot.py --dry-run    # generate only, don't publish
    python bot.py --topic "AI in healthcare"   # force a specific topic
"""
import logging
import sys
from datetime import datetime, timezone

import config
from agents import content_agent, linkedin_agent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("bot")


def pick_topic_and_pillar(forced_topic: str = "") -> tuple[str, str]:
    """Rotate topic + pillar by day of month to avoid repetition."""
    if forced_topic:
        return forced_topic, config.CONTENT_PILLARS[0]
    day = datetime.now(timezone.utc).day
    topic = config.DEFAULT_TOPICS[day % len(config.DEFAULT_TOPICS)]
    pillar = config.CONTENT_PILLARS[day % len(config.CONTENT_PILLARS)]
    return topic, pillar


def main():
    dry_run = "--dry-run" in sys.argv
    forced_topic = ""
    for i, arg in enumerate(sys.argv):
        if arg == "--topic" and i + 1 < len(sys.argv):
            forced_topic = sys.argv[i + 1]
            break

    logger.info("=== LinkedIn Bot starting%s ===", " (DRY RUN)" if dry_run else "")

    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set")
        sys.exit(1)

    if not dry_run and not linkedin_agent.validate_token():
        logger.error("LinkedIn token is invalid or missing — set LINKEDIN_ACCESS_TOKEN in GitHub secrets")
        sys.exit(1)

    topic, pillar = pick_topic_and_pillar(forced_topic)
    logger.info("Topic: %s | Pillar: %s", topic, pillar)

    try:
        result = content_agent.generate_post(
            topic=topic,
            pillar=pillar,
            tone="Professional",
        )
    except Exception as e:
        logger.error("Content generation failed: %s", e)
        sys.exit(1)

    content = result.get("content", "")
    hashtags = result.get("hashtags", [])
    if hashtags:
        content += "\n\n" + " ".join(f"#{h}" for h in hashtags)

    logger.info("Generated post (%d chars):", len(content))
    logger.info("---\n%s\n---", content)
    logger.info("Hook: %s", result.get("hook", ""))
    logger.info("Why it works: %s", result.get("why_it_works", ""))

    if dry_run:
        logger.info("Dry run — skipping publish")
        return

    try:
        publish_result = linkedin_agent.publish_post(content)
        logger.info("Published! LinkedIn post ID: %s", publish_result.get("linkedin_post_id"))
    except Exception as e:
        logger.error("Publishing failed: %s", e)
        sys.exit(1)

    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
