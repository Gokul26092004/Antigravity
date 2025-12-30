from langchain_core.tools import tool

@tool
def query_logs(query: str, timeframe: str = "1h") -> str:
    """Search logs in ELK/Datadog. Returns raw log lines."""
    print(f"  [Tool] querying logs for '{query}' in last {timeframe}...")
    # Mock response grounded in a realistic scenario
    if "ConnectionRefused" in query:
        return "[2023-10-27 10:00:01] DB connection failed: Connection refused on port 5432"
    return "No logs found."

@tool
def retrieve_docs(query: str) -> str:
    """Retrieve runbooks or internal documentation."""
    print(f"  [Tool] searching docs for '{query}'...")
    if "Connection refused" in query or "DB" in query:
        return "Runbook #12: Check if RDS instance is reachable. Check Security Groups."
    return "No relevant docs found."

@tool
def git_grep(pattern: str) -> str:
    """Search codebase for patterns."""
    print(f"  [Tool] git grep '{pattern}'...")
    return "src/db/connection.py:45: db_url = os.getenv('DB_URL')"

@tool
def create_pull_request(diff: str) -> str:
    """Creates a PR with the fix."""
    print(f"  [Tool] Creating PR with diff:\n{diff}")
    return "PR #123 created successfully."

@tool
def run_api_test(endpoint: str, method: str = "GET") -> str:
    """Runs a test request against the API."""
    print(f"  [Tool] Running {method} {endpoint}...")
    # Simulate a successful test after a fix
    return "HTTP 200 OK"

@tool
def revert_commit(commit_hash: str) -> str:
    """Reverts a specific commit."""
    print(f"  [Tool] git revert {commit_hash}...")
    return f"Commit {commit_hash} reverted successfully."
