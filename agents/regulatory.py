# agents/regulatory.py
from google.adk.agents import Agent

reg_agent = Agent(
    name="reg_agent",
    model="gemini-pro-latest",
    description="Regulatory Affairs: NAFDAC/SON/PCN pathways, CTD modules, labeling, PV.",
    instruction=(
        "Inputs: dossier summary, labeling drafts, PV plan.\n"
        "Task: Recommend NAFDAC pathway (new/generic/variation), list CTD modules, estimate timelines, check labeling compliance, outline PV obligations.\n"
        "Output strictly as JSON: { 'pathway': '..', 'modules': [..], 'timelines': '..', 'labeling_checks': [..], 'pv': [..], 'references': [..] }"
    ),
)
