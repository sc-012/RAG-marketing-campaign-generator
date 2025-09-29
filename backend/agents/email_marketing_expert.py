"""
Email Marketing Expert Agent - Specialized in email marketing campaigns
"""
from .base_agent import BaseMarketingAgent
from typing import Dict, Any, List

class EmailMarketingExpertAgent(BaseMarketingAgent):
    """Agent specialized in email marketing campaigns and automation"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Email Marketing Expert",
            role="Senior Email Marketing Specialist",
            goal="Create high-converting email marketing campaigns that nurture leads and drive customer engagement",
            backstory="""You are an email marketing expert with 12+ years of experience in creating 
            successful email campaigns across various industries. You excel at email automation, 
            segmentation, personalization, and A/B testing. You understand email deliverability, 
            compliance, and how to create compelling subject lines and content that drive action."""
        )
    
    async def create_email_campaign(self, document_analysis: Dict[str, Any], 
                                  campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive email marketing campaign"""
        
        return {
            "campaign_strategy": self._develop_email_strategy(campaign_strategy),
            "email_sequences": self._create_email_sequences(document_analysis, campaign_strategy),
            "subject_lines": self._create_subject_lines(campaign_strategy),
            "email_templates": self._create_email_templates(document_analysis),
            "segmentation_strategy": self._create_segmentation_strategy(),
            "automation_workflows": self._create_automation_workflows(),
            "deliverability_guidelines": self._create_deliverability_guidelines(),
            "compliance_checklist": self._create_compliance_checklist()
        }
    
    def _develop_email_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Develop email marketing strategy"""
        return {
            "campaign_objectives": [
                "Lead nurturing",
                "Customer retention",
                "Product promotion",
                "Brand awareness",
                "Event promotion"
            ],
            "email_types": {
                "welcome_series": "3-5 emails over 2 weeks",
                "nurture_sequences": "5-7 emails over 4-6 weeks",
                "promotional_campaigns": "1-3 emails per campaign",
                "newsletters": "Weekly or bi-weekly",
                "re_engagement": "3-4 emails over 2 weeks"
            },
            "sending_frequency": {
                "new_subscribers": "Daily for first week, then weekly",
                "engaged_subscribers": "2-3 times per week",
                "inactive_subscribers": "Monthly re-engagement campaigns"
            },
            "content_strategy": {
                "educational_content": "40%",
                "promotional_content": "30%",
                "company_updates": "20%",
                "user_generated_content": "10%"
            }
        }
    
    def _create_email_sequences(self, document_analysis: Dict[str, Any], 
                              campaign_strategy: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Create email sequences for different campaign types"""
        
        return {
            "welcome_series": [
                {
                    "email_number": 1,
                    "subject": "Welcome to {brand_name}! Here's what to expect",
                    "timing": "Immediately after signup",
                    "purpose": "Welcome and set expectations",
                    "content_outline": [
                        "Welcome message and thank you",
                        "What they can expect from us",
                        "How to get the most value",
                        "Next steps and call-to-action"
                    ]
                },
                {
                    "email_number": 2,
                    "subject": "Get started with {brand_name} - Your quick start guide",
                    "timing": "Day 2",
                    "purpose": "Provide value and guide onboarding",
                    "content_outline": [
                        "Quick start guide or tutorial",
                        "Key features and benefits",
                        "Success tips and best practices",
                        "Support resources"
                    ]
                },
                {
                    "email_number": 3,
                    "subject": "Success story: How {customer_name} achieved {result}",
                    "timing": "Day 5",
                    "purpose": "Social proof and motivation",
                    "content_outline": [
                        "Customer success story",
                        "Key results and benefits",
                        "How they achieved success",
                        "Encourage engagement"
                    ]
                }
            ],
            "nurture_sequence": [
                {
                    "email_number": 1,
                    "subject": "The #1 mistake most {industry} professionals make",
                    "timing": "Day 1",
                    "purpose": "Educational content with problem identification",
                    "content_outline": [
                        "Common industry mistake",
                        "Why it's problematic",
                        "How to avoid it",
                        "Solution or best practice"
                    ]
                },
                {
                    "email_number": 2,
                    "subject": "5 proven strategies to {achieve_goal}",
                    "timing": "Day 4",
                    "purpose": "Provide actionable value",
                    "content_outline": [
                        "Strategy 1 with explanation",
                        "Strategy 2 with example",
                        "Strategy 3 with case study",
                        "Strategy 4 with tips",
                        "Strategy 5 with next steps"
                    ]
                },
                {
                    "email_number": 3,
                    "subject": "Behind the scenes: How we {process_description}",
                    "timing": "Day 7",
                    "purpose": "Build trust and transparency",
                    "content_outline": [
                        "Behind-the-scenes look",
                        "Our process and methodology",
                        "Why we do it this way",
                        "Invitation to learn more"
                    ]
                }
            ],
            "promotional_campaign": [
                {
                    "email_number": 1,
                    "subject": "🎉 {offer_description} - Limited time only!",
                    "timing": "Campaign launch",
                    "purpose": "Announce promotion and create urgency",
                    "content_outline": [
                        "Promotion announcement",
                        "Offer details and value",
                        "Urgency and scarcity elements",
                        "Clear call-to-action"
                    ]
                },
                {
                    "email_number": 2,
                    "subject": "Last chance: {offer_description} ends {deadline}",
                    "timing": "24 hours before deadline",
                    "purpose": "Create urgency and drive action",
                    "content_outline": [
                        "Final reminder",
                        "Reinforce value proposition",
                        "Countdown timer",
                        "Strong call-to-action"
                    ]
                }
            ]
        }
    
    def _create_subject_lines(self, campaign_strategy: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create compelling subject lines for different email types"""
        
        return {
            "welcome_emails": [
                "Welcome to {brand_name}! Let's get started",
                "Thanks for joining us! Here's what's next",
                "You're in! Welcome to the {brand_name} family",
                "Welcome aboard! Your journey starts here",
                "Hello! We're excited to have you"
            ],
            "educational_emails": [
                "The secret to {achieving_goal} (most people miss this)",
                "5 ways to {solve_problem} that actually work",
                "Why {common_belief} is holding you back",
                "The {number} mistake everyone makes with {topic}",
                "How to {achieve_result} in {timeframe}"
            ],
            "promotional_emails": [
                "🎉 {offer_description} - Don't miss out!",
                "Limited time: {discount}% off {product}",
                "Last chance: {offer} ends {deadline}",
                "Exclusive offer just for you: {deal}",
                "Flash sale: {product} at {price}"
            ],
            "newsletter_emails": [
                "This week in {industry}: {key_topic}",
                "Your weekly {brand_name} update",
                "What's new this week: {highlight}",
                "Industry insights you can't miss",
                "Weekly roundup: {number} things to know"
            ],
            "re_engagement_emails": [
                "We miss you! Here's what you've been missing",
                "Is this email address still active?",
                "We have something special for you",
                "Don't let this opportunity pass you by",
                "Your account is waiting for you"
            ]
        }
    
    def _create_email_templates(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create email templates for different purposes"""
        brand_identity = document_analysis.get("brand_identity", {})
        
        return {
            "welcome_template": {
                "header": "Welcome to {brand_name}!",
                "body_structure": [
                    "Personalized greeting",
                    "Welcome message and excitement",
                    "What to expect from us",
                    "First steps or next actions",
                    "Support and contact information"
                ],
                "cta": "Get Started",
                "footer": "Thank you for joining us!"
            },
            "educational_template": {
                "header": "Educational Content Title",
                "body_structure": [
                    "Hook or attention-grabbing opening",
                    "Problem identification or question",
                    "Educational content with examples",
                    "Key takeaways or action items",
                    "Related resources or next steps"
                ],
                "cta": "Learn More",
                "footer": "Keep learning with us!"
            },
            "promotional_template": {
                "header": "Special Offer Inside!",
                "body_structure": [
                    "Attention-grabbing offer announcement",
                    "Value proposition and benefits",
                    "Offer details and terms",
                    "Urgency and scarcity elements",
                    "Clear call-to-action"
                ],
                "cta": "Claim Offer",
                "footer": "Limited time offer - act now!"
            },
            "newsletter_template": {
                "header": "Weekly Update",
                "body_structure": [
                    "Personal greeting",
                    "This week's highlights",
                    "Featured content or articles",
                    "Company updates or news",
                    "Upcoming events or opportunities"
                ],
                "cta": "Read More",
                "footer": "Thanks for staying connected!"
            }
        }
    
    def _create_segmentation_strategy(self) -> Dict[str, Any]:
        """Create email segmentation strategy"""
        return {
            "segmentation_criteria": {
                "demographics": ["Age", "Gender", "Location", "Job title"],
                "behavioral": ["Email engagement", "Website activity", "Purchase history"],
                "psychographic": ["Interests", "Values", "Lifestyle"],
                "firmographic": ["Company size", "Industry", "Revenue"]
            },
            "segment_examples": [
                {
                    "segment_name": "High Engagers",
                    "criteria": "Opens 80%+ of emails, clicks regularly",
                    "content_strategy": "Advanced content, exclusive offers",
                    "frequency": "2-3 times per week"
                },
                {
                    "segment_name": "New Subscribers",
                    "criteria": "Subscribed within last 30 days",
                    "content_strategy": "Welcome series, educational content",
                    "frequency": "Daily for first week, then weekly"
                },
                {
                    "segment_name": "Inactive Users",
                    "criteria": "No opens in last 90 days",
                    "content_strategy": "Re-engagement campaigns, special offers",
                    "frequency": "Monthly"
                }
            ],
            "personalization_tactics": [
                "Dynamic content based on preferences",
                "Personalized subject lines",
                "Product recommendations",
                "Location-based offers",
                "Behavior-triggered content"
            ]
        }
    
    def _create_automation_workflows(self) -> Dict[str, Any]:
        """Create email automation workflows"""
        return {
            "welcome_workflow": {
                "trigger": "New subscriber",
                "emails": 3,
                "timing": "Immediate, Day 2, Day 5",
                "purpose": "Onboard new subscribers"
            },
            "abandoned_cart_workflow": {
                "trigger": "Cart abandonment",
                "emails": 3,
                "timing": "1 hour, 24 hours, 72 hours",
                "purpose": "Recover abandoned purchases"
            },
            "post_purchase_workflow": {
                "trigger": "Purchase completion",
                "emails": 2,
                "timing": "Immediate, Day 7",
                "purpose": "Thank customer and encourage repeat purchase"
            },
            "re_engagement_workflow": {
                "trigger": "No engagement for 30 days",
                "emails": 3,
                "timing": "Day 30, Day 37, Day 44",
                "purpose": "Re-engage inactive subscribers"
            },
            "birthday_workflow": {
                "trigger": "Birthday",
                "emails": 1,
                "timing": "On birthday",
                "purpose": "Send birthday wishes and special offer"
            }
        }
    
    def _create_deliverability_guidelines(self) -> Dict[str, Any]:
        """Create email deliverability guidelines"""
        return {
            "technical_requirements": [
                "SPF record configured",
                "DKIM signature implemented",
                "DMARC policy set",
                "Clean IP reputation",
                "Proper authentication"
            ],
            "content_guidelines": [
                "Avoid spam trigger words",
                "Maintain text-to-image ratio (80:20)",
                "Use proper HTML structure",
                "Include unsubscribe link",
                "Test across email clients"
            ],
            "sending_practices": [
                "Warm up new IP addresses",
                "Maintain consistent sending volume",
                "Monitor bounce rates (<2%)",
                "Track spam complaints (<0.1%)",
                "Clean email lists regularly"
            ],
            "reputation_management": [
                "Monitor sender reputation",
                "Respond to feedback loops",
                "Handle complaints promptly",
                "Maintain engagement rates",
                "Use double opt-in"
            ]
        }
    
    def _create_compliance_checklist(self) -> Dict[str, Any]:
        """Create email compliance checklist"""
        return {
            "gdpr_compliance": [
                "Clear consent collection",
                "Easy unsubscribe process",
                "Data processing transparency",
                "Right to be forgotten",
                "Privacy policy accessible"
            ],
            "can_spam_compliance": [
                "Clear sender identification",
                "Non-deceptive subject lines",
                "Physical address included",
                "Unsubscribe mechanism",
                "Honor unsubscribe requests"
            ],
            "best_practices": [
                "Double opt-in for subscriptions",
                "Regular list cleaning",
                "Permission-based marketing",
                "Clear value proposition",
                "Respect user preferences"
            ],
            "data_protection": [
                "Secure data storage",
                "Encrypted data transmission",
                "Access controls in place",
                "Regular security audits",
                "Incident response plan"
            ]
        }
