from google.adk.agents import Agent

ma_agent = Agent(
    name="ma_agent",
    model="gemini-pro-latest",
    description="Market Access: NHIA reimbursement, formulary, NPHCDA programs, cold chain QA.",
    instruction=(
        "Inputs: cost-effectiveness summary, budget impact model, formulary requirements, cold chain SOPs.\n"
        "Task: Outline reimbursement strategy, formulary steps, budget impact highlights, and cold chain compliance.\n"
        "Output strictly as JSON: { 'strategy': '..', 'formulary_requirements': [..], 'budget_impact': '..', 'cold_chain': [..], 'references': [..] }"
    ),
)