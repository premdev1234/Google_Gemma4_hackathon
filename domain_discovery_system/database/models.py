# domain_discovery_system/database/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from domain_discovery_system.database.connection import Base

# =========================================================
# BASE MODEL
# =========================================================


class BaseModel(Base):
    """
    Abstract base class to provide 'id' and 'created_at' to all tables.
    This fixes the 'UndefinedColumn' error by ensuring the primary key
    exists before it is referenced as a foreign key.
    """

    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# =========================================================
# USERS (CORRECTED)
# =========================================================


class User(BaseModel):  # Changed from Base to BaseModel
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer)
    educational_level = Column(String(100))
    country = Column(String(100))
    career_stage = Column(String(100))


# =========================================================
# TRAITS & DOMAINS
# =========================================================


class Trait(BaseModel):
    __tablename__ = "traits"
    trait_name = Column(String(255), unique=True, nullable=False)
    trait_category = Column(String(100), nullable=False)
    description = Column(Text)
    importance_score = Column(Float, default=0.0)


class Domain(BaseModel):
    __tablename__ = "domains"
    domain_name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    market_demand_score = Column(Float, default=0.0)
    future_growth_score = Column(Float, default=0.0)


class Subdomain(BaseModel):
    __tablename__ = "subdomains"
    domain_id = Column(ForeignKey("domains.id"))
    subdomain_name = Column(String(255), nullable=False)
    description = Column(Text)
    complexity_level = Column(String(50))


class Specialization(BaseModel):
    __tablename__ = "specializations"
    subdomain_id = Column(ForeignKey("subdomains.id"))
    specialization_name = Column(String(255), nullable=False)
    description = Column(Text)


# =========================================================
# TECHNOLOGY STACK
# =========================================================


class TechnologyStack(BaseModel):

    __tablename__ = "technology_stacks"

    specialization_id = Column(ForeignKey("specializations.id"))

    languages = Column(Text)

    frameworks = Column(Text)

    databases = Column(Text)

    infrastructure_tools = Column(Text)

    ai_tools = Column(Text)


# =========================================================
# STATIC ASSESSMENT QUESTIONS
# =========================================================


class StaticQuestion(BaseModel):
    __tablename__ = "static_questions"
    question_text = Column(Text, nullable=False)
    question_format = Column(
        String(50), nullable=False
    )  # likert, mcq, msq, scenario, ranking
    trait_id = Column(ForeignKey("traits.id"))
    difficulty_level = Column(String(50))
    cognitive_load_score = Column(Float, default=0.0)
    fatigue_score = Column(Float, default=0.0)
    estimated_time_seconds = Column(Integer, default=30)
    is_required = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)


class StaticQuestionOption(BaseModel):
    __tablename__ = "static_question_options"
    question_id = Column(ForeignKey("static_questions.id"))
    option_text = Column(Text)
    option_score = Column(Float, default=0.0)
    trait_signal_strength = Column(Float, default=0.0)
    domain_signal_strength = Column(Float, default=0.0)
    option_order = Column(Integer, default=1)


# =========================================================
# QUESTION TAGS
# =========================================================


class QuestionTag(BaseModel):

    __tablename__ = "question_tags"

    question_id = Column(ForeignKey("static_questions.id"))

    tag_name = Column(String(100))


# =========================================================
# DYNAMIC ENGINE & ADAPTIVE LOGIC
# =========================================================


class ContradictionPattern(BaseModel):
    __tablename__ = "contradiction_patterns"
    pattern_name = Column(String(255))
    condition_logic = Column(Text)
    severity_score = Column(Float)
    followup_template_id = Column(Integer)


class DynamicQuestionTemplate(BaseModel):
    __tablename__ = "dynamic_question_templates"
    template_name = Column(String(255))
    trigger_trait_id = Column(ForeignKey("traits.id"))
    trigger_condition = Column(String(100))
    contradiction_pattern_id = Column(ForeignKey("contradiction_patterns.id"))
    prompt_template = Column(Text)
    question_goal = Column(Text)
    question_format = Column(String(50))
    target_domain_id = Column(ForeignKey("domains.id"))
    priority_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)


# =========================================================
# DYNAMIC QUESTION RULES
# =========================================================


