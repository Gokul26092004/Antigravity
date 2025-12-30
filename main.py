from state import ErrorContext
from graph import app
import uuid

def main():
    print("==================================================")
    print("Agentic API Error Diagnosis System (MVP)")
    print("==================================================")
    
    # Simulate an input error
    simulated_error_log = """
    ERROR 2023-10-27 10:00:01 com.example.db.ConnectionManager - 
    Failed to connect to jdbc:postgresql://db-prod:5432/users
    org.postgresql.util.PSQLException: Connection to localhost:5432 refused.
    """
    
    print(f"\n[Input] Received Error Log:\n{simulated_error_log.strip()}\n")
    
    initial_state = ErrorContext(
        incident_id=str(uuid.uuid4()),
        status="ANALYZING",
        raw_error_log=simulated_error_log,
        parsed_stack_trace={},
        related_logs=[],
        metrics_snapshot={},
        root_cause_analysis="",
        confidence_score=0.0,
        proposed_fix_diff="",
        validation_status="",
        history=[]
    )
    
    print("[System] Starting Diagnosis Workflow...\n")
    
    # Run the graph
    result = app.invoke(initial_state)
    
    print("\n==================================================")
    print("FINAL DIAGNOSIS REPORT")
    print("==================================================")
    print(f"Incident ID: {result['incident_id']}")
    print(f"Root Cause:  {result['root_cause_analysis']}")
    print(f"Confidence:  {result['confidence_score'] * 100}%")
    print(f"History:     {result['history']}")
    print("==================================================")

if __name__ == "__main__":
    main()
