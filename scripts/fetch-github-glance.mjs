#!/usr/bin/env node
/**
 * scripts/fetch-github-glance.mjs
 * Fetches real-time GitHub telemetry for the user from GitHub API:
 * - Total Stars Earned
 * - Total Commits (last year) from site/data/contributions.json
 * - Total PRs authored
 * - Total Issues
 * - Contributed to (last year)
 * Saves to site/data/github-glance.json
 */

import fs from "node:fs";
import path from "node:path";

const LOGIN = process.env.GH_USERNAME || "aggisanjay";
const TOKEN = process.env.GH_TOKEN || process.env.GITHUB_TOKEN;
const OUTPUT = process.env.GLANCE_OUTPUT || "site/data/github-glance.json";

async function fetchJson(url) {
  const headers = { "User-Agent": "portfolio-glance-telemetry" };
  if (TOKEN) headers["Authorization"] = `bearer ${TOKEN}`;
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error(`HTTP ${res.status} from ${url}`);
  return await res.json();
}

async function main() {
  console.log(`Fetching real-time GitHub telemetry for @${LOGIN}...`);

  let stars = 0;
  let prsCount = 0;
  let issuesCount = 0;
  let reposCount = 0;
  let contributedTo = 0;

  try {
    const repos = await fetchJson(`https://api.github.com/users/${LOGIN}/repos?per_page=100`);
    if (Array.isArray(repos)) {
      reposCount = repos.length;
      stars = repos.reduce((sum, r) => sum + (r.stargazers_count || 0), 0);
      contributedTo = repos.filter((r) => !r.fork).length || 1;
    }
  } catch (err) {
    console.warn(`Could not fetch repos (${err.message}). Using fallback.`);
  }

  try {
    const prs = await fetchJson(`https://api.github.com/search/issues?q=author:${LOGIN}+type:pr`);
    prsCount = prs.total_count ?? 0;
  } catch (err) {
    console.warn(`Could not search PRs (${err.message}).`);
  }

  try {
    const issues = await fetchJson(`https://api.github.com/search/issues?q=author:${LOGIN}+type:issue`);
    issuesCount = issues.total_count ?? 0;
  } catch (err) {
    console.warn(`Could not search Issues (${err.message}).`);
  }

  // Read commits from contributions.json
  let totalCommits = 0;
  const contribPath = path.resolve("site/data/contributions.json");
  if (fs.existsSync(contribPath)) {
    try {
      const cdata = JSON.parse(fs.readFileSync(contribPath, "utf8"));
      totalCommits = cdata.total || 0;
    } catch {}
  }

  const result = {
    login: LOGIN,
    fetchedAt: new Date().toISOString(),
    stars,
    commits: totalCommits,
    prs: prsCount,
    issues: issuesCount,
    contributed_to: contributedTo,
    public_repos: reposCount,
  };

  const outPath = path.resolve(OUTPUT);
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, JSON.stringify(result, null, 2) + "\n", "utf8");
  console.log(`Wrote real-time telemetry to ${OUTPUT}:`, result);
}

main().catch((err) => {
  console.error("Error in fetch-github-glance:", err);
  process.exit(0); // Exit 0 so workflow never breaks
});