class DynamicQuestionRule(BaseModel):

    __tablename__ = "dynamic_question_rules"

    source_trait_id = Column(ForeignKey("traits.id"))

    condition_type = Column(String(100))

    threshold_min = Column(Float)

    threshold_max = Column(Float)

    next_template_id = Column(ForeignKey("dynamic_question_templates.id"))

    priority_score = Column(Float)


# =========================================================
# ASSESSMENT SESSIONS
# =========================================================


class AssessmentSession(BaseModel):
    __tablename__ = "assessment_sessions"
    user_id = Column(ForeignKey("users.id"))
    session_status = Column(String(100))
    total_questions_answered = Column(Integer, default=0)
    fatigue_level = Column(Float, default=0.0)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))


# =========================================================
# DYNAMIC QUESTION SESSIONS
# =========================================================


class DynamicQuestionSession(BaseModel):

    __tablename__ = "dynamic_question_sessions"

    user_id = Column(ForeignKey("users.id"))

    assessment_session_id = Column(ForeignKey("assessment_sessions.id"))

    template_id = Column(ForeignKey("dynamic_question_templates.id"))

    generated_question = Column(Text)

    generated_context = Column(Text)

    question_format = Column(String(50))

    trigger_reason = Column(Text)

    generated_by = Column(String(100))

    gemma_prompt = Column(Text)

    gemma_response = Column(Text)

    response_time_seconds = Column(Float)

    was_answered = Column(Boolean, default=False)


# =========================================================
# DYNAMIC QUESTION OPTIONS
# =========================================================


class DynamicQuestionOption(BaseModel):

    __tablename__ = "dynamic_question_options"

    dynamic_question_session_id = Column(ForeignKey("dynamic_question_sessions.id"))

    option_text = Column(Text)

    option_score = Column(Float)

    trait_signal = Column(Text)

    domain_signal = Column(Text)

    option_order = Column(Integer)

    is_generated = Column(Boolean, default=True)


# =========================================================
# SESSION & BEHAVIORAL TRACKING
# =========================================================
class UserResponse(BaseModel):
    __tablename__ = "user_responses"
    user_id = Column(ForeignKey("users.id"))
    assessment_session_id = Column(ForeignKey("assessment_sessions.id"))
    question_source = Column(String(50))  # 'static' or 'dynamic'
    question_id = Column(Integer)
    selected_option_ids = Column(JSON)
    open_text_response = Column(Text)
    response_duration_seconds = Column(Float)
    answer_change_count = Column(Integer, default=0)


class BehavioralSignal(BaseModel):
    __tablename__ = "behavioral_signals"
    user_id = Column(ForeignKey("users.id"))
    assessment_session_id = Column(ForeignKey("assessment_sessions.id"))
    hesitation_count = Column(Integer, default=0)
    answer_change_count = Column(Integer, default=0)
    tab_switch_count = Column(Integer, default=0)
    focus_loss_score = Column(Float, default=0.0)
    rage_exit_detected = Column(Boolean, default=False)


# =========================================================
# PROFILING & PREDICTIONS
# =========================================================


class UserTraitScore(BaseModel):
    __tablename__ = "user_trait_scores"
    user_id = Column(ForeignKey("users.id"))
    trait_id = Column(ForeignKey("traits.id"))
    raw_score = Column(Float)
    normalized_score = Column(Float)
    confidence_score = Column(Float)
    last_updated = Column(DateTime(timezone=True))


class UserDomainPrediction(BaseModel):
    __tablename__ = "user_domain_predictions"
    user_id = Column(ForeignKey("users.id"))
    domain_id = Column(ForeignKey("domains.id"))
    subdomain_id = Column(ForeignKey("subdomains.id"))
    specialization_id = Column(ForeignKey("specializations.id"))
    prediction_score = Column(Float)
    confidence_score = Column(Float)
    reasoning_summary = Column(Text)


class CognitiveProfile(BaseModel):
    __tablename__ = "cognitive_profiles"
    user_id = Column(ForeignKey("users.id"))
    logic_score = Column(Float)
    creativity_score = Column(Float)
    persistence_score = Column(Float)
    focus_score = Column(Float)
    stress_tolerance_score = Column(Float)
    systems_thinking_score = Column(Float)
    overall_confidence = Column(Float)


