from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = {
    "score3_high": [
        "Let’s just grab a bite and vibe out this weekend?",
        "Quick hang this week? You popped into my head today."
    ]
}

@app.get("/generate-message")
def generate_message(
    relationship_score: int = Query(..., ge=1, le=5),
    energy_level: str = Query(..., regex="^(low|neutral|high)$"),
    relationship_tags: List[str] = Query(...)
):
    key = f"score{relationship_score}_{energy_level}"
    message = random.choice(templates.get(key, ["Hey, wanna catch up this week?"]))
    return {
        "connection_score": relationship_score,
        "energy": energy_level,
        "tags": relationship_tags,
        "suggested_plan": "Based on your vibe and closeness",
        "message": message
    }

@app.get("/ai-plugin.json")
def serve_plugin_manifest():
    return FileResponse("ai-plugin.json", media_type="application/json")

@app.get("/openapi.yaml")
def serve_openapi_spec():
    return FileResponse("openapi.yaml", media_type="text/yaml")
