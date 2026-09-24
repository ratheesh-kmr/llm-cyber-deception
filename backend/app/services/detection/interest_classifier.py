from typing import List
from app.core.scoring_config import INTEREST_PATTERNS

def classify_interest(endpoints: List[str]) -> str:
    """
    Classifies attacker's target interest based on visited endpoints.
    Categories: database, credentials, api, admin, configuration, reconnaissance
    """
    scores = {category: 0 for category in INTEREST_PATTERNS}

    for endpoint in endpoints:
        ep_lower = endpoint.lower()
        for category, patterns in INTEREST_PATTERNS.items():
            for pattern in patterns:
                if pattern in ep_lower:
                    scores[category] += 1

    # Return interest with highest frequency, fallback to reconnaissance
    sorted_interests = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_interests[0][1] > 0:
        return sorted_interests[0][0]
    return "reconnaissance"
