"""
Resume Intelligence Router
Handles resume parsing, data extraction, and confidence scoring

Key Features:
1. PDF/DOCX file parsing
2. Structured data extraction (name, email, skills, experience)
3. Confidence scoring for each extracted field
4. Interactive correction API
"""
import re
import io
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Candidate, Skill

router = APIRouter(prefix="/api/resume", tags=["Resume Intelligence"])


# ============================================================
# Pydantic Schemas
# ============================================================

class ExtractedField(BaseModel):
    """A single extracted field with its confidence score"""
    value: Any
    confidence: int  # 0-100
    source: str      # Where in the document this was found
    needs_review: bool


class ParsedResume(BaseModel):
    """Complete parsed resume with all fields and confidence scores"""
    full_name: ExtractedField
    email: ExtractedField
    phone: ExtractedField
    location: ExtractedField
    current_role: ExtractedField
    years_of_experience: ExtractedField
    skills: List[ExtractedField]
    education: List[Dict]
    work_experience: List[Dict]
    overall_confidence: int
    raw_text: str


class ProfileUpdate(BaseModel):
    """User correction for a parsed field"""
    field_name: str
    corrected_value: Any


# ============================================================
# Extraction Helpers with Confidence Scoring
# ============================================================

# Common email pattern
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Phone patterns (Indian & International)
PHONE_REGEX = re.compile(r'(?:\+91[\-\s]?)?[6-9]\d{9}|(?:\+1[\-\s]?)?\d{3}[\-\s]?\d{3}[\-\s]?\d{4}')

# Known skills list for matching
KNOWN_SKILLS = {
    # Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin",
    # Frameworks
    "react", "angular", "vue", "nextjs", "django", "flask", "fastapi", "express", "spring", "rails",
    # Databases
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "dynamodb", "sqlite",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "github actions", "ci/cd",
    # Data & ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "spark", "airflow", "kafka",
    # Tools
    "git", "linux", "rest api", "graphql", "microservices", "agile", "scrum"
}


def extract_email(text: str) -> ExtractedField:
    """Extract email with validation confidence"""
    matches = EMAIL_REGEX.findall(text)
    if matches:
        email = matches[0].lower()
        # Higher confidence for common domains
        trusted_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
        domain = email.split('@')[1] if '@' in email else ''
        confidence = 100 if domain in trusted_domains else 85
        return ExtractedField(
            value=email,
            confidence=confidence,
            source="Pattern matching",
            needs_review=False
        )
    return ExtractedField(
        value="",
        confidence=0,
        source="Not found",
        needs_review=True
    )


def extract_phone(text: str) -> ExtractedField:
    """Extract phone number with format validation"""
    matches = PHONE_REGEX.findall(text)
    if matches:
        phone = re.sub(r'[\s\-]', '', matches[0])
        # Indian numbers get higher confidence
        confidence = 95 if phone.startswith('+91') or (len(phone) == 10 and phone[0] in '6789') else 80
        return ExtractedField(
            value=phone,
            confidence=confidence,
            source="Pattern matching",
            needs_review=False
        )
    return ExtractedField(
        value="",
        confidence=0,
        source="Not found",
        needs_review=True
    )


def extract_name(text: str) -> ExtractedField:
    """Extract name - typically first line or after common headers"""
    lines = text.strip().split('\n')
    
    # Skip empty lines and common headers
    skip_words = {'resume', 'curriculum vitae', 'cv', 'profile', 'contact'}
    
    for line in lines[:5]:  # Check first 5 lines
        clean_line = line.strip()
        if clean_line and not any(word in clean_line.lower() for word in skip_words):
            # Check if it looks like a name (2-4 words, no numbers)
            words = clean_line.split()
            if 2 <= len(words) <= 4 and not any(char.isdigit() for char in clean_line):
                return ExtractedField(
                    value=clean_line.title(),
                    confidence=75,
                    source="First non-header line",
                    needs_review=True  # Names always need review
                )
    
    return ExtractedField(
        value="Unknown",
        confidence=0,
        source="Could not extract",
        needs_review=True
    )


