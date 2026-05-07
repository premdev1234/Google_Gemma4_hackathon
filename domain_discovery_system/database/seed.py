# domain_discovery_system/database/seed.py

from sqlalchemy.orm import Session

from domain_discovery_system.database.connection import SessionLocal
from domain_discovery_system.database.models import (
    Trait,
    Domain,
    Subdomain,
    Specialization,
    Technology,
    TechnologyStack,
    StaticQuestion,
    StaticQuestionOption,
    TraitDomainMapping,
)

# =========================================================
# DATABASE SESSION
# =========================================================

db: Session = SessionLocal()

# =========================================================
# TRAITS DATA
# =========================================================

TRAITS = [
    {
        "trait_name": "Deep Focus",
        "trait_category": "Cognitive",
        "description": "Ability to concentrate deeply for long periods",
        "importance_score": 9.5,
    },
    {
        "trait_name": "Persistence",
        "trait_category": "Behavioral",
        "description": "Ability to continue solving difficult problems",
        "importance_score": 9.2,
    },
    {
        "trait_name": "Analytical Thinking",
        "trait_category": "Cognitive",
        "description": "Ability to break problems logically",
        "importance_score": 9.4,
    },
    {
        "trait_name": "Creativity",
        "trait_category": "Creative",
        "description": "Ability to think uniquely and creatively",
        "importance_score": 8.7,
    },
    {
        "trait_name": "Systems Thinking",
        "trait_category": "Engineering",
        "description": "Ability to understand large systems",
        "importance_score": 9.3,
    },
    {
        "trait_name": "Curiosity",
        "trait_category": "Psychological",
        "description": "Strong desire to explore and learn",
        "importance_score": 9.1,
    },
    {
        "trait_name": "Stress Tolerance",
        "trait_category": "Behavioral",
        "description": "Ability to remain stable under pressure",
        "importance_score": 8.8,
    },
]

# =========================================================
# DOMAINS DATA
# =========================================================

DOMAINS = [
    {
        "domain_name": "Backend Engineering",
        "description": "Server-side engineering and APIs",
        "market_demand_score": 9.7,
        "future_growth_score": 9.5,
    },
    {
        "domain_name": "AI/ML Engineering",
        "description": "Artificial Intelligence and Machine Learning",
        "market_demand_score": 10.0,
        "future_growth_score": 10.0,
    },
    {
        "domain_name": "Cybersecurity",
        "description": "Security engineering and threat prevention",
        "market_demand_score": 9.5,
        "future_growth_score": 9.6,
    },
    {
        "domain_name": "Cloud/DevOps",
        "description": "Cloud infrastructure and DevOps engineering",
        "market_demand_score": 9.4,
        "future_growth_score": 9.3,
    },
    {
        "domain_name": "Data Engineering",
        "description": "Data pipelines and big data systems",
        "market_demand_score": 9.2,
        "future_growth_score": 9.1,
    },
]

# =========================================================
# SUBDOMAINS DATA
# =========================================================

SUBDOMAINS = [
    {
        "domain_name": "Backend Engineering",
        "subdomain_name": "Distributed Systems",
        "description": "Scalable distributed architecture",
        "complexity_level": "Advanced",
    },
    {
        "domain_name": "Backend Engineering",
        "subdomain_name": "API Engineering",
        "description": "REST and GraphQL APIs",
        "complexity_level": "Intermediate",
    },
    {
        "domain_name": "AI/ML Engineering",
        "subdomain_name": "Deep Learning",
        "description": "Neural networks and transformers",
        "complexity_level": "Advanced",
    },
    {
        "domain_name": "Cybersecurity",
        "subdomain_name": "Application Security",
        "description": "Web and API security",
        "complexity_level": "Advanced",
    },
    {
        "domain_name": "Cloud/DevOps",
        "subdomain_name": "Kubernetes Engineering",
        "description": "Container orchestration",
        "complexity_level": "Advanced",
    },
]

# =========================================================
# SPECIALIZATIONS DATA
# =========================================================

