# complianceAssistant

complianceAssistant is an AI-powered compliance assistant for pharmaceutical regulatory workflows. It leverages Google’s Agent Development Kit (ADK) and Gemini models to automate compliance reports, GMP audit checklists, and CAPA (Corrective and Preventive Actions) recommendations. The system orchestrates multiple specialized agents to provide structured compliance assessments across various functional areas.

## Overview

complianceAssistant streamlines regulatory compliance for pharmaceutical organizations by automating the generation of audit checklists, CAPA recommendations, and consolidated compliance reports. It is designed for use in quality assurance, pharmacovigilance, regulatory affairs, and market access functions.

## System Architecture

### Components

- **Agents**
  - QA Agent: Handles Quality Assurance findings.
  - QC Agent: Manages Quality Control data.
  - Regulatory Agent: Aligns with NAFDAC/WHO guidelines.
  - PV Agent: Pharmacovigilance reporting.
  - Market Access Agent: Market entry compliance.
  - Search Agent: External references.
  - Report Agent: Consolidates outputs into structured reports.

- **Runner Manager (`runner.py`)**
  - Initializes agent sessions.
  - Provides helper functions for event creation.

- **Orchestrator (`orchestrator.py`)**
  - Routes queries to appropriate agents.
  - Collects and formats results.

- **Main Application (`main.py`)**
  - CLI interface for user queries.
  - Handles error messages (quota exceeded, service unavailable).
  - Prints compliance reports.

## Installation & Setup

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- Google Cloud project with Gemini API enabled

### Steps

Clone project
git clone https://github.com/your-org/RegPharmaAssist.git
cd RegPharmaAssist

Create virtual environment
python -m venv myenv
source myenv/bin/activate # Linux/Mac
myenv\Scripts\activate # Windows

Install dependencies
pip install -r requirements.txt

text

### Environment Variables

Set up in `.env` or `config.py`:
- `GOOGLE_API_KEY`
- `APP_NAME`
- `USER_ID`
- `SESSION_ID`

## Usage

Run the app:
python main.py

text

You’ll see:
Enter your query (or 'quit'):

text

### Example Queries

**Simple text:**
Generate a GMP compliance audit checklist for XYZ Pharma Ltd.

text

**Structured JSON payload:**
{
"audit_scope": "Recall audit",
"facility": "XYZ Pharma Ltd",
"findings": [
{
"area": "Equipment Calibration",
"issue": "Two balances overdue for calibration",
"severity": "Major"
},
{
"area": "Batch Records",
"issue": "Incomplete entries in batch record for lot 12345",
"severity": "Major"
}
],
"references": [
"WHO GMP Guidelines",
"NAFDAC GMP Inspection Guide"
]
}

text

## Error Handling

### Common Errors

- **429 RESOURCE_EXHAUSTED**
  - Cause: Free tier quota exceeded (2 requests/minute or 50 requests/day).
  - Solution: Wait for quota reset or upgrade billing.
  - Message: `⚠️ Gemini API quota exceeded. Please wait or upgrade your plan.`

- **503 UNAVAILABLE**
  - Cause: Gemini service overloaded.
  - Solution: Retry later.
  - Message: `⚠️ Gemini service is temporarily overloaded. Try again later.`

### Retry Logic

- Automatic retry after delay extracted from error message.
- Retries once before failing gracefully.

## Sample Output

Compliance Assessment Report
Overview
Audit conducted for XYZ Pharma Ltd under NAFDAC GMP guidelines.

Key Findings
Equipment Calibration: Major deviation (two balances overdue).

Batch Records: Major deviation (incomplete entries for lot 12345).

CAPA Recommendations
Immediate calibration of balances; implement automated reminders.

Retrain staff on batch record completion; introduce electronic batch records.

References
WHO GMP Guidelines

NAFDAC GMP Inspection Guide

text

## Future Improvements

- Web dashboard for interactive compliance reports.
- Integration with document repositories (OneDrive, Google Drive).
- Multi-language support for global regulatory contexts.
- Automated CAPA tracking and effectiveness checks.

## Conclusion

complianceAssistant provides a robust, multi-agent framework for pharmaceutical compliance audits. While quota limits may restrict free-tier usage, the architecture is extensible for enterprise deployment[web:6][web:10].

---

You can drop this README.md directly into your repository. Let me know if you want a version tailored for a different agent name or with additional sections.