# =========================================================
# GEMMA REASONING LOGS
# =========================================================


class GemmaReasoningLog(BaseModel):

    __tablename__ = "gemma_reasoning_logs"

    user_id = Column(ForeignKey("users.id"))

    reasoning_type = Column(String(100))

    input_summary = Column(Text)

    prompt_used = Column(Text)

    output_summary = Column(Text)

    confidence_score = Column(Float)


# =========================================================
# MARKET TRENDS
# =========================================================


class MarketTrend(BaseModel):

    __tablename__ = "market_trends"

    domain_id = Column(ForeignKey("domains.id"))

    subdomain_id = Column(ForeignKey("subdomains.id"))

    demand_score = Column(Float)

    salary_average = Column(Float)

    competition_level = Column(Float)

    growth_rate = Column(Float)

    data_source = Column(String(255))

    collected_at = Column(DateTime(timezone=True))


# =========================================================
# TRAIT DOMAIN MAPPING
# =========================================================


class TraitDomainMapping(BaseModel):

    __tablename__ = "trait_domain_mappings"

    trait_id = Column(ForeignKey("traits.id"))

    domain_id = Column(ForeignKey("domains.id"))

    influence_score = Column(Float)

    positive_or_negative = Column(String(50))


# =========================================================
# COGNITIVE STATE TIMELINE
# =========================================================


class CognitiveStateTimeline(BaseModel):

    __tablename__ = "cognitive_state_timelines"

    user_id = Column(ForeignKey("users.id"))

    session_id = Column(ForeignKey("assessment_sessions.id"))

    fatigue_score = Column(Float)

    emotional_state = Column(String(100))

    confidence_level = Column(Float)

    focus_level = Column(Float)

    timestamp = Column(DateTime(timezone=True))


# =========================================================
# TECHNICAL SIMULATIONS
# =========================================================


class TechnicalSimulation(BaseModel):

    __tablename__ = "technical_simulations"

    domain_id = Column(ForeignKey("domains.id"))

    subdomain_id = Column(ForeignKey("subdomains.id"))

    simulation_type = Column(String(100))

    prompt = Column(Text)

    difficulty = Column(String(50))

    expected_skills = Column(Text)


# =========================================================
# SIMULATION RESPONSES
# =========================================================


class SimulationResponse(BaseModel):

    __tablename__ = "simulation_responses"

    user_id = Column(ForeignKey("users.id"))

    simulation_id = Column(ForeignKey("technical_simulations.id"))

    reasoning_text = Column(Text)

    completion_time = Column(Float)

    correctness_score = Column(Float)

    persistence_score = Column(Float)

    gemma_analysis = Column(Text)


# =========================================================
# USER DOMAIN EVOLUTION
# =========================================================


class UserDomainEvolution(BaseModel):

    __tablename__ = "user_domain_evolutions"

    user_id = Column(ForeignKey("users.id"))

    previous_domain = Column(String(255))

    new_domain = Column(String(255))

    reason_for_change = Column(Text)

    confidence_delta = Column(Float)

    changed_at = Column(DateTime(timezone=True))


# =========================================================
# EMBEDDINGS MEMORY
# =========================================================


class EmbeddingsMemory(BaseModel):

    __tablename__ = "embeddings_memory"

    user_id = Column(ForeignKey("users.id"))

    memory_type = Column(String(100))

    embedding_vector = Column(Text)

    source_text = Column(Text)


# =========================================================
# RECOMMENDATION EXPLANATIONS
# =========================================================


class RecommendationExplanation(BaseModel):

    __tablename__ = "recommendation_explanations"

    prediction_id = Column(ForeignKey("user_domain_predictions.id"))

    top_traits = Column(Text)

    strongest_behaviors = Column(Text)

    strongest_signals = Column(Text)

    weakness_summary = Column(Text)

    generated_explanation = Column(Text)


# =========================================================
# TECHNOLOGIES
# =========================================================


class Technology(BaseModel):

    __tablename__ = "technologies"

    technologies_name = Column(String(255))

    technology_type = Column(String(100))
