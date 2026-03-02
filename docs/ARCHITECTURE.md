# AI Capability Radar - Architecture

The AI Capability Radar tracks the "Expanding AI Bubble" not by running expensive zero-day prompts, but by aggregating, parsing, and evaluating the claims of the broader tech ecosystem. If a new capability emerges (e.g., zero-shot multi-agent system deployment), someone in the open-source community, a leading researcher, or a tech influencer has likely already tested it and documented the failure/success modes.

## System Components

### 1. The Targets (What we are looking for)
Defined in `data/CAPABILITIES.yml`. This is our internal taxonomy of IT and Information Analysis tasks. 
Each capability consists of:
*   **Domain**: (e.g., `Infrastructure`, `Code_Generation`, `Data_Analysis`)
*   **Skill**: (e.g., `Terraform_Scaffolding`, `Complex_SQL_Querying`)
*   **Success Criteria**: What defines this as "Inside the Bubble" vs "On the Frontier".

### 2. The Sensors (Where we listen)
Defined in `data/SOURCES.yml`. The curated list of high-signal nodes on the internet.
*   **YouTube Channels**: (e.g., AI Engineer, sentdex)
*   **Engineering Blogs**: (e.g., OpenAI, Anthropic, Cloudflare, Uber Engineering)
*   **Subreddits/Forums**: (e.g., r/MachineLearning, r/LocalLLaMA)
*   **X (Twitter) Lists**: Curated lists of AI researchers and builders.

### 3. The Ingestion Pipeline (The Scrapers)
A set of Python scripts in `src/ingestion/` that run periodically (e.g., daily/weekly) to pull new content from the Sensors.
*   Downloads YouTube transcripts.
*   Parses RSS feeds.
*   Scrapes URLs for main body text.

### 4. The Extraction Engine (LLM-as-a-Reader)
A local or API-based LLM (e.g., Claude 3 Haiku or GPT-4o-mini) tailored for fast, structured data extraction.
*   **Input**: Raw transcript/article + `CAPABILITIES.yml`.
*   **Prompt Instruction**: "Read this text. Does the author make a claim about an AI model successfully or unsuccessfully performing any of the skills listed in our capability taxonomy? If yes, extract the model name, the capability, the success level, and a quote."
*   **Output**: Structured JSON logs appended to `data/extracted_claims.json`.

### 5. Aggregate & Dashboard (The Output)
A web interface or synthesized Markdown report that answers:
*   "What tasks moved from *Frontier* to *Inside the Bubble* this month?"
*   "What are the known Failure Models for Claude 3.5 Sonnet when writing React hooks, according to the community?"
