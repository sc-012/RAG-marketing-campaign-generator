"""
Document Analyzer Agent - Specialized in analyzing uploaded documents
"""
from .base_agent import BaseMarketingAgent
from crewai import Agent
from typing import Dict, Any, List
import re

class DocumentAnalyzerAgent(BaseMarketingAgent):
    """Agent specialized in analyzing marketing documents and extracting key insights"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Document Analyzer",
            role="Senior Marketing Document Analyst",
            goal="Analyze uploaded marketing documents and extract key brand elements, messaging, and strategic insights",
            backstory="""You are an expert marketing analyst with 15+ years of experience in 
            brand analysis, market research, and strategic planning. You excel at quickly 
            identifying key brand elements, target audiences, messaging themes, and strategic 
            opportunities from various types of marketing documents including brand guidelines, 
            case studies, product specifications, and market research reports.""",
            llm=llm
        )
    
    def analyze_document(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Analyze document and extract key marketing insights"""
        
        analysis_prompt = f"""
        Analyze this {document_type} document and extract the following key marketing elements:
        
        Document Content:
        {document_content}
        
        Please provide a structured analysis including:
        1. Brand Identity Elements (colors, fonts, tone, voice)
        2. Target Audience Insights (demographics, psychographics, pain points)
        3. Key Messages and Value Propositions
        4. Product/Service Features and Benefits
        5. Competitive Positioning
        6. Marketing Channels Mentioned
        7. Success Metrics and KPIs
        8. Strategic Recommendations
        
        Format your response as a structured JSON object.
        """
        
        # This would be processed by the LLM
        return {
            "brand_identity": self._extract_brand_identity(document_content),
            "target_audience": self._extract_target_audience(document_content),
            "key_messages": self._extract_key_messages(document_content),
            "features_benefits": self._extract_features_benefits(document_content),
            "competitive_positioning": self._extract_competitive_positioning(document_content),
            "marketing_channels": self._extract_marketing_channels(document_content),
            "success_metrics": self._extract_success_metrics(document_content),
            "strategic_recommendations": self._extract_strategic_recommendations(document_content)
        }
    
    def _extract_brand_identity(self, content: str) -> Dict[str, Any]:
        """Extract brand identity elements from document"""
        # Pattern matching for brand elements
        colors = re.findall(r'#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{3}', content)
        fonts = re.findall(r'font[:\s]+([A-Za-z\s]+)', content, re.IGNORECASE)
        
        return {
            "colors": list(set(colors)),
            "fonts": list(set(fonts)),
            "tone": self._analyze_tone(content),
            "voice": self._analyze_voice(content)
        }
    
    def _extract_target_audience(self, content: str) -> Dict[str, Any]:
        """Extract target audience information"""
        # Look for demographic and psychographic indicators
        age_patterns = re.findall(r'(\d+-\d+|\d+\+)\s*years?', content, re.IGNORECASE)
        income_patterns = re.findall(r'\$[\d,]+', content)
        
        return {
            "age_groups": list(set(age_patterns)),
            "income_levels": list(set(income_patterns)),
            "demographics": self._extract_demographics(content),
            "psychographics": self._extract_psychographics(content)
        }
    
    def _extract_key_messages(self, content: str) -> List[str]:
        """Extract key marketing messages"""
        # Look for value propositions and key messages
        messages = re.findall(r'(?:value proposition|key message|tagline)[:\s]+([^.\n]+)', content, re.IGNORECASE)
        return messages
    
    def _extract_features_benefits(self, content: str) -> Dict[str, List[str]]:
        """Extract product features and benefits"""
        features = re.findall(r'feature[:\s]+([^.\n]+)', content, re.IGNORECASE)
        benefits = re.findall(r'benefit[:\s]+([^.\n]+)', content, re.IGNORECASE)
        
        return {
            "features": features,
            "benefits": benefits
        }
    
    def _extract_competitive_positioning(self, content: str) -> str:
        """Extract competitive positioning information"""
        # Look for competitive analysis or positioning statements
        positioning = re.findall(r'(?:positioning|competitive advantage)[:\s]+([^.\n]+)', content, re.IGNORECASE)
        return positioning[0] if positioning else "Not specified"
    
    def _extract_marketing_channels(self, content: str) -> List[str]:
        """Extract mentioned marketing channels"""
        channels = re.findall(r'(?:social media|email|digital|traditional|print|radio|tv|online|offline)', content, re.IGNORECASE)
        return list(set(channels))
    
    def _extract_success_metrics(self, content: str) -> List[str]:
        """Extract success metrics and KPIs"""
        metrics = re.findall(r'(?:KPI|metric|ROI|conversion|engagement|reach|impression)', content, re.IGNORECASE)
        return list(set(metrics))
    
    def _extract_strategic_recommendations(self, content: str) -> List[str]:
        """Extract strategic recommendations"""
        recommendations = re.findall(r'(?:recommend|suggest|strategy|approach)[:\s]+([^.\n]+)', content, re.IGNORECASE)
        return recommendations
    
    def _analyze_tone(self, content: str) -> str:
        """Analyze the tone of the content"""
        # Simple tone analysis based on word patterns
        professional_words = ['professional', 'expert', 'quality', 'premium', 'sophisticated']
        casual_words = ['fun', 'easy', 'simple', 'friendly', 'approachable']
        
        professional_count = sum(1 for word in professional_words if word in content.lower())
        casual_count = sum(1 for word in casual_words if word in content.lower())
        
        if professional_count > casual_count:
            return "Professional"
        elif casual_count > professional_count:
            return "Casual"
        else:
            return "Balanced"
    
    def _analyze_voice(self, content: str) -> str:
        """Analyze the voice of the content"""
        # Simple voice analysis
        if 'we' in content.lower():
            return "First Person"
        elif 'you' in content.lower():
            return "Second Person"
        else:
            return "Third Person"
    
    def _extract_demographics(self, content: str) -> Dict[str, Any]:
        """Extract demographic information"""
        return {
            "age": re.findall(r'(\d+-\d+|\d+\+)\s*years?', content, re.IGNORECASE),
            "gender": re.findall(r'(male|female|men|women)', content, re.IGNORECASE),
            "location": re.findall(r'(urban|rural|suburban|city|country)', content, re.IGNORECASE)
        }
    
    def _extract_psychographics(self, content: str) -> Dict[str, Any]:
        """Extract psychographic information"""
        return {
            "interests": re.findall(r'(?:interested in|passionate about|enjoys)[:\s]+([^.\n]+)', content, re.IGNORECASE),
            "values": re.findall(r'(?:values|believes in|principles)[:\s]+([^.\n]+)', content, re.IGNORECASE),
            "lifestyle": re.findall(r'(?:lifestyle|way of life)[:\s]+([^.\n]+)', content, re.IGNORECASE)
        }
