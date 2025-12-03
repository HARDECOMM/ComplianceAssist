# router.py
from typing import Optional, List

ROLE_KEYWORDS = {
    "QA": {"qa", "gmp", "sop", "audit", "capa"},
    "QC": {"qc", "batch", "release", "testing", "oos", "oot", "validation"},
    "Regulatory": {"regulatory", "nafdac", "dossier", "submission", "labeling", "son", "pcn", "ema", "fda"},
    "PV": {"pv", "pharmacovigilance", "adverse event", "psur", "rmp", "clinician", "safety"},
    "MarketAccess": {"market access", "nhia", "reimbursement", "formulary", "nphcda", "immunization", "program"},
}

ROLE_REFERENCES = {
    "QA": ["https://www.nafdac.gov.ng/"],
    "QC": ["https://www.nafdac.gov.ng/"],
    "Regulatory": ["https://www.nafdac.gov.ng/", "https://son.gov.ng/", "https://pcn.gov.ng/"],
    "PV": ["https://www.nafdac.gov.ng/safety-updates/"],
    "MarketAccess": ["https://nhia.gov.ng/", "https://nphcda.gov.ng/"],
}

def detect_role(query: str) -> Optional[str]:
    ql = query.lower()
    for role, keys in ROLE_KEYWORDS.items():
        if any(k in ql for k in keys):
            return role
    return None

def role_references(role: Optional[str]) -> List[str]:
    if role and role in ROLE_REFERENCES:
        return ROLE_REFERENCES[role]
    return []
