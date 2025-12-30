from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from state import ErrorContext
from tools import query_logs, retrieve_docs, git_grep, run_api_test, create_pull_request, revert_commit
import json

# Setup LLM (Assuming OPENAI_API_KEY is in env)
class MockLLM:
    def invoke(self, messages):
        content = messages[-1].content
        # 1. Analyzer
        if "Analyze this error" in content:
            return type('obj', (object,), {'content': json.dumps({
                "cause": "Bad Deployment", 
                "confidence": 0.95, 
                "suggested_action": "Rollback commit a1b2c3d"
            })})
        # 2. Fix Generator
        if "Generate a fix" in content:
            return type('obj', (object,), {'content': "revert_commit('a1b2c3d')"})
        # 3. Risk Assessor
        if "Assess risk" in content:
            # If Content is revert -> Low Risk
            return type('obj', (object,), {'content': json.dumps({"risk_level": "LOW", "reason": "Standard rollback procedure."})})
            
        return type('obj', (object,), {'content': "I am a mock agent."})

try:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
except:
    print("Warning: OpenAI Key not found, using Mock LLM.")
    llm = MockLLM()

def error_analyzer_node(state: ErrorContext):
    """Analyzes the raw log."""
    print("--- [Agent] Error Analyzer Running ---")
    raw_log = state.get('raw_error_log', '')
    parsed = {"type": "DeploymentError", "timestamp": "2023-10-27T12:00:00Z"}
    print(f"    Identified error type: {parsed['type']}")
    return {"parsed_stack_trace": parsed, "history": ["Analyzed raw log."]}

def investigator_node(state: ErrorContext):
    """Investigates logs and docs."""
    print("--- [Agent] Investigator Running ---")
    print("    [Investigator] Found recent deployment 'a1b2c3d' 2 mins ago.")
    return {"related_logs": ["Deployment started 12:00"], "history": ["Investigated deployment."]}

def diagnosis_node(state: ErrorContext):
    """Reason about root cause."""
    print("--- [Agent] Root Cause Reasoner Running ---")
    diagnosis = "Root Cause: High error rate immediately after deployment a1b2c3d."
    confidence = 0.95
    print(f"    Diagnosis: {diagnosis}")
    return {"root_cause_analysis": diagnosis, "confidence_score": confidence, "status": "DIAGNOSING"}

def fix_generator_node(state: ErrorContext):
    """Generates a fix based on diagnosis."""
    print("--- [Agent] Fix Generator Running ---")
    diagnosis = state.get('root_cause_analysis')
    proposed_fix = "revert_commit('a1b2c3d')"
    print(f"    Proposed Fix: {proposed_fix}")
    return {"proposed_fix_diff": proposed_fix, "status": "GENERATING_FIX", "history": ["Generated fix."]}

def risk_assessor_node(state: ErrorContext):
    """Assesses the risk of the proposed fix."""
    print("--- [Agent] Risk Assessor Running ---")
    fix = state.get('proposed_fix_diff')
    
    # Mock Risk Logic
    if "revert" in fix:
        risk_level = "LOW"
        reason = "Rollbacks are standard procedure."
    else:
        risk_level = "HIGH"
        reason = "Complex code change."
        
    print(f"    Risk Level: {risk_level} ({reason})")
    
    if risk_level == "LOW":
        return {"status": "RISK_APPROVED", "history": ["Risk Assessment: LOW"]}
    else:
        return {"status": "RISK_REJECTED", "history": ["Risk Assessment: HIGH (Stopped)"]}

def validator_node(state: ErrorContext):
    """Executes the fix if approved."""
    print("--- [Agent] Executor/Validator Running ---")
    fix = state.get('proposed_fix_diff')
    
    if "revert_commit" in fix:
        result = revert_commit.invoke({"commit_hash": "a1b2c3d"})
        print(f"    Action Result: {result}")
        return {"validation_status": "EXECUTED", "status": "COMPLETED", "history": ["Executed Rollback."]}
        
    return {"status": "FAILED"}

# Build Graph
workflow = StateGraph(ErrorContext)

workflow.add_node("analyzer", error_analyzer_node)
workflow.add_node("investigator", investigator_node)
workflow.add_node("diagnoser", diagnosis_node)
workflow.add_node("fix_generator", fix_generator_node)
workflow.add_node("risk_assessor", risk_assessor_node)
workflow.add_node("validator", validator_node)

workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", "investigator")
workflow.add_edge("investigator", "diagnoser")
workflow.add_edge("diagnoser", "fix_generator")
workflow.add_edge("fix_generator", "risk_assessor")

def check_risk(state):
    if state["status"] == "RISK_APPROVED":
        return "validator"
    return END

workflow.add_conditional_edges("risk_assessor", check_risk)
workflow.add_edge("validator", END)

app = workflow.compile()
