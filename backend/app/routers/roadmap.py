"""
Actionable Growth Router
Personalized Learning Roadmap Generator

Uses skill dependency topology to create phased learning paths
based on skill gaps between candidate and target job.
"""
import json
from typing import List, Dict, Optional
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/roadmap", tags=["Actionable Growth"])


# ============================================================
# Pydantic Schemas
# ============================================================

class LearningResource(BaseModel):
    """A single learning resource"""
    title: str
    type: str  # "course", "tutorial", "documentation", "project"
    url: Optional[str] = None
    provider: str
    estimated_hours: int
    is_free: bool


class SkillNode(BaseModel):
    """A skill in the learning roadmap"""
    name: str
    category: str
    difficulty: int  # 1-5
    estimated_weeks: float
    prerequisites: List[str]
    resources: List[LearningResource]
    why_needed: str  # Explanation of why this skill is needed


class LearningPhase(BaseModel):
    """A phase of learning containing related skills"""
    phase_number: int
    title: str
    description: str
    skills: List[SkillNode]
    total_weeks: float
    milestone: str  # What you can do after this phase


class RoadmapResponse(BaseModel):
    """Complete learning roadmap"""
    target_job: str
    target_company: str
    current_match_score: float
    projected_match_score: float
    missing_skills_count: int
    phases: List[LearningPhase]
    total_estimated_weeks: float
    total_estimated_hours: int
    summary: str
    motivation_message: str


class RoadmapRequest(BaseModel):
    """Request for generating a roadmap"""
    current_skills: List[str]
    target_job_id: int
    learning_pace: str = "moderate"  # "intensive", "moderate", "relaxed"


# ============================================================
# Skill Resource Database
# ============================================================

