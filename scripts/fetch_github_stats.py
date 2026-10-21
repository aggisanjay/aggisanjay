import urllib.request
import json
import os

LOGIN = "aggisanjay"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# User profile info
user = fetch_json(f"https://api.github.com/users/{LOGIN}")

# Public repos to count stars
repos = fetch_json(f"https://api.github.com/users/{LOGIN}/repos?per_page=100") or []
total_stars = sum(r.get("stargazers_count", 0) for r in repos)

# Search PRs and Issues
prs = fetch_json(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:pr") or {}
issues = fetch_json(f"https://api.github.com/search/issues?q=author:{LOGIN}+type:issue") or {}

# Contributions from site/data/contributions.json
contrib_path = os.path.join("site", "data", "contributions.json")
total_commits = 0
contributed_to = 1
if os.path.exists(contrib_path):
    with open(contrib_path, "r", encoding="utf-8") as f:
        cdata = json.load(f)
        total_commits = cdata.get("total", 0)

data = {
    "login": LOGIN,
    "stars": total_stars,
    "commits": total_commits,
    "prs": prs.get("total_count", 0),
    "issues": issues.get("total_count", 0),
    "contributed_to": len(set(r.get("name") for r in repos if not r.get("fork", False))) or 1,
    "public_repos": user.get("public_repos", len(repos)) if user else len(repos)
}

print(json.dumps(data, indent=2))

out_path = os.path.join("site", "data", "github-glance.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(f"Saved to {out_path}")
