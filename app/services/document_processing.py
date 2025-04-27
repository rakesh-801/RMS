from mistralai.client import MistralClient
import PyPDF2
from io import BytesIO
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.mistral_client = MistralClient(api_key="kggSszmQIlWUC0J4bbWfDcuOZvkawkeE")
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text content from PDF resume"""
        with BytesIO(file_bytes) as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def parse_resume(self, resume_text: str) -> dict:
        """Parse resume text and extract structured data"""
        prompt = '''
        You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
        1. full name (split into firstName and lastName)
        2. email id
        3. github portfolio
        4. linkedin id
        5. employment details (currentRole, currentEmployer, experienceHistory)
        6. technical skills
        7. soft skills
        8. educational details
        9. certifications
        10. publications
        11. industry contributions
        12. currentCTC (if mentioned)
        13. expectedCTC (if mentioned)
        Give the extracted information in json format only. if you do not find any of the above information in the resume, then return empty string for that field. Do not return any other information apart from the json data. The json data should be in the following format:
        '''

        response = self.mistral_client.chat(
            model="mistral-medium",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": resume_text}
            ],
            temperature=0.0,
            max_tokens=1500
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Handle cases where the response isn't valid JSON
            return {}

    def parse_job_description(self, jd_text: str) -> dict:
        """Parse job description text and extract structured data"""
        prompt = '''
        You are an AI bot designed to parse job descriptions. Extract the following information:
        1. jdName (job title)
        2. role
        3. responsibilities (as a single string)
        4. primarySkills (comma-separated)
        5. secondarySkills (comma-separated)
        6. academicQualifications
        7. requiredCertifications
        8. status (default to ACTIVE)
        Return the data in JSON format with keys matching the database schema.
        '''

        response = self.mistral_client.chat(
            model="mistral-medium",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": jd_text}
            ],
            temperature=0.0,
            max_tokens=1500
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {}