from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple

# Importing our Core Engineering Modules
from stream_processing.top_k_patterns import top_k_suspicious_patterns
from agent_workflows.dependency_resolver import has_deadlock
from text_sanitization.trie_search import PromptSanitizer
from resource_allocation.cloud_optimizer import optimize_cluster_allocation

# Initialize the API and the Trie Database
app = FastAPI(
    title="Aegis-IR Core",
    description="Automated Incident Response & Observability Gateway"
)

sanitizer = PromptSanitizer()
# Pre-loading the WAF with standard adversarial injection attempts
for word in ["ignore_previous", "system_prompt", "bypass", "drop_table"]:
    sanitizer.insert_banned_word(word)

# --- Request Models (Data Validation) ---
class StreamData(BaseModel):
    stream: List[str]
    k: int

class WorkflowData(BaseModel):
    num_tasks: int
    dependencies: List[Tuple[int, int]]

class PromptData(BaseModel):
    prompt: str

class CloudBudget(BaseModel):
    costs: List[int]
    compute_power: List[int]
    max_budget: int

# --- API Endpoints ---

@app.post("/analyze-traffic")
async def analyze_traffic(data: StreamData):
    """Detects top K suspicious IPs/patterns in a high-velocity stream."""
    anomalies = top_k_suspicious_patterns(data.stream, data.k)
    return {"status": "success", "suspicious_patterns": anomalies}

@app.post("/waf/sanitize")
async def sanitize_input(data: PromptData):
    """O(L) real-time Web Application Firewall for AI prompts."""
    is_safe = sanitizer.is_prompt_safe(data.prompt)
    if not is_safe:
        raise HTTPException(status_code=403, detail="Malicious payload detected and blocked.")
    return {"status": "safe", "message": "Prompt cleared for inference."}

@app.post("/orchestration/detect-deadlock")
async def detect_workflow_deadlock(data: WorkflowData):
    """Prevents AI agents from freezing by detecting cyclical dependencies."""
    is_deadlocked = has_deadlock(data.num_tasks, data.dependencies)
    return {"status": "success", "system_deadlocked": is_deadlocked}

@app.post("/infrastructure/optimize-fallback")
async def optimize_cloud_fallback(data: CloudBudget):
    """Calculates maximum compute recovery within strict financial constraints."""
    max_compute = optimize_cluster_allocation(data.costs, data.compute_power, data.max_budget)
    return {"status": "success", "allocated_compute_power": max_compute}
