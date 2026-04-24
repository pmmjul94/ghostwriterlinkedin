"""
LinkedIn Agent — handles LinkedIn API v2: posting, profile, and analytics.
"""
import requests
from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN

LINKEDIN_API_BASE = "https://api.linkedin.com/v2"


def _headers() -> dict:
    token = LINKEDIN_ACCESS_TOKEN
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202401",
    }


def get_person_urn() -> str:
    """Return person URN from config, or fetch via /userinfo (OpenID Connect)."""
    if LINKEDIN_PERSON_URN:
        return LINKEDIN_PERSON_URN

    # /userinfo works with openid+profile scopes (standard with LinkedIn's token generator)
    resp = requests.get(f"{LINKEDIN_API_BASE}/userinfo", headers=_headers(), timeout=10)
    resp.raise_for_status()
    sub = resp.json().get("sub", "")
    if not sub:
        raise RuntimeError("Could not determine LinkedIn person URN — set LINKEDIN_PERSON_URN secret")
    return f"urn:li:person:{sub}"


def publish_post(content: str) -> dict:
    """Publish a text post to LinkedIn. Returns the created post data."""
    author_urn = get_person_urn()

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    resp = requests.post(
        f"{LINKEDIN_API_BASE}/ugcPosts",
        headers=_headers(),
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()

    post_id = resp.headers.get("X-RestLi-Id", "")
    return {
        "linkedin_post_id": post_id,
        "status": "published",
        "response": resp.json() if resp.content else {},
    }


def get_post_analytics(linkedin_post_id: str) -> dict:
    """Fetch engagement analytics for a specific LinkedIn post."""
    resp = requests.get(
        f"{LINKEDIN_API_BASE}/socialMetadata",
        headers=_headers(),
        params={"ids[0]": linkedin_post_id},
        timeout=10,
    )

    if not resp.ok:
        return {"reactions": 0, "comments": 0, "shares": 0, "impressions": 0, "clicks": 0}

    data = resp.json()
    results = data.get("results", {})
    post_data = results.get(linkedin_post_id, {})

    return {
        "reactions": post_data.get("reactionSummary", {}).get("numLikes", 0),
        "comments": post_data.get("commentCount", 0),
        "shares": post_data.get("shareStatistics", {}).get("shareCount", 0),
        "impressions": post_data.get("shareStatistics", {}).get("impressionCount", 0),
        "clicks": post_data.get("shareStatistics", {}).get("clickCount", 0),
    }


def validate_token() -> bool:
    """Check if token exists and is recognised by LinkedIn (via /userinfo)."""
    if not LINKEDIN_ACCESS_TOKEN:
        return False
    try:
        resp = requests.get(f"{LINKEDIN_API_BASE}/userinfo", headers=_headers(), timeout=5)
        return resp.ok
    except Exception:
        return False
