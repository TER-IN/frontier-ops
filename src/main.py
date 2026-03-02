import os
import json
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

from src.models.sources import load_sources
from src.models.capabilities import load_capabilities
from src.ingestion.youtube import fetch_transcript, extract_video_id
from src.ingestion.rss import fetch_rss_feed
from src.evaluation.extractor import ClaimExtractor

load_dotenv()

def run_pipeline():
    print("--- Starting AI Capability Radar Pipeline ---")
    sources = load_sources()
    capabilities = load_capabilities()
    extractor = ClaimExtractor()
    
    all_claims = []
    
    for source in sources:
        print(f"\nProcessing Source: {source.id} ({source.type})")
        
        texts_to_process = []
        
        if source.type == "youtube_channel":
            # For this MVP, we will try to fetch if the source URL is actually a video URL.
            # In a full system, we would list all recent videos from the channel.
            vid_id = extract_video_id(source.url)
            if vid_id:
                transcript = fetch_transcript(vid_id)
                if transcript:
                    texts_to_process.append(transcript)
            else:
                print(f"MVP Mode: Assuming {source.id} config URL is not a direct video. Skipping.")
                
        elif source.type == "rss_feed":
            entries = fetch_rss_feed(source.url)
            # Process only the top 3 latest entries to save API costs
            for entry in entries[:3]:
                texts_to_process.append(entry.get('content', ''))
                
        # Extract claims from the fetched texts
        for i, text in enumerate(texts_to_process):
            if not text.strip(): continue
            print(f"  -> Extracting from piece {i+1}/{len(texts_to_process)} ({len(text)} chars)")
            claims = extractor.extract(text, capabilities)
            
            for claim in claims:
                # Augment claim with source info
                claim_dict = claim.dict()
                claim_dict["source_id"] = source.id
                claim_dict["extracted_at"] = datetime.now(timezone.utc).isoformat()
                all_claims.append(claim_dict)
                print(f"     [+] Found Claim: {claim.model_name} -> {claim.capability_id} ({claim.success_level})")
                
    # Save raw claims
    save_claims(all_claims)
    # Generate report
    generate_report(all_claims, capabilities)
    
def save_claims(claims: list, output_file: str = "data/extracted_claims.json"):
    """Appends new claims to the database of claims."""
    path = Path(output_file)
    existing_claims = []
    
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            existing_claims = json.load(f)
            
    existing_claims.extend(claims)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing_claims, f, indent=2, ensure_ascii=False)
        
    print(f"\nSaved {len(claims)} new claims to {output_file}.")

def generate_report(claims: list, capabilities: list, output_file: str = "docs/CAPABILITY_REPORT.md"):
    """Generates a Markdown report summarizing the findings."""
    cap_dict = {cap.id: cap for cap in capabilities}
    
    generator_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    report_lines = [
        "# AI Capability Radar - State of the Bubble",
        f"**Generated on:** {generator_time}",
        "",
        "This report aggregates claims extracted from monitored sources to determine which capabilities are 'Inside the Bubble' (solved), 'Frontier', or 'Outside the Bubble'.",
        ""
    ]
    
    # Group claims by capability
    claims_by_cap = {}
    for claim in claims:
        cid = claim["capability_id"]
        if cid not in claims_by_cap:
            claims_by_cap[cid] = []
        claims_by_cap[cid].append(claim)
        
    for cap in capabilities:
        report_lines.append(f"## {cap.skill} (Status: {cap.current_status})")
        report_lines.append(f"*{cap.description}*")
        report_lines.append("")
        
        rel_claims = claims_by_cap.get(cap.id, [])
        if not rel_claims:
            report_lines.append("> No new claims extracted for this capability during this run.")
        else:
            report_lines.append("### Extracted Claims:")
            for c in rel_claims:
                status_icon = "✅" if c['success_level'].lower() == "success" else "❌" if c['success_level'].lower() == "failure" else "⚠️"
                report_lines.append(f"- **{status_icon} {c['model_name']}** (Confidence: {c['confidence']:.2f})")
                report_lines.append(f"  - *\"{c['quote']}\"*")
                if c.get('failure_mode'):
                    report_lines.append(f"  - **Failure Mode:** {c['failure_mode']}")
                report_lines.append(f"  - *Source: {c['source_id']}*")
        report_lines.append("\n---")
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Generated Markdown report at {output_file}")

if __name__ == "__main__":
    run_pipeline()