SPECIALIZATIONS = [
    {
        "subdomain_name": "Distributed Systems",
        "specialization_name": "High Performance Backend",
        "description": "Low latency backend systems",
    },
    {
        "subdomain_name": "Deep Learning",
        "specialization_name": "LLM Engineering",
        "description": "Large language model systems",
    },
    {
        "subdomain_name": "Application Security",
        "specialization_name": "Penetration Testing",
        "description": "Offensive security testing",
    },
    {
        "subdomain_name": "Kubernetes Engineering",
        "specialization_name": "Platform Engineering",
        "description": "Cloud platform automation",
    },
]

# =========================================================
# TECHNOLOGIES DATA
# =========================================================

TECHNOLOGIES = [
    {
        "technologies_name": "Python",
        "technology_type": "Programming Language",
    },
    {
        "technologies_name": "C++",
        "technology_type": "Programming Language",
    },
    {
        "technologies_name": "FastAPI",
        "technology_type": "Backend Framework",
    },
    {
        "technologies_name": "PostgreSQL",
        "technology_type": "Database",
    },
    {
        "technologies_name": "Docker",
        "technology_type": "Infrastructure",
    },
    {
        "technologies_name": "Kubernetes",
        "technology_type": "Infrastructure",
    },
    {
        "technologies_name": "Redis",
        "technology_type": "Database",
    },
    {
        "technologies_name": "PyTorch",
        "technology_type": "AI Framework",
    },
]

# =========================================================
# STATIC QUESTIONS
# =========================================================

STATIC_QUESTIONS = [
    {
        "question_text": "When solving difficult problems, I can stay focused for long periods.",
        "question_format": "likert",
        "trait_name": "Deep Focus",
    },
    {
        "question_text": "I enjoy understanding how systems work internally.",
        "question_format": "likert",
        "trait_name": "Systems Thinking",
    },
    {
        "question_text": "I enjoy mathematical and analytical problem solving.",
        "question_format": "likert",
        "trait_name": "Analytical Thinking",
    },
    {
        "question_text": "I continue debugging even after many failures.",
        "question_format": "likert",
        "trait_name": "Persistence",
    },
    {
        "question_text": "I enjoy experimenting with new technologies.",
        "question_format": "likert",
        "trait_name": "Curiosity",
    },
]

LIKERT_OPTIONS = [
    ("Strongly Disagree", 1),
    ("Disagree", 2),
    ("Neutral", 3),
    ("Agree", 4),
    ("Strongly Agree", 5),
]

# =========================================================
# TRAIT DOMAIN MAPPINGS
# =========================================================

TRAIT_DOMAIN_MAPPINGS = [
    ("Deep Focus", "Backend Engineering", 0.95),
    ("Persistence", "Cybersecurity", 0.92),
    ("Systems Thinking", "Cloud/DevOps", 0.94),
    ("Analytical Thinking", "AI/ML Engineering", 0.96),
    ("Curiosity", "AI/ML Engineering", 0.90),
    ("Creativity", "AI/ML Engineering", 0.84),
]

# =========================================================
# INSERT TRAITS
# =========================================================

print("\nSeeding traits...")

for item in TRAITS:

    exists = (
        db.query(Trait)
        .filter(Trait.trait_name == item["trait_name"])
        .first()
    )

    if not exists:
        db.add(Trait(**item))

db.commit()

# =========================================================
# INSERT DOMAINS
# =========================================================

print("Seeding domains...")

for item in DOMAINS:

    exists = (
        db.query(Domain)
        .filter(Domain.domain_name == item["domain_name"])
        .first()
    )

    if not exists:
        db.add(Domain(**item))

db.commit()

# =========================================================
# INSERT SUBDOMAINS
# =========================================================

print("Seeding subdomains...")

for item in SUBDOMAINS:

    domain = (
        db.query(Domain)
        .filter(Domain.domain_name == item["domain_name"])
        .first()
    )

    if domain:

        exists = (
            db.query(Subdomain)
            .filter(
                Subdomain.subdomain_name == item["subdomain_name"]
            )
            .first()
        )

        if not exists:

            db.add(
                Subdomain(
                    domain_id=domain.id,
                    subdomain_name=item["subdomain_name"],
                    description=item["description"],
                    complexity_level=item["complexity_level"],
                )
            )