def extract_skills(text: str) -> List[ExtractedField]:
    """Extract skills by matching against known skill taxonomy"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in KNOWN_SKILLS:
        # Use word boundary matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(ExtractedField(
                value=skill.title(),
                confidence=90,
                source="Skill taxonomy match",
                needs_review=False
            ))
    
    return found_skills


def extract_experience_years(text: str) -> ExtractedField:
    """Extract years of experience from text"""
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience',
        r'experience\s*[:\-]?\s*(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)\s*in\s*(?:software|development|tech)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            years = float(match.group(1))
            return ExtractedField(
                value=years,
                confidence=85,
                source="Pattern matching",
                needs_review=True
            )
    
    # Try to infer from work history dates (simplified)
    return ExtractedField(
        value=0,
        confidence=0,
        source="Could not determine",
        needs_review=True
    )


def extract_location(text: str) -> ExtractedField:
    """Extract location - look for city/state patterns"""
    # Major Indian cities
    cities = [
        'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'chennai', 
        'pune', 'kolkata', 'ahmedabad', 'jaipur', 'noida', 'gurgaon', 'gurugram'
    ]
    
    text_lower = text.lower()
    for city in cities:
        if city in text_lower:
            return ExtractedField(
                value=city.title(),
                confidence=80,
                source="City name match",
                needs_review=True
            )
    
    return ExtractedField(
        value="",
        confidence=0,
        source="Not found",
        needs_review=True
    )


def calculate_overall_confidence(parsed: Dict) -> int:
    """Calculate weighted overall confidence score"""
    weights = {
        'email': 0.20,
        'phone': 0.10,
        'full_name': 0.15,
        'skills': 0.30,
        'experience': 0.15,
        'location': 0.10
    }
    
    total = 0
    total += parsed['email'].confidence * weights['email']
    total += parsed['phone'].confidence * weights['phone']
    total += parsed['full_name'].confidence * weights['full_name']
    total += parsed['location'].confidence * weights['location']
    total += parsed['years_of_experience'].confidence * weights['experience']
    
    # Skills confidence is average of all found skills
    if parsed['skills']:
        avg_skill_conf = sum(s.confidence for s in parsed['skills']) / len(parsed['skills'])
        total += avg_skill_conf * weights['skills']
    
    return int(total)


# ============================================================
# API Endpoints
# ============================================================

@router.post("/parse", response_model=ParsedResume)
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse an uploaded resume (PDF/DOCX) and extract structured data.
    Returns confidence scores for each extracted field.
    """
    # Validate file type
    allowed_types = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Please upload a PDF or DOCX file."
        )
    
    # Read file content
    content = await file.read()
    
    # Extract text based on file type
    file_type = allowed_types[file.content_type]
    
    try:
        if file_type == "pdf":
            text = extract_text_from_pdf(content)
        else:
            text = extract_text_from_docx(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing file: {str(e)}"
        )
    
    if not text or len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Could not extract sufficient text from the document. Please ensure the file is not corrupted or empty."
        )
    
    # Extract all fields
    parsed = {
        'full_name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'location': extract_location(text),
        'current_role': ExtractedField(value="", confidence=0, source="Not implemented", needs_review=True),
        'years_of_experience': extract_experience_years(text),
        'skills': extract_skills(text),
        'education': [],
        'work_experience': [],
    }
    
    overall_confidence = calculate_overall_confidence(parsed)
    
    return ParsedResume(
        **parsed,
        overall_confidence=overall_confidence,
        raw_text=text[:2000]  # Limit raw text length
    )


@router.post("/save/{candidate_id}")
async def save_parsed_profile(
    candidate_id: int,
    profile: ParsedResume,
    db: Session = Depends(get_db)
):
    """
    Save or update a parsed profile to the database.
    Can be called after user corrections.
    """
    # Check if candidate exists
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    
    if not candidate:
        # Create new candidate
        candidate = Candidate(
            full_name=profile.full_name.value,
            email=profile.email.value,
            phone=profile.phone.value,
            location=profile.location.value,
            current_role=profile.current_role.value,
            years_of_experience=profile.years_of_experience.value,
            raw_resume_text=profile.raw_text,
            confidence_scores={
                'full_name': profile.full_name.confidence,
                'email': profile.email.confidence,
                'phone': profile.phone.confidence,
                'location': profile.location.confidence,
                'skills': [s.confidence for s in profile.skills],
                'overall': profile.overall_confidence
            }
        )
        db.add(candidate)
    else:
        # Update existing
        candidate.full_name = profile.full_name.value
        candidate.email = profile.email.value
        candidate.phone = profile.phone.value
        candidate.location = profile.location.value
        candidate.years_of_experience = profile.years_of_experience.value
    
    db.commit()
    db.refresh(candidate)
    
    return {"message": "Profile saved successfully", "candidate_id": candidate.id}


# ============================================================
# File Parsing Helpers
# ============================================================

def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF using pdfplumber"""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text_parts = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return '\n'.join(text_parts)
    except ImportError:
        # Fallback message if pdfplumber not installed
        return "[PDF parsing library not available]"
    except Exception as e:
        raise Exception(f"PDF parsing error: {str(e)}")


def extract_text_from_docx(content: bytes) -> str:
    """Extract text from DOCX using python-docx"""
    try:
        from docx import Document
        doc = Document(io.BytesIO(content))
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except ImportError:
        return "[DOCX parsing library not available]"
    except Exception as e:
        raise Exception(f"DOCX parsing error: {str(e)}")
