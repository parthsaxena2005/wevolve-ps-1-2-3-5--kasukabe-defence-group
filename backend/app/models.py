"""
SQLAlchemy Models for Wevolve
Defines the database schema for CandidateProfiles, JobPostings, and SkillTaxonomy
"""
from sqlalchemy import Column, Integer, String, Float, Text, JSON, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between candidates and skills
candidate_skills = Table(
    'candidate_skills',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('proficiency_level', Integer, default=1)  # 1-5 scale
)

# Association table for many-to-many relationship between jobs and required skills
job_skills = Table(
    'job_skills',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('is_required', Boolean, default=True)  # Required vs Nice-to-have
)


class Skill(Base):
    """
    Skill Taxonomy - Centralized skill database
    Used for matching and gap analysis
    """
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category = Column(String(50))  # e.g., "Programming", "Database", "Soft Skills"
    difficulty_level = Column(Integer, default=1)  # 1-5 scale for learning roadmap
    prerequisites = Column(JSON, default=[])  # List of skill IDs that should be learned first
    
    def __repr__(self):
        return f"<Skill(name='{self.name}', category='{self.category}')>"


class Candidate(Base):
    """
    Candidate Profile - Parsed from resume
    Stores extracted data with confidence scores
    """
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    full_name = Column(String(200))
    email = Column(String(200), index=True)
    phone = Column(String(50))
    location = Column(String(200))
    
    # Professional Information
    current_role = Column(String(200))
    years_of_experience = Column(Float, default=0)
    expected_salary_min = Column(Integer)
    expected_salary_max = Column(Integer)
    
    # Parsed Content (stored as structured JSON)
    education = Column(JSON, default=[])  # List of education entries
    work_experience = Column(JSON, default=[])  # List of work experience entries
    certifications = Column(JSON, default=[])
    
    # Confidence Scores (0-100 for each field)
    confidence_scores = Column(JSON, default={})
    
    # Raw resume text for reference
    raw_resume_text = Column(Text)
    resume_file_path = Column(String(500))
    
    # Relationships
    skills = relationship("Skill", secondary=candidate_skills, backref="candidates")
    
    def __repr__(self):
        return f"<Candidate(name='{self.full_name}', email='{self.email}')>"


class Job(Base):
    """
    Job Posting - Jobs available for matching
    """
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Location & Work Type
    location = Column(String(200))
    is_remote = Column(Boolean, default=False)
    
    # Compensation
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    
    # Requirements
    min_experience_years = Column(Float, default=0)
    max_experience_years = Column(Float)
    
    # Relationships
    required_skills = relationship("Skill", secondary=job_skills, backref="jobs")
    
    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"


class MatchResult(Base):
    """
    Stores match results between candidates and jobs
    Includes breakdown of all scoring factors
    """
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Overall Score
    total_score = Column(Float, nullable=False)  # 0-100
    
    # Individual Factor Scores (weighted)
    skills_score = Column(Float)      # 40% weight
    location_score = Column(Float)    # 20% weight
    salary_score = Column(Float)      # 15% weight
    experience_score = Column(Float)  # 15% weight
    role_score = Column(Float)        # 10% weight
    
    # Detailed breakdown for transparency
    matching_skills = Column(JSON, default=[])
    missing_skills = Column(JSON, default=[])
    match_explanation = Column(Text)  # Human-readable explanation
    
    # Relationships
    candidate = relationship("Candidate", backref="matches")
    job = relationship("Job", backref="matches")
    
    def __repr__(self):
        return f"<MatchResult(candidate_id={self.candidate_id}, job_id={self.job_id}, score={self.total_score})>"
