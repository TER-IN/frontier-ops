import os
import json
from typing import List, Optional
from pydantic import BaseModel, Field
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# 1. Define the desired output schema for the LLM
class ExtractedClaim(BaseModel):
    capability_id: str = Field(description="The ID of the capability this claim refers to (from the provided taxonomy).")
    model_name: str = Field(description="The name of the AI model being discussed (e.g., 'GPT-4', 'Claude 3.5 Sonnet', 'Llama 3').")
    success_level: str = Field(description="Whether the claim indicates 'Success', 'Failure', or 'Mixed' results.")
    quote: str = Field(description="A direct, verbatim quote from the text that supports this claim.")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0 that this text is making a genuine, concrete claim about solving this task.", ge=0.0, le=1.0)
    failure_mode: Optional[str] = Field(description="If the claim is a 'Failure' or 'Mixed', describe exactly how the model failed in 1 sentence. Leave null otherwise.", default=None)

class ExtractionResult(BaseModel):
    claims: List[ExtractedClaim]

# 2. Define the Extractor Class
class ClaimExtractor:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("WARNING: OpenAI API key not found. Extractor will run in mock mode.")
            
    def _build_prompt(self, text: str, capabilities_json: str) -> str:
        prompt = f"""
        You are an intelligence analyst tracking the "Expanding AI Bubble". 
        Your task is to read the following text (e.g., from a YouTube transcript or blog post) 
        and determine if the author makes concrete claims about an AI model's ability to perform 
        ANY of the capabilities listed in our taxonomy.
        
        Our Taxonomy of tracked capabilities:
        {capabilities_json}
        
        Text to analyze:
        ---
        {text[:15000]} # Truncated for token limits in MVP
        ---
        
        Extract all valid claims that match our taxonomy. If the text does not make any concrete claims about these specific skills, return an empty list of claims.
        """
        return prompt

    def extract(self, text: str, capabilities: List[BaseModel]) -> List[ExtractedClaim]:
        """Extracts claims from text using OpenAI's structured outputs."""
        if not self.client:
            print("Mock mode: returning empty claim list.")
            return []
            
        # Convert capability taxonomy to a string representation for the prompt
        caps_dict = [cap.model_dump() for cap in capabilities]
        caps_str = json.dumps(caps_dict, indent=2)
        
        prompt = self._build_prompt(text, caps_str)
        
        try:
            # We use structured outputs feature to guarantee the schema
            response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a precise data extraction engine. You only return structured JSON matching the provided schema."},
                    {"role": "user", "content": prompt}
                ],
                response_format=ExtractionResult,
                temperature=0.1
            )
            
            result: ExtractionResult = response.choices[0].message.parsed
            return result.claims
        except Exception as e:
            print(f"Extraction failed: {e}")
            return []

if __name__ == "__main__":
    # A quick mock test to see if it instantiates cleanly
    from src.models.capabilities import load_capabilities
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing Extractor Initialization...")
    extractor = ClaimExtractor()
    caps = load_capabilities()
    
    sample_text = "In our tests yesterday, we found that Claude 3.5 Sonnet completely failed at Unstructured PDF Table Parsing. It mangled all the columns when dealing with scanned financial reports."
    
    if extractor.client:
        print("Running live extraction to test API...")
        claims = extractor.extract(sample_text, caps)
        for claim in claims:
            print(f"Extracted: {claim.model_name} -> {claim.capability_id} ({claim.success_level})")
            if claim.failure_mode:
                print(f"  Failure Mode: {claim.failure_mode}")
            print(f"  Quote: '{claim.quote}'")
    else:
        print("Set OPENAI_API_KEY environment variable to run the live test.")
