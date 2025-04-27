from mistralai.client import MistralClient
from config import settings
from typing import List, Dict
import json

class JobMatchingService:
    def __init__(self):
        self.client = MistralClient(api_key=settings.MISTRAL_API_KEY)
    
    def match_resume_to_jds(self, resume_text: str, jds: List[Dict]) -> List[Dict]:
        prompt = f"""
        You are an AI hiring assistant. Analyze this resume and match it against the following job descriptions.
        For each job, provide:
        - match_score (0-100)
        - matching_skills
        - missing_skills
        - overall_fit_analysis
        
        Resume:
        {resume_text}
        
        Job Descriptions:
        {json.dumps(jds, indent=2)}
        
        Return a JSON array of matches sorted by match_score descending.
        """
        
        response = self.client.chat(
            model="mistral-medium",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return []