SKILL_RESOURCES = {
    "python": {
        "category": "Programming",
        "difficulty": 2,
        "prerequisites": [],
        "estimated_weeks": 4,
        "resources": [
            {
                "title": "Python for Everybody",
                "type": "course",
                "url": "https://www.coursera.org/specializations/python",
                "provider": "Coursera / University of Michigan",
                "estimated_hours": 40,
                "is_free": True
            },
            {
                "title": "Automate the Boring Stuff with Python",
                "type": "course",
                "url": "https://automatetheboringstuff.com/",
                "provider": "Al Sweigart",
                "estimated_hours": 20,
                "is_free": True
            }
        ]
    },
    "fastapi": {
        "category": "Backend Framework",
        "difficulty": 3,
        "prerequisites": ["python"],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "FastAPI Official Tutorial",
                "type": "documentation",
                "url": "https://fastapi.tiangolo.com/tutorial/",
                "provider": "FastAPI",
                "estimated_hours": 10,
                "is_free": True
            },
            {
                "title": "Build a REST API with FastAPI",
                "type": "project",
                "url": "https://testdriven.io/courses/tdd-fastapi/",
                "provider": "TestDriven.io",
                "estimated_hours": 15,
                "is_free": False
            }
        ]
    },
    "postgresql": {
        "category": "Database",
        "difficulty": 3,
        "prerequisites": ["sql"],
        "estimated_weeks": 3,
        "resources": [
            {
                "title": "PostgreSQL Tutorial",
                "type": "tutorial",
                "url": "https://www.postgresqltutorial.com/",
                "provider": "PostgreSQL Tutorial",
                "estimated_hours": 15,
                "is_free": True
            },
            {
                "title": "PostgreSQL Exercises",
                "type": "project",
                "url": "https://pgexercises.com/",
                "provider": "PG Exercises",
                "estimated_hours": 10,
                "is_free": True
            }
        ]
    },
    "sql": {
        "category": "Database",
        "difficulty": 2,
        "prerequisites": [],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "SQLZoo",
                "type": "tutorial",
                "url": "https://sqlzoo.net/",
                "provider": "SQLZoo",
                "estimated_hours": 8,
                "is_free": True
            },
            {
                "title": "SQL for Data Science",
                "type": "course",
                "url": "https://www.coursera.org/learn/sql-for-data-science",
                "provider": "Coursera / UC Davis",
                "estimated_hours": 20,
                "is_free": True
            }
        ]
    },
    "docker": {
        "category": "DevOps",
        "difficulty": 3,
        "prerequisites": [],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "Docker Getting Started",
                "type": "documentation",
                "url": "https://docs.docker.com/get-started/",
                "provider": "Docker",
                "estimated_hours": 5,
                "is_free": True
            },
            {
                "title": "Docker for Developers",
                "type": "course",
                "url": "https://www.udemy.com/course/docker-mastery/",
                "provider": "Udemy",
                "estimated_hours": 20,
                "is_free": False
            }
        ]
    },
    "kubernetes": {
        "category": "DevOps",
        "difficulty": 4,
        "prerequisites": ["docker"],
        "estimated_weeks": 4,
        "resources": [
            {
                "title": "Kubernetes Basics",
                "type": "tutorial",
                "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
                "provider": "Kubernetes",
                "estimated_hours": 10,
                "is_free": True
            },
            {
                "title": "CKA Certification Prep",
                "type": "course",
                "url": "https://kodekloud.com/courses/certified-kubernetes-administrator-cka/",
                "provider": "KodeKloud",
                "estimated_hours": 40,
                "is_free": False
            }
        ]
    },
    "aws": {
        "category": "Cloud",
        "difficulty": 4,
        "prerequisites": [],
        "estimated_weeks": 6,
        "resources": [
            {
                "title": "AWS Cloud Practitioner Essentials",
                "type": "course",
                "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
                "provider": "AWS",
                "estimated_hours": 6,
                "is_free": True
            },
            {
                "title": "AWS Free Tier Hands-On Labs",
                "type": "project",
                "url": "https://aws.amazon.com/free/",
                "provider": "AWS",
                "estimated_hours": 30,
                "is_free": True
            }
        ]
    },
    "react": {
        "category": "Frontend Framework",
        "difficulty": 3,
        "prerequisites": ["javascript"],
        "estimated_weeks": 4,
        "resources": [
            {
                "title": "React Official Tutorial",
                "type": "documentation",
                "url": "https://react.dev/learn",
                "provider": "React",
                "estimated_hours": 15,
                "is_free": True
            },
            {
                "title": "Full Stack Open - React",
                "type": "course",
                "url": "https://fullstackopen.com/en/",
                "provider": "University of Helsinki",
                "estimated_hours": 40,
                "is_free": True
            }
        ]
    },
    "javascript": {
        "category": "Programming",
        "difficulty": 2,
        "prerequisites": [],
        "estimated_weeks": 4,
        "resources": [
            {
                "title": "JavaScript.info",
                "type": "tutorial",
                "url": "https://javascript.info/",
                "provider": "JavaScript.info",
                "estimated_hours": 30,
                "is_free": True
            },
            {
                "title": "freeCodeCamp JavaScript",
                "type": "course",
                "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/",
                "provider": "freeCodeCamp",
                "estimated_hours": 40,
                "is_free": True
            }
        ]
    },
    "typescript": {
        "category": "Programming",
        "difficulty": 3,
        "prerequisites": ["javascript"],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "TypeScript Handbook",
                "type": "documentation",
                "url": "https://www.typescriptlang.org/docs/handbook/",
                "provider": "TypeScript",
                "estimated_hours": 10,
                "is_free": True
            }
        ]
    },
    "node.js": {
        "category": "Backend Runtime",
        "difficulty": 3,
        "prerequisites": ["javascript"],
        "estimated_weeks": 3,
        "resources": [
            {
                "title": "Node.js Documentation",
                "type": "documentation",
                "url": "https://nodejs.org/docs/latest/api/",
                "provider": "Node.js",
                "estimated_hours": 15,
                "is_free": True
            }
        ]
    },
    "mongodb": {
        "category": "Database",
        "difficulty": 2,
        "prerequisites": [],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "MongoDB University",
                "type": "course",
                "url": "https://university.mongodb.com/",
                "provider": "MongoDB",
                "estimated_hours": 20,
                "is_free": True
            }
        ]
    },
    "spark": {
        "category": "Big Data",
        "difficulty": 4,
        "prerequisites": ["python", "sql"],
        "estimated_weeks": 4,
        "resources": [
            {
                "title": "Apache Spark Documentation",
                "type": "documentation",
                "url": "https://spark.apache.org/docs/latest/",
                "provider": "Apache",
                "estimated_hours": 20,
                "is_free": True
            }
        ]
    },
    "airflow": {
        "category": "Orchestration",
        "difficulty": 3,
        "prerequisites": ["python"],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "Apache Airflow Tutorial",
                "type": "documentation",
                "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/",
                "provider": "Apache",
                "estimated_hours": 10,
                "is_free": True
            }
        ]
    },
    "terraform": {
        "category": "Infrastructure",
        "difficulty": 4,
        "prerequisites": [],
        "estimated_weeks": 3,
        "resources": [
            {
                "title": "Terraform Getting Started",
                "type": "documentation",
                "url": "https://learn.hashicorp.com/terraform",
                "provider": "HashiCorp",
                "estimated_hours": 15,
                "is_free": True
            }
        ]
    },
    "redis": {
        "category": "Database",
        "difficulty": 2,
        "prerequisites": [],
        "estimated_weeks": 1,
        "resources": [
            {
                "title": "Redis University",
                "type": "course",
                "url": "https://university.redis.com/",
                "provider": "Redis",
                "estimated_hours": 8,
                "is_free": True
            }
        ]
    },
    "graphql": {
        "category": "API",
        "difficulty": 3,
        "prerequisites": ["javascript"],
        "estimated_weeks": 2,
        "resources": [
            {
                "title": "GraphQL Official Learn",
                "type": "documentation",
                "url": "https://graphql.org/learn/",
                "provider": "GraphQL Foundation",
                "estimated_hours": 10,
                "is_free": True
            }
        ]
    }
}


