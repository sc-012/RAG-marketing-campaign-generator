# Multi-Agent System for AI RAG Marketing Campaign Generator
# Using CrewAI for specialized agent collaboration

from .document_analyzer import DocumentAnalyzerAgent
from .campaign_strategist import CampaignStrategistAgent
from .content_creator import ContentCreatorAgent
from .social_media_specialist import SocialMediaSpecialistAgent
from .email_marketing_expert import EmailMarketingExpertAgent
from .ab_testing_analyst import ABTestingAnalystAgent
from .visual_designer import VisualDesignerAgent
from .performance_optimizer import PerformanceOptimizerAgent

__all__ = [
    'DocumentAnalyzerAgent',
    'CampaignStrategistAgent', 
    'ContentCreatorAgent',
    'SocialMediaSpecialistAgent',
    'EmailMarketingExpertAgent',
    'ABTestingAnalystAgent',
    'VisualDesignerAgent',
    'PerformanceOptimizerAgent'
]