db.commit()

# =========================================================
# INSERT SPECIALIZATIONS
# =========================================================

print("Seeding specializations...")

for item in SPECIALIZATIONS:

    subdomain = (
        db.query(Subdomain)
        .filter(
            Subdomain.subdomain_name == item["subdomain_name"]
        )
        .first()
    )

    if subdomain:

        exists = (
            db.query(Specialization)
            .filter(
                Specialization.specialization_name
                == item["specialization_name"]
            )
            .first()
        )

        if not exists:

            db.add(
                Specialization(
                    subdomain_id=subdomain.id,
                    specialization_name=item["specialization_name"],
                    description=item["description"],
                )
            )

db.commit()

# =========================================================
# INSERT TECHNOLOGIES
# =========================================================

print("Seeding technologies...")

for item in TECHNOLOGIES:

    exists = (
        db.query(Technology)
        .filter(
            Technology.technologies_name
            == item["technologies_name"]
        )
        .first()
    )

    if not exists:
        db.add(Technology(**item))

db.commit()

# =========================================================
# INSERT TECHNOLOGY STACKS
# =========================================================

print("Seeding technology stacks...")

specializations = db.query(Specialization).all()

for spec in specializations:

    exists = (
        db.query(TechnologyStack)
        .filter(
            TechnologyStack.specialization_id == spec.id
        )
        .first()
    )

    if not exists:

        db.add(
            TechnologyStack(
                specialization_id=spec.id,
                languages="Python,C++,JavaScript",
                frameworks="FastAPI,Django,React",
                databases="PostgreSQL,Redis",
                infrastructure_tools="Docker,Kubernetes",
                ai_tools="PyTorch,HuggingFace",
            )
        )

db.commit()

# =========================================================
# INSERT STATIC QUESTIONS
# =========================================================

print("Seeding static questions...")

for item in STATIC_QUESTIONS:

    trait = (
        db.query(Trait)
        .filter(Trait.trait_name == item["trait_name"])
        .first()
    )

    if trait:

        exists = (
            db.query(StaticQuestion)
            .filter(
                StaticQuestion.question_text
                == item["question_text"]
            )
            .first()
        )

        if not exists:

            question = StaticQuestion(
                question_text=item["question_text"],
                question_format=item["question_format"],
                trait_id=trait.id,
                difficulty_level="Medium",
                cognitive_load_score=0.5,
                fatigue_score=0.2,
                estimated_time_seconds=30,
                is_required=True,
                is_active=True,
            )

            db.add(question)
            db.commit()
            db.refresh(question)

            for order, (text, score) in enumerate(
                LIKERT_OPTIONS,
                start=1,
            ):

                db.add(
                    StaticQuestionOption(
                        question_id=question.id,
                        option_text=text,
                        option_score=score,
                        trait_signal_strength=1.0,
                        domain_signal_strength=1.0,
                        option_order=order,
                    )
                )

db.commit()

# =========================================================
# INSERT TRAIT DOMAIN MAPPINGS
# =========================================================

print("Seeding trait-domain mappings...")

for trait_name, domain_name, influence in TRAIT_DOMAIN_MAPPINGS:

    trait = (
        db.query(Trait)
        .filter(Trait.trait_name == trait_name)
        .first()
    )

    domain = (
        db.query(Domain)
        .filter(Domain.domain_name == domain_name)
        .first()
    )

    if trait and domain:

        exists = (
            db.query(TraitDomainMapping)
            .filter(
                TraitDomainMapping.trait_id == trait.id,
                TraitDomainMapping.domain_id == domain.id,
            )
            .first()
        )

        if not exists:
where 
            db.add(
                TraitDomainMapping(
                    trait_id=trait.id,
                    domain_id=domain.id,
                    influence_score=influence,
                    positive_or_negative="positive",
                )
            )

db.commit()

# =========================================================
# FINISHED
# =========================================================

print("\n===================================")
print("DATABASE SEEDED SUCCESSFULLY")
print("===================================")

db.close()