# ============================================================
# Topology Sorting for Skill Dependencies
# ============================================================

def topological_sort_skills(missing_skills: List[str]) -> List[List[str]]:
    """
    Sort skills into phases based on dependencies.
    Returns list of phases, where each phase contains skills
    that can be learned in parallel.
    """
    missing_lower = {s.lower() for s in missing_skills}
    
    # Build dependency graph for missing skills
    dependencies = {}
    for skill in missing_lower:
        skill_data = SKILL_RESOURCES.get(skill, {})
        prereqs = skill_data.get('prerequisites', [])
        # Only include prerequisites that are also missing
        relevant_prereqs = [p for p in prereqs if p.lower() in missing_lower]
        dependencies[skill] = set(relevant_prereqs)
    
    # Kahn's algorithm for topological sorting into phases
    phases = []
    remaining = set(missing_lower)
    
    while remaining:
        # Find skills with no unsatisfied dependencies
        phase = []
        for skill in remaining:
            prereqs = dependencies.get(skill, set())
            if not prereqs & remaining:  # All prereqs satisfied
                phase.append(skill)
        
        if not phase:
            # Circular dependency or misconfiguration - add remaining as one phase
            phases.append(list(remaining))
            break
        
        phases.append(phase)
        remaining -= set(phase)
    
    return phases


def get_skill_node(skill_name: str, job_required_skills: List[str]) -> SkillNode:
    """Create a SkillNode with full details for a skill"""
    skill_lower = skill_name.lower()
    skill_data = SKILL_RESOURCES.get(skill_lower, {})
    
    # Determine why this skill is needed
    is_required = skill_name.lower() in [s.lower() for s in job_required_skills]
    why = f"Required skill for this role" if is_required else "Nice-to-have skill that strengthens your profile"
    
    resources = [
        LearningResource(**res) 
        for res in skill_data.get('resources', [])
    ]
    
    # Default resources if not found
    if not resources:
        resources = [
            LearningResource(
                title=f"Learn {skill_name.title()}",
                type="tutorial",
                provider="Various",
                estimated_hours=10,
                is_free=True
            )
        ]
    
    return SkillNode(
        name=skill_name.title(),
        category=skill_data.get('category', 'Technical'),
        difficulty=skill_data.get('difficulty', 3),
        estimated_weeks=skill_data.get('estimated_weeks', 2),
        prerequisites=[p.title() for p in skill_data.get('prerequisites', [])],
        resources=resources,
        why_needed=why
    )


def calculate_phase_weeks(skills: List[SkillNode], pace: str) -> float:
    """Calculate total weeks for a phase based on pace"""
    base_weeks = sum(s.estimated_weeks for s in skills)
    
    # Adjust for pace - skills in a phase can be learned in parallel
    parallel_factor = 0.7  # Some parallelization possible
    
    pace_multipliers = {
        "intensive": 0.6,   # Full-time learning
        "moderate": 1.0,    # Normal pace
        "relaxed": 1.5      # Part-time learning
    }
    
    multiplier = pace_multipliers.get(pace, 1.0)
    
    return round(base_weeks * parallel_factor * multiplier, 1)


PHASE_TITLES = [
    "Foundation",
    "Core Skills",
    "Advanced Topics",
    "Specialization",
    "Mastery"
]

PHASE_MILESTONES = [
    "You'll have the fundamentals to start building",
    "You can contribute to real projects",
    "You'll be comfortable with complex implementations",
    "You'll be an expert in key areas",
    "You'll be ready for senior-level responsibilities"
]


