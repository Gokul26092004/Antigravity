from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from state import ErrorContext
from graph import app as agent_app
import uuid
import logging

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class LogRequest(BaseModel):
    log_content: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/analyze")
def analyze_error(request: LogRequest):
    print(f"[Server] Received log: {request.log_content[:50]}...")
    
    initial_state = ErrorContext(
        incident_id=str(uuid.uuid4()),
        status="ANALYZING",
        raw_error_log=request.log_content,
        parsed_stack_trace={},
        related_logs=[],
        metrics_snapshot={},
        root_cause_analysis="",
        confidence_score=0.0,
        proposed_fix_diff="",
        validation_status="",
        history=[]
    )
    
    # Run the agent
    final_state = agent_app.invoke(initial_state)
    
    return final_state

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
