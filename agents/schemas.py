# agents/schemas.py
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class QAResult(BaseModel):
    gaps: List[str] = Field(default_factory=list)
    capa: List[str] = Field(default_factory=list)
    audit_checklist: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class QCResult(BaseModel):
    specs: Dict[str, Any] = Field(default_factory=dict)
    observed: Dict[str, Any] = Field(default_factory=dict)
    decision: str = ""
    investigation: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class RegulatoryResult(BaseModel):
    pathway: str = ""
    modules: List[str] = Field(default_factory=list)
    timelines: str = ""
    labeling_checks: List[str] = Field(default_factory=list)
    pv: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class PVResult(BaseModel):   # <-- this was missing
    workflow: List[str] = Field(default_factory=list)
    forms: List[str] = Field(default_factory=list)
    clinician_brief: str = ""
    references: List[str] = Field(default_factory=list)

class MarketAccessResult(BaseModel):
    strategy: str = ""
    formulary_requirements: List[str] = Field(default_factory=list)
    budget_impact: str = ""
    cold_chain: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)

class SearchResult(BaseModel):
    summary: str = ""
    notes: List[str] = Field(default_factory=list)

class RootReport(BaseModel):
    title: str = "Compliance Assessment Report"
    overview: str = ""
    key_findings: List[str] = Field(default_factory=list)
    sections: Dict[str, Any] = Field(default_factory=dict)
    references: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