# ============================================================
# API Endpoints
# ============================================================

@router.post("/generate", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """
    Generate a personalized learning roadmap based on skill gaps.
    Uses topological sorting to order skills by dependencies.
    """
    # Load jobs data
    jobs_file = Path(__file__).parent.parent.parent / "data" / "jobs.json"
    
    try:
        with open(jobs_file, 'r') as f:
            data = json.load(f)
            jobs = {j['id']: j for j in data.get('jobs', [])}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jobs data not found")
    
    # Get target job
    job = jobs.get(request.target_job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {request.target_job_id} not found")
    
    # Identify missing skills
    current_skills_lower = {s.lower() for s in request.current_skills}
    required_skills = job.get('required_skills', [])
    optional_skills = job.get('nice_to_have_skills', [])
    
    all_job_skills = required_skills + optional_skills
    missing_skills = [s for s in all_job_skills if s.lower() not in current_skills_lower]
    
    if not missing_skills:
        return RoadmapResponse(
            target_job=job['title'],
            target_company=job['company'],
            current_match_score=100.0,
            projected_match_score=100.0,
            missing_skills_count=0,
            phases=[],
            total_estimated_weeks=0,
            total_estimated_hours=0,
            summary="Congratulations! You already have all the skills for this role.",
            motivation_message="🎉 You're ready to apply! Your skills are a perfect match."
        )
    
    # Sort skills into phases by dependencies
    skill_phases = topological_sort_skills(missing_skills)
    
    # Build detailed phases
    phases = []
    total_weeks = 0
    total_hours = 0
    
    for i, phase_skills in enumerate(skill_phases):
        skill_nodes = [get_skill_node(s, required_skills) for s in phase_skills]
        phase_weeks = calculate_phase_weeks(skill_nodes, request.learning_pace)
        phase_hours = sum(
            sum(r.estimated_hours for r in s.resources)
            for s in skill_nodes
        )
        
        phases.append(LearningPhase(
            phase_number=i + 1,
            title=PHASE_TITLES[min(i, len(PHASE_TITLES) - 1)],
            description=f"Learn {', '.join(s.name for s in skill_nodes)}",
            skills=skill_nodes,
            total_weeks=phase_weeks,
            milestone=PHASE_MILESTONES[min(i, len(PHASE_MILESTONES) - 1)]
        ))
        
        total_weeks += phase_weeks
        total_hours += phase_hours
    
    # Calculate score improvement
    matching_count = len(request.current_skills)
    total_count = len(all_job_skills)
    current_score = (matching_count / total_count * 100) if total_count > 0 else 0
    projected_score = 100.0  # After learning all skills
    
    # Generate summary
    weeks_text = f"{int(total_weeks)} weeks" if total_weeks >= 1 else f"{int(total_weeks * 4)} days"
    summary = (
        f"To become a strong candidate for {job['title']} at {job['company']}, "
        f"you need to learn {len(missing_skills)} skills across {len(phases)} phases. "
        f"Estimated timeline: {weeks_text} at a {request.learning_pace} pace."
    )
    
    motivation = _get_motivation_message(len(missing_skills), total_weeks)
    
    return RoadmapResponse(
        target_job=job['title'],
        target_company=job['company'],
        current_match_score=round(current_score, 1),
        projected_match_score=projected_score,
        missing_skills_count=len(missing_skills),
        phases=phases,
        total_estimated_weeks=total_weeks,
        total_estimated_hours=total_hours,
        summary=summary,
        motivation_message=motivation
    )


@router.get("/skills")
async def get_available_skills():
    """Get all skills in the taxonomy with their metadata"""
    return {
        skill: {
            "category": data.get("category"),
            "difficulty": data.get("difficulty"),
            "prerequisites": data.get("prerequisites", []),
            "estimated_weeks": data.get("estimated_weeks")
        }
        for skill, data in SKILL_RESOURCES.items()
    }


def _get_motivation_message(missing_count: int, weeks: float) -> str:
    """Generate an encouraging message based on the gap size"""
    if missing_count <= 2:
        return "🚀 You're almost there! Just a few skills to learn and you'll be a perfect match."
    elif missing_count <= 5:
        return "💪 A solid learning journey ahead! With dedication, you'll be job-ready soon."
    elif weeks <= 8:
        return "📚 This is achievable! Many developers have bridged similar gaps in a few months."
    else:
        return "🎯 A significant but rewarding journey. Break it into phases and celebrate each milestone!"
