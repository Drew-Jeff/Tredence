# Mini Agent Workflow Engine

A lightweight, async-native backend system designed to define, execute, and monitor stateful agent workflows. Built with **FastAPI** and **Python 3.11+**, this engine simulates a simplified version of frameworks like LangGraph, focusing on clean architecture and modularity.

## 🚀 Features

* Graph-Based Execution: Nodes are simple Python functions; edges define control flow.
* State Management: Shared state (dictionary) flows immutably between nodes.
* Conditional Routing: Dynamic branching based on state values (e.g., quality checks).
* Loops: Supports cyclic graphs for iterative improvement (e.g., "Refine until perfect").
* Async Support: Built on `asyncio` for non-blocking execution using FastAPI `BackgroundTasks`.
* Tool Registry: specific tools are decoupled from the core logic.

---

## 📂 Project Structure

```text
/ai-agent-engine
├── app/
│   ├── __init__.py        # Exports Engine & Registry
│   ├── main.py            # FastAPI Entry Point & Endpoints
│   ├── engine.py          # Core Graph Logic (Nodes, Edges, Runner)
│   ├── models.py          # Pydantic Schemas for API & Logging
│   ├── tools.py           # Registry of available functions (Tools)
│   └── workflows.py       # Implementation of specific workflows (Code Review)
├── requirements.txt
└── README.md
