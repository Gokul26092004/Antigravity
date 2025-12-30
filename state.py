from typing import List, Optional, TypedDict, Dict, Any, Annotated
import operator

class ErrorContext(TypedDict):
    incident_id: str
    status: str # 'ANALYZING', 'DIAGNOSING', 'GENERATING_FIX', 'VALIDATING', 'COMPLETED', 'FAILED'
    
    # 1. Detection Data
    raw_error_log: str
    parsed_stack_trace: Dict[str, Any]
    
    # 2. Investigation Data
    related_logs: Annotated[List[str], operator.add]
    metrics_snapshot: Dict[str, Any]
    
    # 3. Diagnosis
    root_cause_analysis: str
    confidence_score: float
    
    # 4. Resolution
    proposed_fix_diff: str
    validation_status: str
    history: Annotated[List[str], operator.add] # Audit trail
