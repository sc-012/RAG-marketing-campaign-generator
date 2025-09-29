"""
Content Creator Agent - Specialized in creating engaging marketing content
"""
from .base_agent import BaseMarketingAgent
from typing import Dict, Any, List

class ContentCreatorAgent(BaseMarketingAgent):
    """Agent specialized in creating engaging marketing content across all channels"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Content Creator",
            role="Senior Content Marketing Specialist",
            goal="Create compelling, engaging marketing content that resonates with target audiences and drives action",
            backstory="""You are a creative content marketing specialist with 12+ years of experience 
            in creating high-converting content across all marketing channels. You excel at 
            storytelling, copywriting, and creating content that not only engages audiences 
            but also drives measurable business results. You understand how to adapt content 
            for different platforms while maintaining brand consistency."""
        )
    
    async def create_content_calendar(self, document_analysis: Dict[str, Any], 
                                    campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive content calendar"""
        
        return {
            "calendar_overview": self._create_calendar_overview(campaign_strategy),
            "content_themes": self._develop_content_themes(document_analysis, campaign_strategy),
            "daily_content": self._create_daily_content_plan(campaign_strategy),
            "content_formats": self._define_content_formats(),
            "publishing_schedule": self._create_publishing_schedule(),
            "content_guidelines": self._create_content_guidelines(document_analysis),
            "repurposing_strategy": self._create_repurposing_strategy()
        }
    
    async def create_blog_content(self, document_analysis: Dict[str, Any], 
                                campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create blog content strategy"""
        
        return {
            "blog_strategy": self._develop_blog_strategy(campaign_strategy),
            "topic_ideas": self._generate_topic_ideas(document_analysis, campaign_strategy),
            "content_outlines": self._create_content_outlines(),
            "seo_optimization": self._create_seo_strategy(),
            "content_calendar": self._create_blog_calendar()
        }
    
    async def create_video_content(self, document_analysis: Dict[str, Any], 
                                 campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create video content strategy"""
        
        return {
            "video_strategy": self._develop_video_strategy(campaign_strategy),
            "video_ideas": self._generate_video_ideas(document_analysis),
            "script_outlines": self._create_video_scripts(),
            "production_requirements": self._define_production_requirements(),
            "distribution_plan": self._create_video_distribution_plan()
        }
    
    def _create_calendar_overview(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create content calendar overview"""
        return {
            "duration": campaign_strategy.get("timeline_strategy", {}).get("campaign_duration", "30 days"),
            "content_frequency": "Daily",
            "platforms": campaign_strategy.get("channel_strategy", {}).get("primary_channels", []),
            "content_mix": {
                "Educational": "40%",
                "Promotional": "30%",
                "Entertainment": "20%",
                "Behind_the_scenes": "10%"
            }
        }
    
    def _develop_content_themes(self, document_analysis: Dict[str, Any], 
                              campaign_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Develop content themes"""
        brand_identity = document_analysis.get("brand_identity", {})
        key_messages = document_analysis.get("key_messages", [])
        
        return [
            {
                "theme": "Brand Story",
                "description": "Share the brand's journey and values",
                "content_ideas": [
                    "Company history and mission",
                    "Founder's story",
                    "Brand values in action",
                    "Customer success stories"
                ],
                "frequency": "Weekly"
            },
            {
                "theme": "Product Education",
                "description": "Educate audience about products/services",
                "content_ideas": [
                    "How-to guides and tutorials",
                    "Product features and benefits",
                    "Use cases and applications",
                    "Comparison with competitors"
                ],
                "frequency": "3x per week"
            },
            {
                "theme": "Industry Insights",
                "description": "Share industry knowledge and trends",
                "content_ideas": [
                    "Market trends and analysis",
                    "Expert opinions and predictions",
                    "Industry news and updates",
                    "Best practices and tips"
                ],
                "frequency": "2x per week"
            },
            {
                "theme": "Customer Engagement",
                "description": "Engage and interact with customers",
                "content_ideas": [
                    "User-generated content",
                    "Q&A sessions",
                    "Polls and surveys",
                    "Customer testimonials"
                ],
                "frequency": "Daily"
            }
        ]
    
    def _create_daily_content_plan(self, campaign_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create daily content plan for 30 days"""
        daily_plan = []
        
        for day in range(1, 31):
            daily_plan.append({
                "day": day,
                "date": f"Day {day}",
                "theme": self._get_daily_theme(day),
                "content_type": self._get_daily_content_type(day),
                "platforms": self._get_daily_platforms(day),
                "content_idea": self._get_daily_content_idea(day),
                "hashtags": self._get_daily_hashtags(day),
                "call_to_action": self._get_daily_cta(day)
            })
        
        return daily_plan
    
    def _define_content_formats(self) -> Dict[str, Any]:
        """Define content formats for different platforms"""
        return {
            "social_media": {
                "Instagram": ["Posts", "Stories", "Reels", "IGTV"],
                "Facebook": ["Posts", "Stories", "Videos", "Live"],
                "Twitter": ["Tweets", "Threads", "Images", "Videos"],
                "LinkedIn": ["Posts", "Articles", "Videos", "Polls"],
                "TikTok": ["Videos", "Duets", "Stitches"]
            },
            "blog": {
                "formats": ["How-to guides", "Listicles", "Case studies", "Opinion pieces"],
                "lengths": ["Short (300-500 words)", "Medium (800-1200 words)", "Long (1500+ words)"]
            },
            "email": {
                "formats": ["Newsletters", "Promotional emails", "Welcome series", "Drip campaigns"],
                "types": ["HTML", "Plain text", "Interactive"]
            },
            "video": {
                "formats": ["Tutorials", "Behind-the-scenes", "Interviews", "Product demos"],
                "lengths": ["Short (15-30 seconds)", "Medium (1-3 minutes)", "Long (5+ minutes)"]
            }
        }
    
    def _create_publishing_schedule(self) -> Dict[str, Any]:
        """Create publishing schedule"""
        return {
            "monday": {
                "time": "9:00 AM",
                "content": "Motivational Monday - Inspirational content",
                "platforms": ["Instagram", "Facebook", "LinkedIn"]
            },
            "tuesday": {
                "time": "2:00 PM",
                "content": "Tip Tuesday - Educational content",
                "platforms": ["Twitter", "LinkedIn", "Blog"]
            },
            "wednesday": {
                "time": "11:00 AM",
                "content": "Wisdom Wednesday - Industry insights",
                "platforms": ["LinkedIn", "Blog", "Email"]
            },
            "thursday": {
                "time": "3:00 PM",
                "content": "Throwback Thursday - Brand history",
                "platforms": ["Instagram", "Facebook", "Twitter"]
            },
            "friday": {
                "time": "5:00 PM",
                "content": "Fun Friday - Entertaining content",
                "platforms": ["Instagram", "TikTok", "Twitter"]
            },
            "weekend": {
                "time": "10:00 AM",
                "content": "Weekend Wrap-up - Weekly highlights",
                "platforms": ["Instagram Stories", "Facebook", "Email"]
            }
        }
    
    def _create_content_guidelines(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create content guidelines based on brand analysis"""
        brand_identity = document_analysis.get("brand_identity", {})
        
        return {
            "tone_of_voice": brand_identity.get("tone", "Professional"),
            "brand_voice": brand_identity.get("voice", "First Person"),
            "color_palette": brand_identity.get("colors", []),
            "font_guidelines": brand_identity.get("fonts", []),
            "content_principles": [
                "Always provide value to the audience",
                "Maintain brand consistency",
                "Use clear and concise language",
                "Include relevant call-to-actions",
                "Optimize for each platform"
            ],
            "avoid": [
                "Jargon and technical terms",
                "Overly promotional content",
                "Inconsistent messaging",
                "Poor quality images",
                "Irrelevant hashtags"
            ]
        }
    
    def _create_repurposing_strategy(self) -> Dict[str, Any]:
        """Create content repurposing strategy"""
        return {
            "blog_to_social": "Convert blog posts into social media posts, infographics, and video scripts",
            "video_to_blog": "Transcribe videos into blog posts and create written summaries",
            "social_to_email": "Compile social media content into email newsletters",
            "long_form_to_short": "Break down long-form content into bite-sized social media posts",
            "cross_platform_adaptation": "Adapt content for different platforms while maintaining core message"
        }
    
    def _develop_blog_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Develop blog content strategy"""
        return {
            "publishing_frequency": "3x per week",
            "content_pillars": [
                "Educational content",
                "Industry insights",
                "Product updates",
                "Customer stories"
            ],
            "seo_focus": "Long-tail keywords and topic clusters",
            "content_length": "800-1500 words per post",
            "internal_linking": "Link to relevant product pages and other blog posts"
        }
    
    def _generate_topic_ideas(self, document_analysis: Dict[str, Any], 
                            campaign_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate blog topic ideas"""
        key_messages = document_analysis.get("key_messages", [])
        features_benefits = document_analysis.get("features_benefits", {})
        
        topics = []
        
        # Educational topics
        for benefit in features_benefits.get("benefits", []):
            topics.append({
                "title": f"How to {benefit.lower()}",
                "type": "How-to guide",
                "target_keyword": benefit.lower(),
                "estimated_read_time": "5-7 minutes"
            })
        
        # Industry insight topics
        topics.extend([
            {
                "title": "Top 10 Marketing Trends for 2024",
                "type": "Industry insights",
                "target_keyword": "marketing trends 2024",
                "estimated_read_time": "8-10 minutes"
            },
            {
                "title": "The Future of Digital Marketing",
                "type": "Thought leadership",
                "target_keyword": "future of digital marketing",
                "estimated_read_time": "6-8 minutes"
            }
        ])
        
        return topics
    
    def _create_content_outlines(self) -> List[Dict[str, Any]]:
        """Create content outlines for blog posts"""
        return [
            {
                "title": "How to Choose the Right Marketing Strategy",
                "outline": [
                    "Introduction: Why strategy matters",
                    "Define your goals and objectives",
                    "Know your target audience",
                    "Choose the right channels",
                    "Set your budget and timeline",
                    "Measure and optimize",
                    "Conclusion: Key takeaways"
                ]
            }
        ]
    
    def _create_seo_strategy(self) -> Dict[str, Any]:
        """Create SEO strategy for content"""
        return {
            "primary_keywords": ["marketing strategy", "digital marketing", "content marketing"],
            "long_tail_keywords": [
                "how to create marketing strategy",
                "digital marketing for small business",
                "content marketing best practices"
            ],
            "meta_descriptions": "Compelling 150-160 character descriptions",
            "internal_linking": "Link to relevant pages and posts",
            "external_linking": "Link to authoritative sources",
            "image_optimization": "Alt text and file names for all images"
        }
    
    def _create_blog_calendar(self) -> List[Dict[str, Any]]:
        """Create blog content calendar"""
        return [
            {
                "week": 1,
                "topics": [
                    "How to Define Your Target Audience",
                    "The Complete Guide to Content Marketing",
                    "5 Ways to Improve Your Marketing ROI"
                ]
            },
            {
                "week": 2,
                "topics": [
                    "Social Media Marketing Best Practices",
                    "Email Marketing: From Basics to Advanced",
                    "The Psychology of Consumer Behavior"
                ]
            }
        ]
    
    def _develop_video_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Develop video content strategy"""
        return {
            "video_types": [
                "Educational tutorials",
                "Behind-the-scenes content",
                "Customer testimonials",
                "Product demonstrations"
            ],
            "publishing_frequency": "2x per week",
            "platforms": ["YouTube", "Instagram", "TikTok", "LinkedIn"],
            "video_lengths": {
                "short": "15-30 seconds (TikTok, Instagram Reels)",
                "medium": "1-3 minutes (Instagram, Facebook)",
                "long": "5+ minutes (YouTube, LinkedIn)"
            }
        }
    
    def _generate_video_ideas(self, document_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate video content ideas"""
        return [
            {
                "title": "Behind the Scenes: How We Create Our Products",
                "type": "Behind-the-scenes",
                "duration": "2-3 minutes",
                "platforms": ["Instagram", "YouTube", "LinkedIn"]
            },
            {
                "title": "Customer Success Story: [Customer Name]",
                "type": "Testimonial",
                "duration": "1-2 minutes",
                "platforms": ["YouTube", "Instagram", "Facebook"]
            },
            {
                "title": "Quick Tutorial: How to Use [Product Feature]",
                "type": "Tutorial",
                "duration": "30-60 seconds",
                "platforms": ["TikTok", "Instagram Reels", "YouTube Shorts"]
            }
        ]
    
    def _create_video_scripts(self) -> List[Dict[str, Any]]:
        """Create video script outlines"""
        return [
            {
                "title": "Product Demo Video",
                "script_structure": [
                    "Hook (0-5 seconds): Attention-grabbing opening",
                    "Problem (5-15 seconds): Identify the problem",
                    "Solution (15-45 seconds): Present the product",
                    "Benefits (45-60 seconds): Show key benefits",
                    "CTA (60-65 seconds): Clear call to action"
                ]
            }
        ]
    
    def _define_production_requirements(self) -> Dict[str, Any]:
        """Define video production requirements"""
        return {
            "equipment": [
                "Camera (smartphone or professional)",
                "Lighting setup",
                "Microphone",
                "Tripod or stabilizer"
            ],
            "software": [
                "Video editing software",
                "Thumbnail creation tool",
                "Audio editing software"
            ],
            "team_roles": [
                "Director/Producer",
                "Camera operator",
                "Editor",
                "Script writer"
            ]
        }
    
    def _create_video_distribution_plan(self) -> Dict[str, Any]:
        """Create video distribution plan"""
        return {
            "primary_platform": "YouTube",
            "secondary_platforms": ["Instagram", "TikTok", "LinkedIn"],
            "optimization_per_platform": {
                "YouTube": "SEO-optimized titles and descriptions",
                "Instagram": "Square format, engaging captions",
                "TikTok": "Vertical format, trending hashtags",
                "LinkedIn": "Professional tone, business focus"
            }
        }
    
    # Helper methods for daily content planning
    def _get_daily_theme(self, day: int) -> str:
        """Get theme for specific day"""
        themes = ["Motivation", "Education", "Entertainment", "Behind-the-scenes", "Customer focus"]
        return themes[day % len(themes)]
    
    def _get_daily_content_type(self, day: int) -> str:
        """Get content type for specific day"""
        types = ["Post", "Story", "Video", "Image", "Poll"]
        return types[day % len(types)]
    
    def _get_daily_platforms(self, day: int) -> List[str]:
        """Get platforms for specific day"""
        platform_sets = [
            ["Instagram", "Facebook"],
            ["Twitter", "LinkedIn"],
            ["Instagram", "TikTok"],
            ["Facebook", "LinkedIn"],
            ["Instagram", "Twitter"]
        ]
        return platform_sets[day % len(platform_sets)]
    
    def _get_daily_content_idea(self, day: int) -> str:
        """Get content idea for specific day"""
        ideas = [
            "Share a motivational quote with brand context",
            "Post an educational tip related to your industry",
            "Share behind-the-scenes content from your team",
            "Feature a customer success story",
            "Ask an engaging question to your audience"
        ]
        return ideas[day % len(ideas)]
    
    def _get_daily_hashtags(self, day: int) -> List[str]:
        """Get hashtags for specific day"""
        hashtag_sets = [
            ["#motivation", "#inspiration", "#brand"],
            ["#education", "#tips", "#learning"],
            ["#bts", "#behindthescenes", "#team"],
            ["#customer", "#success", "#testimonial"],
            ["#engagement", "#question", "#community"]
        ]
        return hashtag_sets[day % len(hashtag_sets)]
    
    def _get_daily_cta(self, day: int) -> str:
        """Get call-to-action for specific day"""
        ctas = [
            "Follow us for more inspiration!",
            "Save this post for later reference",
            "Share your thoughts in the comments",
            "Visit our website to learn more",
            "Tag a friend who needs to see this"
        ]
        return ctas[day % len(ctas)]
