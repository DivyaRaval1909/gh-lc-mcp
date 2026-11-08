from mcp.server.fastmcp import FastMCP

from services.leetcode import get_leetcode_profile
from services.codeforces import (
    get_codeforces_profile,
    get_codeforces_submissions
)

mcp = FastMCP("CodeProfile")


@mcp.tool()
def leetcode_profile(username: str) -> dict:
    """
    Get a public LeetCode profile.

    Returns global ranking, problems solved by difficulty,
    country, and contest statistics.
    """
    return get_leetcode_profile(username)


@mcp.tool()
def codeforces_profile(handle: str) -> dict:
    """
    Get a public Codeforces profile.

    Returns current rating, maximum rating, rank,
    contribution and contest participation.
    """
    return get_codeforces_profile(handle)


@mcp.tool()
def codeforces_submissions(
    handle: str,
    count: int = 10
) -> list:
    """
    Get recent Codeforces submissions.

    Returns problem names, verdicts, programming languages,
    difficulty ratings and problem tags.
    """
    return get_codeforces_submissions(handle, count)


if __name__ == "__main__":
    import sys

    print("Starting CodeProfile MCP Server...", file=sys.stderr)

    mcp.run(transport="stdio")