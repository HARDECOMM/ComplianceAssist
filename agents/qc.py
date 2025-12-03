# agents/qc.py
from google.adk.agents import Agent

qc_agent = Agent(
    name="qc_agent",
    model="gemini-pro-latest",
    description="Quality Control: analytical validation, specs, OOS/OOT, batch release.",
    instruction=(
        "Inputs: COA, chromatograms, validation reports, stability data.\n"
        "Task: Compare observed vs specifications, flag OOS/OOT, confirm validation suitability, decide batch release.\n"
        "Output strictly as JSON: { 'specs': {..}, 'observed': {..}, 'decision': '..', 'investigation': [..], 'references': [..] }"
    ),
)
