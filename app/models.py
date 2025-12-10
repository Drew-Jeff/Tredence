# app/models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from enum import Enum

# --- Enums ---

class WorkflowStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# --- Logging Models ---

class LogEntry(BaseModel):
    step: int
    node: str
    state_snapshot: Dict[str, Any]
    timestamp: Optional[float] = None

# --- API Request/Response Models for Execution ---

class WorkflowStartRequest(BaseModel):
    """Payload to start a specific workflow."""
    initial_state: Dict[str, Any] = Field(default_factory=dict)

class WorkflowRunResponse(BaseModel):
    """Immediate response after triggering a run."""
    run_id: str
    status: WorkflowStatus

class WorkflowStateResponse(BaseModel):
    """Full details of a run (used for polling status)."""
    run_id: str
    status: WorkflowStatus
    current_state: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    logs: List[LogEntry] = []

# --- API Models for Dynamic Graph Creation (Requirement 3) ---

class EdgeDefinition(BaseModel):
    from_node: str
    to_node: Optional[str] = None 
    # If using conditional routing, 'to_node' might be null here 
    # and handled via a condition_map, or strictly defined.
    # For this simple assignment, let's keep it simple:
    
class NodeDefinition(BaseModel):
    name: str
    tool_name: str # The function name registered in tools.py

class GraphCreateRequest(BaseModel):
    """Payload to define a new graph structure via JSON."""
    nodes: List[NodeDefinition]
    edges: List[Dict[str, str]] # Simple adjacency: {"start": "step1", "step1": "step2"}
    start_node: str
    
class GraphCreateResponse(BaseModel):
    graph_id: str
    message: str