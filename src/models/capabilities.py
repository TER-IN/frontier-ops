import yaml
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Capability(BaseModel):
    id: str
    domain: str
    skill: str
    description: str
    success_criteria: str
    current_status: str

def load_capabilities(file_path: str = "data/CAPABILITIES.yml") -> List[Capability]:
    """Loads the taxonomy of capabilities we are tracking from YAML."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Capabilities file not found at {file_path}")
        
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    capabilities = []
    for cap_data in data.get("caps", []):
        capabilities.append(Capability(**cap_data))
        
    return capabilities

if __name__ == "__main__":
    # Test loading
    caps = load_capabilities()
    print(f"Loaded {len(caps)} capabilities to track:")
    for cap in caps:
        print(f"- {cap.skill} (Status: {cap.current_status})")
