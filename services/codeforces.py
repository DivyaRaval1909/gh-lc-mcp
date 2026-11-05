import requests

BASE_URL = "https://codeforces.com/api"


def api_request(endpoint: str, params: dict) -> dict:

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params=params,
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    if data.get("status") != "OK":
        raise ValueError(data.get("comment", "Codeforces API error"))

    return data["result"]


def get_codeforces_profile(handle: str) -> dict:

    users = api_request(
        "user.info",
        {"handles": handle}
    )

    if not users:
        raise ValueError(f"Codeforces user '{handle}' not found")

    user = users[0]

    rating_history = api_request(
        "user.rating",
        {"handle": handle}
    )

    return {
        "platform": "Codeforces",
        "handle": user["handle"],
        "name": " ".join(filter(None, [
            user.get("firstName"),
            user.get("lastName")
        ])),
        "country": user.get("country"),
        "city": user.get("city"),
        "rating": user.get("rating"),
        "max_rating": user.get("maxRating"),
        "rank": user.get("rank"),
        "max_rank": user.get("maxRank"),
        "contribution": user.get("contribution"),
        "friend_of_count": user.get("friendOfCount"),
        "contests_participated": len(rating_history),
        "registration_time": user.get("registrationTimeSeconds")
    }


def get_codeforces_submissions(
    handle: str,
    count: int = 10
) -> list:

    if not 1 <= count <= 1000:
        raise ValueError("Count must be between 1 and 1000")

    submissions = api_request(
        "user.status",
        {
            "handle": handle,
            "from": 1,
            "count": count
        }
    )

    return [
        {
            "problem": submission["problem"]["name"],
            "contest_id": submission["problem"].get("contestId"),
            "verdict": submission.get("verdict"),
            "language": submission.get("programmingLanguage"),
            "rating": submission["problem"].get("rating"),
            "tags": submission["problem"].get("tags", []),
            "timestamp": submission.get("creationTimeSeconds")
        }
        for submission in submissions
    ]