# agents/pv.py
from google.adk.agents import Agent

pv_agent = Agent(
    name="pv_agent",
    model="gemini-pro-latest",
    description="Pharmacovigilance: AE reporting, clinician workflows, PSUR support.",
    instruction=(
        "Inputs: AE reports, PSURs, clinician feedback.\n"
        "Task: Define AE triage, reporting windows, forms, and clinician brief aligned to NAFDAC PV and MDCN.\n"
        "Output strictly as JSON: { 'workflow': [..], 'forms': [..], 'clinician_brief': '..', 'references': [..] }"
    ),
)
