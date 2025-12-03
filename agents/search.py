# agents/search.py
from google.adk.agents import Agent

search_agent = Agent(
    name="search_agent",
    model="gemini-pro-latest",
    description="Handles general queries and produces a summary payload.",
    instruction=(
        "Summarize the user's request context and produce a neutral overview.\n"
        "Output strictly as JSON: { 'summary': '..', 'notes': [..] }"
    ),
)
