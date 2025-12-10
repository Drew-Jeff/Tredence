import asyncio
from typing import Dict, Any, Callable, Optional, List
from enum import Enum
import uuid

class NodeType(Enum):
    FUNCTION = "function"
    CONDITION = "condition"

class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: Dict[str, str] = {}  # Simple next step: { "node_a": "node_b" }
        self.conditions: Dict[str, Callable] = {} # For branching: { "node_a": condition_func }
        self.start_node: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.start_node = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_func: Callable, routes: Dict[bool, str]):
        """
        condition_func(state) returns True/False. 
        routes maps result to next node name.
        """
        self.conditions[from_node] = (condition_func, routes)

    async def run(self, initial_state: Dict[str, Any]):
        state = initial_state.copy()
        current_node = self.start_node
        execution_log = []

        # Safety break for infinite loops
        steps = 0
        max_steps = 20 

        while current_node and steps < max_steps:
            steps += 1
            
            # Log execution
            execution_log.append({"step": steps, "node": current_node, "state_snapshot": state.copy()})
            
            # 1. Execute the Node
            if current_node not in self.nodes:
                break
                
            node_func = self.nodes[current_node]
            
            # Support both sync and async nodes
            if asyncio.iscoroutinefunction(node_func):
                state = await node_func(state)
            else:
                state = node_func(state)

            # 2. Determine Next Node
            # Check for conditional routing first
            if current_node in self.conditions:
                condition_func, routes = self.conditions[current_node]
                result = condition_func(state)
                current_node = routes.get(result)
            # Check for standard edge
            elif current_node in self.edges:
                current_node = self.edges[current_node]
            else:
                current_node = None # End of graph

        return state, execution_log