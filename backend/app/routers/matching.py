from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..db import get_db, JobPosting
from ..schemas.matching import MatchRequest, MatchResponse, JobMatch
from ..services.matching_service import MatchingEngine

router = APIRouter(prefix="/api/matching", tags=["Transparent Matching"])

# Service instance
engine = MatchingEngine()


@router.post("/calculate", response_model=MatchResponse)
async def calculate_matches(request: MatchRequest, db: Session = Depends(get_db)):
    """
    Match a candidate against all available jobs from the database.
    Uses fuzzy matching for skills and roles.
    """
    # Load jobs from database
    jobs = db.query(JobPosting).all()
    
    if not jobs:
        raise HTTPException(status_code=404, detail="No job postings found in the database.")
    
    candidate_data = request.dict()
    education_data = candidate_data.get('education') or {}
    # Handle list of education entries vs single dict if necessary, but here we just want a field for logging
    field = "Unknown"
    if isinstance(education_data, list) and education_data:
        field = education_data[0].get('field', 'Unknown')
    elif isinstance(education_data, dict):
        field = education_data.get('field', 'Unknown')
    
    # Visual console output
    print(f"\n--- API Match Results for {field} Candidate ---")
    print(f"Skills: {', '.join(candidate_data.get('skills', []))}")
    print("-" * 50)
    
    results = []
    
    for job in jobs:
        # Convert model to dict for matching service compatibility
        job_data = {
            "id": job.id,
            "title": job.title,
            "required_skills": job.required_skills,
            "nice_to_have_skills": job.nice_to_have_skills,
            "location": job.location,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "min_experience_years": job.min_experience_years
        }

        # 1. Skill Match
        skill_score, matching, missing_req, missing_opt = engine.calculate_skills_score(
            candidate_data.get('skills', []),
            job_data.get('required_skills', []),
            job_data.get('nice_to_have_skills', [])
        )
        
        # 2. Location Match
        location_score = engine.calculate_location_score(
            candidate_data.get('preferred_locations', []),
            job_data.get('location', '') or ''
        )
        
        # 3. Salary Match
        # Handle salary extraction from dict safely
        exp_salary_data = candidate_data.get('expected_salary')
        exp_salary_val = 0
        if isinstance(exp_salary_data, dict):
            exp_salary_val = exp_salary_data.get('min', 0)
        elif isinstance(exp_salary_data, (int, float)):
            exp_salary_val = exp_salary_data
            
        salary_score = engine.calculate_salary_score(
            exp_salary_val,
            job_data.get('salary_min') or 0,
            job_data.get('salary_max') or 0
        )
        
        # 4. Experience Match
        experience_score = engine.calculate_experience_score(
            candidate_data.get('experience_years') or 0,
            job_data.get('min_experience_years') or 0
        )
        
        # 5. Role Match
        role_score = engine.calculate_role_score(
            candidate_data.get('preferred_roles', []),
            job_data.get('title', '')
        )
        
        # Prepare breakdown dict for total score and generation
        temp_result = {
            "job_id": job.id,
            "job_title": job.title,
            "missing_skills": missing_req,
            "breakdown": {
                "skill_match": skill_score,
                "location_match": location_score,
                "salary_match": salary_score,
                "experience_match": experience_score,
                "role_match": role_score
            }
        }
        
        total_score = engine.calculate_total_score(temp_result['breakdown'])
        explanation, top_reason, improve = engine.generate_explanation(temp_result)
        
        job_match = JobMatch(
            job_id=job.id,
            job_title=job.title,
            match_score=total_score,
            match_tier=engine.get_match_tier(total_score),
            breakdown=temp_result['breakdown'],
            missing_skills=missing_req,
            explanation=explanation,
            top_reason_for_match=top_reason,
            top_area_to_improve=improve
        )
        
        # Console logging
        print(f"Job: {job.title} (ID: {job.id})")
        print(f"Score: {total_score}%")
        print(f"Skill Match: {skill_score}% | Location: {location_score}% | Salary: {salary_score}%")
        print("-" * 30)
        
        results.append(job_match)
    
    # Sort results by score descending
    results.sort(key=lambda x: x.match_score, reverse=True)
    
    return MatchResponse(
        candidate=candidate_data.get('full_name', 'Candidate'),
        field=field,
        matches=results
    )
