import requests

LEETCODE_URL = "https://leetcode.com/graphql/"

PROFILE_QUERY = """
query userProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            realName
            ranking
            countryName
        }
        submitStats {
            acSubmissionNum {
                difficulty
                count
                submissions
            }
        }
    }
    userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        topPercentage
    }
}
"""


def get_leetcode_profile(username: str) -> dict:

    response = requests.post(
        LEETCODE_URL,
        json={
            "query": PROFILE_QUERY,
            "variables": {"username": username}
        },
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/{username}/"
        },
        timeout=20
    )

    response.raise_for_status()
    payload = response.json()

    if payload.get("errors"):
        raise ValueError(str(payload["errors"]))

    data = payload.get("data", {})
    user = data.get("matchedUser")

    if not user:
        raise ValueError(f"LeetCode user '{username}' not found")

    profile = user.get("profile") or {}
    stats = user.get("submitStats") or {}
    contest = data.get("userContestRanking")

    solved = {
        item["difficulty"]: item["count"]
        for item in stats.get("acSubmissionNum", [])
    }

    return {
        "platform": "LeetCode",
        "username": user["username"],
        "real_name": profile.get("realName"),
        "country": profile.get("countryName"),
        "global_ranking": profile.get("ranking"),
        "problems_solved": {
            "easy": solved.get("Easy", 0),
            "medium": solved.get("Medium", 0),
            "hard": solved.get("Hard", 0),
            "total": solved.get("All", 0)
        },
        "contest": {
            "rating": contest.get("rating") if contest else None,
            "global_ranking": contest.get("globalRanking") if contest else None,
            "contests_attended": contest.get("attendedContestsCount") if contest else 0,
            "top_percentage": contest.get("topPercentage") if contest else None
        } if contest else None
    }