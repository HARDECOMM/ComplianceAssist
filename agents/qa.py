# agents/qa.py
from google.adk.agents import Agent

qa_agent = Agent(
    name="qa_agent",
    model="gemini-pro-latest",
    description="Quality Assurance: GMP/SOP compliance, audits, CAPA.",
    instruction=(
        "Inputs: SOPs, training logs, audit checklists, deviation/CAPA records.\n"
        "Task: Identify GMP gaps, propose CAPA, produce audit-readiness checklist aligned to NAFDAC, SON, PCN, WHO GMP.\n"
        "Output strictly as JSON: { 'gaps': [..], 'capa': [..], 'audit_checklist': [..], 'references': [..] }"
    ),
)
