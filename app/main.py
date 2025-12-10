# app/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid

# Relative imports to ensure package structure works
from .workflows import code_review_workflow
from .models import (
    WorkflowStartRequest, 
    WorkflowRunResponse, 
    WorkflowStateResponse,
    WorkflowStatus
)

app = FastAPI(title="Mini Agent Engine")

# --- In-Memory Storage ---
runs_db: Dict[str, Dict[str, Any]] = {}

# --- API Endpoints ---

@app.post("/graph/run/code-review", response_model=WorkflowRunResponse)
async def run_code_review(request: WorkflowStartRequest, background_tasks: BackgroundTasks):
    """
    Starts the predefined Code Review workflow asynchronously.
    """
    run_id = str(uuid.uuid4())
    
    # Initialize state in DB
    runs_db[run_id] = {
        "run_id": run_id,
        "status": WorkflowStatus.QUEUED,
        "current_state": request.initial_state,
        "logs": [],
        "error": None
    }
    
    # Run in background
    background_tasks.add_task(execute_workflow, run_id, request.initial_state)
    
    return WorkflowRunResponse(run_id=run_id, status=WorkflowStatus.QUEUED)

@app.get("/graph/state/{run_id}", response_model=WorkflowStateResponse)
async def get_run_state(run_id: str):
    if run_id not in runs_db:
        raise HTTPException(status_code=404, detail="Run ID not found")
    
    # Helper to clean up dict keys if necessary, but Pydantic is smart
    data = runs_db[run_id]
    return WorkflowStateResponse(**data)

async def execute_workflow(run_id: str, initial_state: Dict):
    if run_id in runs_db:
        runs_db[run_id]["status"] = WorkflowStatus.RUNNING

    try:
        final_state, logs = await code_review_workflow.run(initial_state)
        
        if run_id in runs_db:
            runs_db[run_id]["status"] = WorkflowStatus.COMPLETED
            runs_db[run_id]["current_state"] = final_state
            runs_db[run_id]["logs"] = logs
            
    except Exception as e:
        if run_id in runs_db:
            runs_db[run_id]["status"] = WorkflowStatus.FAILED
            runs_db[run_id]["error"] = str(e)

if __name__ == "__main__":
    import uvicorn
    # This allows running directly like: python app/main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)