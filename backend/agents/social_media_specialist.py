"""
Social Media Specialist Agent - Specialized in social media marketing
"""
from .base_agent import BaseMarketingAgent
from typing import Dict, Any, List

class SocialMediaSpecialistAgent(BaseMarketingAgent):
    """Agent specialized in social media marketing and engagement"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Social Media Specialist",
            role="Senior Social Media Marketing Specialist",
            goal="Create engaging social media content and strategies that drive brand awareness, engagement, and conversions",
            backstory="""You are a social media expert with 10+ years of experience across all major platforms. 
            You understand platform-specific algorithms, content optimization, community management, 
            and social media advertising. You excel at creating viral content, building engaged communities, 
            and driving measurable results through social media marketing."""
        )
    
    async def create_social_media_campaign(self, document_analysis: Dict[str, Any], 
                                         campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive social media campaign"""
        
        return {
            "platform_strategy": self._develop_platform_strategy(campaign_strategy),
            "content_calendar": self._create_social_content_calendar(campaign_strategy),
            "post_templates": self._create_post_templates(document_analysis),
            "hashtag_strategy": self._develop_hashtag_strategy(document_analysis),
            "engagement_strategy": self._create_engagement_strategy(),
            "advertising_strategy": self._create_advertising_strategy(campaign_strategy),
            "community_management": self._create_community_management_plan(),
            "influencer_strategy": self._create_influencer_strategy(campaign_strategy)
        }
    
    def _develop_platform_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Develop platform-specific strategies"""
        return {
            "Instagram": {
                "content_types": ["Posts", "Stories", "Reels", "IGTV"],
                "posting_frequency": "1-2 posts daily, 3-5 stories daily",
                "optimal_times": ["9:00 AM", "12:00 PM", "3:00 PM", "6:00 PM"],
                "content_mix": {
                    "Educational": "40%",
                    "Behind_the_scenes": "25%",
                    "User_generated": "20%",
                    "Promotional": "15%"
                },
                "hashtag_count": "5-10 hashtags per post",
                "visual_style": "High-quality, branded imagery"
            },
            "Facebook": {
                "content_types": ["Posts", "Stories", "Videos", "Live"],
                "posting_frequency": "1 post daily",
                "optimal_times": ["9:00 AM", "1:00 PM", "3:00 PM"],
                "content_mix": {
                    "Educational": "35%",
                    "Entertainment": "30%",
                    "Promotional": "20%",
                    "Community": "15%"
                },
                "post_length": "40-80 characters for optimal engagement",
                "video_ratio": "60% video content"
            },
            "Twitter": {
                "content_types": ["Tweets", "Threads", "Images", "Videos"],
                "posting_frequency": "3-5 tweets daily",
                "optimal_times": ["8:00 AM", "12:00 PM", "5:00 PM"],
                "content_mix": {
                    "Industry_news": "30%",
                    "Engagement": "25%",
                    "Educational": "25%",
                    "Promotional": "20%"
                },
                "character_optimization": "Use all 280 characters effectively",
                "thread_strategy": "Create educational threads weekly"
            },
            "LinkedIn": {
                "content_types": ["Posts", "Articles", "Videos", "Polls"],
                "posting_frequency": "1 post daily, 1 article weekly",
                "optimal_times": ["8:00 AM", "12:00 PM", "5:00 PM"],
                "content_mix": {
                    "Professional_insights": "40%",
                    "Industry_news": "30%",
                    "Company_updates": "20%",
                    "Thought_leadership": "10%"
                },
                "article_length": "800-1500 words",
                "professional_tone": "Maintain professional yet approachable tone"
            },
            "TikTok": {
                "content_types": ["Videos", "Duets", "Stitches"],
                "posting_frequency": "1-2 videos daily",
                "optimal_times": ["6:00 AM", "10:00 AM", "7:00 PM"],
                "content_mix": {
                    "Trending_topics": "40%",
                    "Educational": "30%",
                    "Behind_the_scenes": "20%",
                    "Challenges": "10%"
                },
                "video_length": "15-30 seconds for maximum engagement",
                "trend_participation": "Participate in relevant trends weekly"
            }
        }
    
    def _create_social_content_calendar(self, campaign_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create 30-day social media content calendar"""
        calendar = []
        
        for day in range(1, 31):
            calendar.append({
                "day": day,
                "date": f"Day {day}",
                "platforms": self._get_daily_platforms(day),
                "content_ideas": self._get_daily_content_ideas(day),
                "hashtags": self._get_daily_hashtags(day),
                "posting_times": self._get_daily_posting_times(day),
                "engagement_goals": self._get_daily_engagement_goals(day)
            })
        
        return calendar
    
    def _create_post_templates(self, document_analysis: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Create post templates for different content types"""
        brand_identity = document_analysis.get("brand_identity", {})
        
        return {
            "educational_posts": [
                {
                    "template": "Did you know? {fact} Here's why this matters for your business: {explanation} #TipTuesday #Education",
                    "variables": ["fact", "explanation"],
                    "platforms": ["Instagram", "Facebook", "LinkedIn", "Twitter"]
                },
                {
                    "template": "5 Quick Tips for {topic}: 1. {tip1} 2. {tip2} 3. {tip3} 4. {tip4} 5. {tip5} Save this post! #Tips #{topic}",
                    "variables": ["topic", "tip1", "tip2", "tip3", "tip4", "tip5"],
                    "platforms": ["Instagram", "Facebook", "LinkedIn"]
                }
            ],
            "behind_the_scenes": [
                {
                    "template": "Behind the scenes: {activity} Our team is working hard to {goal}. Here's what goes into {process}. #BTS #TeamWork",
                    "variables": ["activity", "goal", "process"],
                    "platforms": ["Instagram", "Facebook", "TikTok"]
                }
            ],
            "user_generated_content": [
                {
                    "template": "We love seeing how our customers use {product}! Share your {product} story with #{hashtag} for a chance to be featured! #UGC #CustomerLove",
                    "variables": ["product", "hashtag"],
                    "platforms": ["Instagram", "Facebook", "TikTok"]
                }
            ],
            "promotional_posts": [
                {
                    "template": "🎉 {offer_description} Use code {code} to save {discount}%! Valid until {expiry_date}. Link in bio! #Sale #Deal #LimitedTime",
                    "variables": ["offer_description", "code", "discount", "expiry_date"],
                    "platforms": ["Instagram", "Facebook", "Twitter"]
                }
            ]
        }
    
    def _develop_hashtag_strategy(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive hashtag strategy"""
        return {
            "brand_hashtags": [
                "#{brand_name}",
                "#{brand_name}Life",
                "#{brand_name}Community"
            ],
            "industry_hashtags": [
                "#Marketing",
                "#DigitalMarketing",
                "#SocialMediaMarketing",
                "#ContentMarketing",
                "#BrandAwareness"
            ],
            "niche_hashtags": [
                "#SmallBusiness",
                "#Entrepreneur",
                "#MarketingTips",
                "#SocialMediaTips",
                "#ContentCreation"
            ],
            "trending_hashtags": [
                "#MondayMotivation",
                "#TipTuesday",
                "#WednesdayWisdom",
                "#ThrowbackThursday",
                "#FridayFeeling"
            ],
            "campaign_hashtags": [
                "#NewCampaign",
                "#BrandLaunch",
                "#ProductLaunch",
                "#SpecialOffer"
            ],
            "hashtag_guidelines": {
                "Instagram": "Use 5-10 hashtags per post",
                "Facebook": "Use 1-2 hashtags per post",
                "Twitter": "Use 1-2 hashtags per tweet",
                "LinkedIn": "Use 3-5 hashtags per post",
                "TikTok": "Use 3-5 hashtags per video"
            }
        }
    
    def _create_engagement_strategy(self) -> Dict[str, Any]:
        """Create engagement strategy"""
        return {
            "response_time": {
                "comments": "Within 2 hours during business hours",
                "messages": "Within 1 hour during business hours",
                "mentions": "Within 4 hours"
            },
            "engagement_tactics": [
                "Ask questions in posts to encourage comments",
                "Respond to all comments with meaningful replies",
                "Share user-generated content",
                "Host live Q&A sessions",
                "Create polls and interactive content"
            ],
            "community_building": [
                "Welcome new followers personally",
                "Feature community members regularly",
                "Create exclusive content for followers",
                "Host virtual events and meetups",
                "Collaborate with other brands"
            ],
            "crisis_management": {
                "negative_comments": "Respond professionally and offer to take conversation offline",
                "complaints": "Acknowledge issue, apologize if necessary, and provide solution",
                "controversy": "Address directly with transparent communication"
            }
        }
    
    def _create_advertising_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create social media advertising strategy"""
        return {
            "ad_objectives": [
                "Brand Awareness",
                "Traffic",
                "Engagement",
                "Lead Generation",
                "Conversions"
            ],
            "platform_strategy": {
                "Facebook_Instagram": {
                    "budget_allocation": "40%",
                    "ad_types": ["Image ads", "Video ads", "Carousel ads", "Stories ads"],
                    "targeting": "Interest-based, lookalike audiences, custom audiences"
                },
                "LinkedIn": {
                    "budget_allocation": "30%",
                    "ad_types": ["Sponsored content", "Message ads", "Dynamic ads"],
                    "targeting": "Job title, company size, industry, skills"
                },
                "Twitter": {
                    "budget_allocation": "20%",
                    "ad_types": ["Promoted tweets", "Promoted accounts", "Promoted trends"],
                    "targeting": "Keywords, interests, demographics"
                },
                "TikTok": {
                    "budget_allocation": "10%",
                    "ad_types": ["In-feed ads", "Brand takeovers", "Hashtag challenges"],
                    "targeting": "Demographics, interests, behaviors"
                }
            },
            "creative_guidelines": {
                "image_ads": "High-quality, eye-catching visuals with minimal text",
                "video_ads": "First 3 seconds must capture attention, clear CTA",
                "copy_guidelines": "Concise, benefit-focused, include clear CTA"
            }
        }
    
    def _create_community_management_plan(self) -> Dict[str, Any]:
        """Create community management plan"""
        return {
            "daily_activities": [
                "Monitor all social media mentions",
                "Respond to comments and messages",
                "Engage with relevant industry content",
                "Share user-generated content",
                "Post scheduled content"
            ],
            "weekly_activities": [
                "Analyze engagement metrics",
                "Plan upcoming content",
                "Research trending topics",
                "Engage with influencers",
                "Review competitor activity"
            ],
            "monthly_activities": [
                "Community growth analysis",
                "Content performance review",
                "Strategy adjustments",
                "Influencer outreach",
                "Community event planning"
            ],
            "tools_needed": [
                "Social media management platform",
                "Analytics tools",
                "Content creation tools",
                "Scheduling software",
                "Monitoring tools"
            ]
        }
    
    def _create_influencer_strategy(self, campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create influencer marketing strategy"""
        return {
            "influencer_tiers": {
                "mega_influencers": {
                    "followers": "1M+",
                    "use_case": "Brand awareness campaigns",
                    "budget_allocation": "40%"
                },
                "macro_influencers": {
                    "followers": "100K-1M",
                    "use_case": "Product launches, brand partnerships",
                    "budget_allocation": "35%"
                },
                "micro_influencers": {
                    "followers": "10K-100K",
                    "use_case": "Niche targeting, authentic content",
                    "budget_allocation": "20%"
                },
                "nano_influencers": {
                    "followers": "1K-10K",
                    "use_case": "Local campaigns, community building",
                    "budget_allocation": "5%"
                }
            },
            "collaboration_types": [
                "Sponsored posts",
                "Product reviews",
                "Takeovers",
                "Long-term partnerships",
                "Event appearances"
            ],
            "selection_criteria": [
                "Audience alignment with brand",
                "Engagement rate (3%+)",
                "Content quality and style",
                "Brand safety and values alignment",
                "Previous collaboration success"
            ]
        }
    
    # Helper methods
    def _get_daily_platforms(self, day: int) -> List[str]:
        """Get platforms for specific day"""
        platform_rotations = [
            ["Instagram", "Facebook"],
            ["Twitter", "LinkedIn"],
            ["Instagram", "TikTok"],
            ["Facebook", "LinkedIn"],
            ["Instagram", "Twitter", "TikTok"]
        ]
        return platform_rotations[day % len(platform_rotations)]
    
    def _get_daily_content_ideas(self, day: int) -> List[str]:
        """Get content ideas for specific day"""
        content_rotations = [
            ["Educational tip", "Behind-the-scenes content"],
            ["Industry news", "Company update"],
            ["User-generated content", "Product feature"],
            ["Motivational quote", "Team spotlight"],
            ["Trending topic", "Interactive poll"]
        ]
        return content_rotations[day % len(content_rotations)]
    
    def _get_daily_hashtags(self, day: int) -> List[str]:
        """Get hashtags for specific day"""
        hashtag_sets = [
            ["#Marketing", "#Tips", "#Education"],
            ["#Industry", "#News", "#Updates"],
            ["#BTS", "#BehindTheScenes", "#Team"],
            ["#Motivation", "#Inspiration", "#Quote"],
            ["#Trending", "#Viral", "#Engagement"]
        ]
        return hashtag_sets[day % len(hashtag_sets)]
    
    def _get_daily_posting_times(self, day: int) -> List[str]:
        """Get posting times for specific day"""
        time_sets = [
            ["9:00 AM", "3:00 PM"],
            ["8:00 AM", "12:00 PM", "5:00 PM"],
            ["10:00 AM", "7:00 PM"],
            ["9:00 AM", "1:00 PM", "6:00 PM"],
            ["8:00 AM", "2:00 PM", "8:00 PM"]
        ]
        return time_sets[day % len(time_sets)]
    
    def _get_daily_engagement_goals(self, day: int) -> Dict[str, int]:
        """Get engagement goals for specific day"""
        goal_sets = [
            {"likes": 50, "comments": 10, "shares": 5},
            {"likes": 75, "comments": 15, "shares": 8},
            {"likes": 100, "comments": 20, "shares": 10},
            {"likes": 60, "comments": 12, "shares": 6},
            {"likes": 80, "comments": 18, "shares": 9}
        ]
        return goal_sets[day % len(goal_sets)]
