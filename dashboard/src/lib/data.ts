export interface Capability {
  id: string;
  domain: string;
  skill: string;
  description: string;
  success_criteria: string;
  current_status: string;
}

export interface Claim {
  capability_id: string;
  model_name: string;
  success_level: string;
  quote: string;
  confidence: number;
  failure_mode: string | null;
  source_id: string;
  extracted_at: string;
}

// We will fetch this statically from the data folders at build time
// For a production app this would ideally be an API route pointing to a DB
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';

export function getCapabilities(): Capability[] {
  const filePath = path.join(process.cwd(), '../data/CAPABILITIES.yml');
  try {
    const fileContents = fs.readFileSync(filePath, 'utf8');
    const parsed: any = yaml.load(fileContents);
    return parsed.caps || [];
  } catch (error) {
    console.error("Error loading capabilities:", error);
    return [];
  }
}

export function getClaims(): Claim[] {
  const filePath = path.join(process.cwd(), '../data/extracted_claims.json');
  try {
    if (fs.existsSync(filePath)) {
      const fileContents = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(fileContents);
    }
    return [];
  } catch (error) {
    console.error("Error loading claims:", error);
    return [];
  }
}
