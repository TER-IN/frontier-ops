# Frontier Operations

> *“If your AI agents haven't surprised you recently with their successes or failures, you are likely not operating at the frontier.”*

Implementing the core pillars of the **Frontier Operations** framework (Boundary Sensing, Capability Forecasting, and Failure Model Maintenance) for IT Services and Information Analysis teams.

## How it Works

1. **Sensors (`data/SOURCES.yml`)**: A curated list of high-signal nodes on the internet (YouTube channels like *AI Engineer*, Anthropic's research RSS, subreddits, etc.).
2. **Taxonomy (`data/CAPABILITIES.yml`)**: Your internal list of specific IT/Engineering skills you want to track (e.g., *Complex React Hooks*, *Terraform Scaffolding*, *Scanned PDF Parsing*).
3. **Ingestion Engine (`src/ingestion/`)**: Python scrapers that pull transcripts and raw text from the Sensors.
4. **Extraction Engine (`src/evaluation/extractor.py`)**: Uses OpenAI Structured Outputs to read the scraped text and extract concrete claims that map to your Capability Taxonomy.
5. **Reporting (`src/main.py`)**: Generates an aggregated Markdown report (`docs/CAPABILITY_REPORT.md`). *(A Next.js visual dashboard is currently in development in `/dashboard`)*.

## Setup & Installation

### Requirements
- Python 3.10+
- OpenAI API Key (For the Extraction Engine)

### 1. Python Environment Setup

```bash
# Clone the repository
git clone <repo-url>
cd <repo-dir>

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and add your OpenAI API Key. If no key is provided, the Extractor will run in "Mock Mode".
```bash
echo "OPENAI_API_KEY=your_key_here" > .env
```

### 3. Run the Pipeline
To run the full ingestion, extraction, and reporting pipeline:
```bash
PYTHONPATH=. python src/main.py
```
This will generate/update the `docs/CAPABILITY_REPORT.md` file.

## Project Structure

```text
├── data/
│   ├── CAPABILITIES.yml      # The taxonomy of skills we track
│   ├── SOURCES.yml           # The list of sensors we scrape
│   └── extracted_claims.json # The database of aggregated claims
├── docs/
│   ├── ARCHITECTURE.md       # Detailed system design
│   └── CAPABILITY_REPORT.md  # Auto-generated aggregate report
├── src/
│   ├── ingestion/            # Scrapers (YouTube, RSS)
│   ├── evaluation/           # LLM extraction logic
│   ├── models/               # Pydantic data schemas
│   └── main.py              # The pipeline orchestrator
└── dashboard/                # (WIP) Next.js visual interface
```

## The 5 Pillars of Frontier Operations

This project operationalizes the philosophy outlined by Nate B. Jones:
1. **Boundary Sensing**: Continuously defining exactly where the human-AI boundary sits for specific IT domains.
2. **Seam Design**: Structuring handoffs between humans and AI for clean recoverability.
3. **Failure Model Maintenance**: Documenting the specific texture and shape of how current models fail.
4. **Capability Forecasting**: Reading the "swells" of AI development to make 6-to-12-month bets.
5. **Leverage Calibration**: Treating human attention as the scarcest resource in an agent-rich environment.
