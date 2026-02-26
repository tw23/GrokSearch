from typing import List
from .providers.base import SearchResult


def format_search_results(results: List[SearchResult]) -> str:
    if not results:
        return "No results found."

    formatted = []
    for i, result in enumerate(results, 1):
        parts = [f"## Result {i}: {result.title}"]

        if result.url:
            parts.append(f"**URL:** {result.url}")

        if result.snippet:
            parts.append(f"**Summary:** {result.snippet}")

        if result.source:
            parts.append(f"**Source:** {result.source}")

        if result.published_date:
            parts.append(f"**Published:** {result.published_date}")

        formatted.append("\n".join(parts))

    return "\n\n---\n\n".join(formatted)


fetch_prompt = """
## Webpage Content Extraction

Fetch the given URL and return its full content as structured Markdown. Do not summarize, condense, or omit any text.

### Extraction Rules
1. **Complete content**: Retrieve all visible text — headings, paragraphs, lists, tables, code blocks, images, and links. Do not skip any section.
2. **Preserve structure**: Follow the page's original hierarchy. If a Table of Contents exists, use it as the structural guide.
3. **Markdown conversion**:
   - HTML headings to `#` through `######`
   - `<strong>` to `**bold**`, `<em>` to `*italic*`
   - `<a href="url">text</a>` to `[text](url)`
   - `<img src="url" alt="alt">` to `![alt](url)`
   - Code to fenced code blocks with language identifier
   - Tables to Markdown table syntax (`| col | col |`)
4. **Strip non-content**: Remove scripts, styles, ads, tracking code, and cookie banners.
5. **Metadata header** (at the top of output):
   ---
   source: [original URL]
   title: [page title]
   fetched_at: [ISO timestamp]
   ---
6. Return only the Markdown document — no commentary, no extra explanation.
"""


search_prompt = """The user is requesting web research assistance. Use your web search tools to investigate their query from multiple angles when needed. Prefer authoritative sources and include citations.
"""
