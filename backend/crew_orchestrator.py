"""
CrewAI Orchestrator for Multi-Agent Marketing Campaign System
"""
from crewai import Crew, Process, Task
from typing import Dict, Any, List
import asyncio
from agents import (
    DocumentAnalyzerAgent,
    CampaignStrategistAgent,
    ContentCreatorAgent,
    SocialMediaSpecialistAgent,
    EmailMarketingExpertAgent,
    ABTestingAnalystAgent,
    VisualDesignerAgent,
    PerformanceOptimizerAgent
)

class MarketingCrewOrchestrator:
    """Orchestrates multiple marketing agents using CrewAI"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.agents = self._initialize_agents()
        self.crew = None
        
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all marketing agents"""
        return {
            "document_analyzer": DocumentAnalyzerAgent(self.llm),
            "campaign_strategist": CampaignStrategistAgent(self.llm),
            "content_creator": ContentCreatorAgent(self.llm),
            "social_media_specialist": SocialMediaSpecialistAgent(self.llm),
            "email_marketing_expert": EmailMarketingExpertAgent(self.llm),
            "ab_testing_analyst": ABTestingAnalystAgent(self.llm),
            "visual_designer": VisualDesignerAgent(self.llm),
            "performance_optimizer": PerformanceOptimizerAgent(self.llm)
        }
    
    async def generate_comprehensive_campaign(self, 
                                            document_content: str,
                                            document_type: str,
                                            campaign_goal: str,
                                            target_audience: str,
                                            template_type: str = None,
                                            additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive campaign using multiple agents with CrewAI"""
        
        try:
            print(f"Creating crew with document content length: {len(document_content)}")
            print(f"Campaign goal: {campaign_goal}")
            print(f"Target audience: {target_audience}")
            
            # Create crew with specific context
            crew = self.create_crew(
                document_content=document_content,
                campaign_goal=campaign_goal,
                target_audience=target_audience,
                template_type=template_type,
                additional_params=additional_params
            )
            
            print("Starting crew execution...")
            
            # Execute the crew with timeout
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Crew execution timed out")
            
            # Set timeout to 60 seconds
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(60)
            
            try:
                result = crew.kickoff()
                signal.alarm(0)  # Cancel the alarm
                print("Crew execution completed!")
            except TimeoutError:
                signal.alarm(0)  # Cancel the alarm
                print("Crew execution timed out, using fallback response")
                return self._create_fallback_response(campaign_goal, target_audience, template_type)
            
            # Parse and structure the result
            campaign_result = self._parse_crew_result(result, campaign_goal, target_audience, template_type)
            
            return campaign_result
            
        except Exception as e:
            print(f"Error in generate_comprehensive_campaign: {str(e)}")
            # Fallback to basic response
            return {
                "campaign_overview": {
                    "objective": campaign_goal,
                    "target_audience": target_audience,
                    "campaign_type": template_type or "General Campaign",
                    "key_differentiators": ["AI-powered insights", "Data-driven strategy", "Multi-channel approach"],
                    "expected_outcomes": ["Increased brand awareness", "Higher engagement", "Improved ROI"]
                },
                "content": {
                    "overview": f"Comprehensive marketing campaign for {campaign_goal} targeting {target_audience}",
                    "platform_strategy": "Multi-platform approach with tailored content",
                    "email_campaigns": "Automated email sequences with personalization",
                    "visual_guidelines": "Brand-consistent visual design system"
                },
                "optimization": {
                    "kpis": ["Brand awareness", "Engagement rate", "Conversion rate", "ROI"],
                    "ab_testing": "Comprehensive testing framework for all campaign elements",
                    "monitoring": "Real-time performance tracking and optimization"
                },
                "error": str(e)
            }
    
    def _parse_crew_result(self, result, campaign_goal: str, target_audience: str, template_type: str = None) -> Dict[str, Any]:
        """Parse CrewAI result and structure it for the frontend - ENHANCED VERSION"""
        try:
            # Convert result to string if it's not already
            if hasattr(result, 'raw'):
                result_text = str(result.raw)
            elif hasattr(result, 'tasks_output'):
                # Handle CrewAI result format
                result_text = ""
                for task_output in result.tasks_output:
                    result_text += f"\n--- {task_output.agent.role} ---\n"
                    result_text += str(task_output.raw) + "\n"
            else:
                result_text = str(result)
            
            print(f"Parsing crew result, length: {len(result_text)}")
            print(f"First 500 characters: {result_text[:500]}")
            
            # Extract specific sections from the result using more specific keywords
            document_analysis = self._extract_section(result_text, "BRAND IDENTITY ANALYSIS", "TARGET AUDIENCE INSIGHTS", "KEY MESSAGES", "Document Analysis")
            campaign_strategy = self._extract_section(result_text, "CAMPAIGN OVERVIEW", "MESSAGING FRAMEWORK", "CHANNEL STRATEGY", "Campaign Strategy")
            content_creation = self._extract_section(result_text, "Content", "CONTENT", "Content Creation")
            social_media = self._extract_section(result_text, "Social Media", "SOCIAL", "Instagram", "Facebook", "LinkedIn")
            email_marketing = self._extract_section(result_text, "Email", "EMAIL", "Email Marketing")
            ab_testing = self._extract_section(result_text, "A/B Testing", "TESTING", "AB Testing")
            visual_design = self._extract_section(result_text, "Visual", "DESIGN", "Visual Design")
            performance = self._extract_section(result_text, "Performance", "OPTIMIZATION", "KPI", "Metrics")
            
            # Use the actual agent outputs instead of generic templates
            campaign_result = {
                "campaign_overview": {
                    "objective": campaign_goal,
                    "target_audience": target_audience,
                    "campaign_type": template_type or "General Campaign",
                    "strategy": campaign_strategy or f"Comprehensive marketing strategy for {campaign_goal}",
                    "document_analysis": document_analysis or "Document analysis completed",
                    "key_differentiators": self._extract_key_differentiators(result_text),
                    "expected_outcomes": self._extract_expected_outcomes(result_text)
                },
                "content": {
                    "overview": content_creation or f"Comprehensive content strategy for {campaign_goal} targeting {target_audience}",
                    "platform_strategy": social_media or "Multi-platform social media strategy",
                    "email_campaigns": email_marketing or "Automated email sequences with personalization",
                    "visual_guidelines": visual_design or "Brand-consistent visual design system"
                },
                "optimization": {
                    "kpis": self._extract_kpis(result_text),
                    "ab_testing": ab_testing or "Comprehensive testing framework for all campaign elements",
                    "monitoring": performance or "Real-time performance tracking and optimization"
                },
                "raw_result": result_text
            }
            
            return campaign_result
            
        except Exception as e:
            print(f"Error parsing crew result: {str(e)}")
            return {
                "campaign_overview": {
                    "objective": campaign_goal,
                    "target_audience": target_audience,
                    "campaign_type": template_type or "General Campaign",
                    "strategy": "AI-generated comprehensive marketing strategy",
                    "document_analysis": "Document analysis completed",
                    "key_differentiators": ["AI-powered insights", "Multi-agent collaboration"],
                    "expected_outcomes": ["Improved performance", "Higher engagement", "Better ROI"]
                },
                "content": {
                    "overview": f"Content strategy for {campaign_goal}",
                    "platform_strategy": "Multi-platform approach",
                    "email_campaigns": "Email marketing strategy",
                    "visual_guidelines": "Visual design guidelines"
                },
                "optimization": {
                    "kpis": ["Brand awareness", "Engagement", "Conversion", "ROI"],
                    "ab_testing": "A/B testing framework",
                    "monitoring": "Performance monitoring"
                },
                "error": f"Result parsing error: {str(e)}"
            }
    
    def _extract_section(self, text: str, *keywords) -> str:
        """Extract specific section from result text based on keywords"""
        try:
            lines = text.split('\n')
            section_lines = []
            in_section = False
            
            for line in lines:
                if any(keyword.lower() in line.lower() for keyword in keywords):
                    in_section = True
                    section_lines.append(line)
                elif in_section and line.strip() and not line.startswith('---'):
                    section_lines.append(line)
                elif in_section and line.startswith('---'):
                    break
            
            return '\n'.join(section_lines[:10]) if section_lines else None
        except:
            return None
    
    def _extract_key_differentiators(self, text: str) -> List[str]:
        """Extract key differentiators from agent output"""
        try:
            lines = text.split('\n')
            differentiators = []
            in_section = False
            
            for line in lines:
                if 'differentiator' in line.lower() or 'unique' in line.lower() or 'advantage' in line.lower():
                    in_section = True
                    if line.strip() and not line.startswith('---'):
                        differentiators.append(line.strip())
                elif in_section and line.strip() and not line.startswith('---'):
                    if line.startswith('-') or line.startswith('•'):
                        differentiators.append(line.strip())
                    elif len(differentiators) < 5:  # Limit to 5 differentiators
                        differentiators.append(line.strip())
                elif in_section and line.startswith('---'):
                    break
            
            return differentiators[:5] if differentiators else [
                "AI-powered document analysis",
                "Multi-agent collaboration", 
                "Data-driven insights",
                "Comprehensive strategy"
            ]
        except:
            return ["AI-powered insights", "Multi-agent collaboration"]
    
    def _extract_expected_outcomes(self, text: str) -> List[str]:
        """Extract expected outcomes from agent output"""
        try:
            lines = text.split('\n')
            outcomes = []
            in_section = False
            
            for line in lines:
                if 'outcome' in line.lower() or 'result' in line.lower() or 'metric' in line.lower():
                    in_section = True
                    if line.strip() and not line.startswith('---'):
                        outcomes.append(line.strip())
                elif in_section and line.strip() and not line.startswith('---'):
                    if line.startswith('-') or line.startswith('•'):
                        outcomes.append(line.strip())
                    elif len(outcomes) < 5:  # Limit to 5 outcomes
                        outcomes.append(line.strip())
                elif in_section and line.startswith('---'):
                    break
            
            return outcomes[:5] if outcomes else [
                "Improved brand awareness",
                "Higher engagement rates",
                "Better ROI",
                "Enhanced customer experience"
            ]
        except:
            return ["Improved performance", "Higher engagement", "Better ROI"]
    
    def _extract_kpis(self, text: str) -> List[str]:
        """Extract KPIs from agent output"""
        try:
            lines = text.split('\n')
            kpis = []
            in_section = False
            
            for line in lines:
                if 'kpi' in line.lower() or 'metric' in line.lower() or 'measure' in line.lower():
                    in_section = True
                    if line.strip() and not line.startswith('---'):
                        kpis.append(line.strip())
                elif in_section and line.strip() and not line.startswith('---'):
                    if line.startswith('-') or line.startswith('•'):
                        kpis.append(line.strip())
                    elif len(kpis) < 6:  # Limit to 6 KPIs
                        kpis.append(line.strip())
                elif in_section and line.startswith('---'):
                    break
            
            return kpis[:6] if kpis else [
                "Brand awareness",
                "Engagement rate", 
                "Conversion rate",
                "ROI"
            ]
        except:
            return ["Brand awareness", "Engagement", "Conversion", "ROI"]
    
    def _create_fallback_response(self, campaign_goal: str, target_audience: str, template_type: str = None) -> Dict[str, Any]:
        """Create a fallback response when crew execution fails or times out"""
        return {
            "campaign_overview": {
                "objective": campaign_goal,
                "target_audience": target_audience,
                "campaign_type": template_type or "General Campaign",
                "strategy": f"Comprehensive marketing strategy for {campaign_goal} targeting {target_audience}",
                "document_analysis": "Document analysis completed with AI-powered insights",
                "key_differentiators": [
                    "AI-powered document analysis",
                    "Multi-agent collaboration",
                    "Data-driven insights",
                    "Comprehensive strategy"
                ],
                "expected_outcomes": [
                    "Improved brand awareness",
                    "Higher engagement rates",
                    "Better ROI",
                    "Enhanced customer experience"
                ]
            },
            "content": {
                "overview": f"Multi-channel content strategy for {campaign_goal} targeting {target_audience}",
                "platform_strategy": "Platform-specific social media strategies for Instagram, Facebook, LinkedIn, Twitter, and TikTok",
                "email_campaigns": "Automated email sequences with personalization and segmentation",
                "visual_guidelines": "Brand-consistent visual design system with color palettes and typography"
            },
            "optimization": {
                "kpis": ["Brand awareness", "Engagement rate", "Conversion rate", "ROI", "Customer acquisition cost"],
                "ab_testing": "Comprehensive A/B testing framework for all campaign elements including creatives, copy, and targeting",
                "monitoring": "Real-time performance tracking with automated optimization recommendations"
            },
            "fallback": True,
            "message": "Multi-agent system completed with fallback response due to timeout or execution issues"
        }
    
    async def _analyze_documents(self, document_content: str, document_type: str) -> Dict[str, Any]:
        """Analyze uploaded documents"""
        analyzer = self.agents["document_analyzer"]
        return analyzer.analyze_document(document_content, document_type)
    
    async def _develop_campaign_strategy(self, 
                                       document_analysis: Dict[str, Any],
                                       campaign_goal: str,
                                       target_audience: str,
                                       additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """Develop campaign strategy"""
        strategist = self.agents["campaign_strategist"]
        return strategist.develop_campaign_strategy(
            document_analysis, campaign_goal, target_audience,
            additional_params.get("budget"), additional_params.get("timeline")
        )
    
    async def _create_template_content(self, 
                                     template_type: str,
                                     document_analysis: Dict[str, Any],
                                     campaign_strategy: Dict[str, Any],
                                     additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """Create content based on specific template type"""
        
        # Create tasks for different content types
        tasks = []
        
        if template_type == "email_marketing":
            tasks.append(self._create_email_content(document_analysis, campaign_strategy))
        elif template_type == "social_media_series":
            tasks.append(self._create_social_media_content(document_analysis, campaign_strategy))
        elif template_type == "content_calendar":
            tasks.append(self._create_content_calendar(document_analysis, campaign_strategy))
        elif template_type == "ab_testing":
            tasks.append(self._create_ab_testing_plan(document_analysis, campaign_strategy))
        
        # Execute tasks in parallel
        results = await asyncio.gather(*tasks)
        
        return {
            "template_type": template_type,
            "content": results[0] if results else {},
            "created_at": "2024-01-01T00:00:00Z"
        }
    
    async def _create_general_content(self, 
                                    document_analysis: Dict[str, Any],
                                    campaign_strategy: Dict[str, Any],
                                    additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """Create general content without specific template"""
        
        # Create multiple content types in parallel
        tasks = [
            self._create_email_content(document_analysis, campaign_strategy),
            self._create_social_media_content(document_analysis, campaign_strategy),
            self._create_content_calendar(document_analysis, campaign_strategy),
            self._create_ab_testing_plan(document_analysis, campaign_strategy)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            "email_marketing": results[0],
            "social_media": results[1],
            "content_calendar": results[2],
            "ab_testing": results[3]
        }
    
    async def _create_email_content(self, document_analysis: Dict[str, Any], 
                                  campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create email marketing content"""
        email_agent = self.agents["email_marketing_expert"]
        return await email_agent.create_email_campaign(document_analysis, campaign_strategy)
    
    async def _create_social_media_content(self, document_analysis: Dict[str, Any], 
                                         campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create social media content"""
        social_agent = self.agents["social_media_specialist"]
        return await social_agent.create_social_media_campaign(document_analysis, campaign_strategy)
    
    async def _create_content_calendar(self, document_analysis: Dict[str, Any], 
                                     campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create content calendar"""
        content_agent = self.agents["content_creator"]
        return await content_agent.create_content_calendar(document_analysis, campaign_strategy)
    
    async def _create_ab_testing_plan(self, document_analysis: Dict[str, Any], 
                                    campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create A/B testing plan"""
        ab_agent = self.agents["ab_testing_analyst"]
        return await ab_agent.create_ab_testing_plan(document_analysis, campaign_strategy)
    
    async def _plan_optimization(self, 
                               campaign_strategy: Dict[str, Any],
                               content_results: Dict[str, Any],
                               additional_params: Dict[str, Any]) -> Dict[str, Any]:
        """Plan performance optimization"""
        optimizer = self.agents["performance_optimizer"]
        return await optimizer.create_optimization_plan(campaign_strategy, content_results)
    
    def _compile_final_campaign(self, 
                              document_analysis: Dict[str, Any],
                              campaign_strategy: Dict[str, Any],
                              content_results: Dict[str, Any],
                              optimization_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Compile final campaign results"""
        
        return {
            "campaign_overview": {
                "document_analysis": document_analysis,
                "strategy": campaign_strategy,
                "content": content_results,
                "optimization": optimization_plan
            },
            "executive_summary": self._create_executive_summary(
                document_analysis, campaign_strategy, content_results
            ),
            "implementation_guide": self._create_implementation_guide(
                campaign_strategy, content_results
            ),
            "success_metrics": campaign_strategy.get("success_metrics", {}),
            "next_steps": self._create_next_steps(campaign_strategy, content_results),
            "generated_at": "2024-01-01T00:00:00Z"
        }
    
    def _create_executive_summary(self, 
                                document_analysis: Dict[str, Any],
                                campaign_strategy: Dict[str, Any],
                                content_results: Dict[str, Any]) -> str:
        """Create executive summary"""
        return f"""
        Campaign Strategy Summary:
        
        Based on the analysis of {document_analysis.get('document_type', 'uploaded documents')}, 
        this campaign targets {campaign_strategy.get('target_audience_strategy', {}).get('primary_audience', 'target audience')} 
        with the goal of {campaign_strategy.get('campaign_overview', {}).get('objective', 'campaign objective')}.
        
        Key highlights:
        - Brand identity: {document_analysis.get('brand_identity', {}).get('tone', 'Professional')} tone
        - Target audience: {campaign_strategy.get('target_audience_strategy', {}).get('primary_audience', 'Defined audience')}
        - Content created: {len(content_results)} content types
        - Success metrics: {len(campaign_strategy.get('success_metrics', {}).get('primary_metrics', []))} key metrics
        """
    
    def _create_implementation_guide(self, 
                                   campaign_strategy: Dict[str, Any],
                                   content_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation guide"""
        return {
            "phase_1": {
                "name": "Planning & Setup",
                "duration": "Week 1",
                "activities": [
                    "Review campaign strategy",
                    "Set up tracking systems",
                    "Prepare creative assets",
                    "Configure marketing channels"
                ]
            },
            "phase_2": {
                "name": "Content Creation",
                "duration": "Week 2",
                "activities": [
                    "Create all content assets",
                    "Design visual elements",
                    "Set up email templates",
                    "Prepare social media posts"
                ]
            },
            "phase_3": {
                "name": "Campaign Launch",
                "duration": "Week 3",
                "activities": [
                    "Soft launch with test audience",
                    "Monitor initial performance",
                    "Make quick optimizations",
                    "Full campaign launch"
                ]
            },
            "phase_4": {
                "name": "Optimization & Analysis",
                "duration": "Weeks 4-6",
                "activities": [
                    "Monitor performance metrics",
                    "A/B test different elements",
                    "Optimize based on data",
                    "Prepare final report"
                ]
            }
        }
    
    def _create_next_steps(self, 
                         campaign_strategy: Dict[str, Any],
                         content_results: Dict[str, Any]) -> List[str]:
        """Create next steps"""
        return [
            "Review and approve campaign strategy",
            "Set up tracking and analytics",
            "Create detailed project timeline",
            "Assign team members to tasks",
            "Begin content creation process",
            "Set up A/B testing framework",
            "Prepare launch checklist"
        ]
    
    def create_crew(self, document_content: str, campaign_goal: str, target_audience: str, 
                   template_type: str = None, additional_params: Dict[str, Any] = None) -> Crew:
        """Create CrewAI crew with all agents and specific context - SIMPLIFIED VERSION"""
        
        # Create simplified tasks without delegation to avoid tool errors
        tasks = [
            Task(
                description=f"""DOCUMENT ANALYSIS TASK:
You are a Senior Marketing Document Analyst. Analyze the following marketing documents and extract SPECIFIC, ACTIONABLE insights.

DOCUMENT CONTENT TO ANALYZE:
{document_content}

CAMPAIGN CONTEXT:
- Goal: {campaign_goal}
- Target Audience: {target_audience}
- Template Type: {template_type or 'General Campaign'}

REQUIRED OUTPUT FORMAT:
1. BRAND IDENTITY ANALYSIS:
   - Specific brand colors mentioned (e.g., "#FF6B6B", "Slack Purple")
   - Exact fonts used (e.g., "Helvetica Neue", "Circular")
   - Precise tone of voice (e.g., "Conversational and friendly", "Professional yet approachable")
   - Brand personality traits (e.g., "Innovative", "Reliable", "User-focused")

2. TARGET AUDIENCE INSIGHTS:
   - Specific demographics from documents (age ranges, job titles, company sizes)
   - Psychographics mentioned (values, interests, pain points)
   - Behavioral patterns identified
   - Geographic targeting if mentioned

3. KEY MESSAGES & VALUE PROPS:
   - Exact value propositions stated in documents
   - Unique selling points mentioned
   - Competitive advantages highlighted
   - Key benefits for target audience

4. PRODUCT/SERVICE FEATURES:
   - Specific features mentioned in documents
   - Technical specifications if provided
   - Pricing information if available
   - Use cases and applications

5. STRATEGIC RECOMMENDATIONS:
   - Specific opportunities identified from document analysis
   - Recommended messaging strategies
   - Channel recommendations based on document insights
   - Content themes to emphasize

IMPORTANT: Base your analysis on the ACTUAL document content provided above. Extract specific details, quotes, and insights from the documents. Do not provide generic responses.""",
                agent=self.agents["document_analyzer"].create_agent(),
                expected_output="Detailed document analysis with specific brand elements, exact quotes from documents, precise audience insights, and actionable strategic recommendations based on the actual document content"
            ),
            Task(
                description=f"""CAMPAIGN STRATEGY DEVELOPMENT TASK:
You are a Senior Marketing Campaign Strategist. Develop a comprehensive campaign strategy based on the document analysis from the previous agent.

CAMPAIGN CONTEXT:
- Goal: {campaign_goal}
- Target Audience: {target_audience}
- Template Type: {template_type or 'General Campaign'}

DOCUMENT CONTENT FOR REFERENCE:
{document_content[:1000]}...

REQUIRED OUTPUT FORMAT:
1. CAMPAIGN OVERVIEW:
   - Specific campaign objective based on document insights
   - Target audience segments with detailed personas
   - Campaign type and positioning strategy
   - Key differentiators from document analysis

2. MESSAGING FRAMEWORK:
   - Primary message based on document content
   - Supporting messages for different audience segments
   - Tone of voice recommendations from brand analysis
   - Value propositions extracted from documents

3. CHANNEL STRATEGY:
   - Primary channels recommended based on audience insights
   - Secondary channels for broader reach
   - Channel-specific messaging adaptations
   - Budget allocation recommendations

4. TIMELINE & MILESTONES:
   - Phase 1: Setup and preparation (specific weeks)
   - Phase 2: Launch and initial campaigns (specific weeks)
   - Phase 3: Optimization and scaling (specific weeks)
   - Key milestones and deliverables

5. SUCCESS METRICS:
   - Primary KPIs based on campaign goal
   - Secondary metrics for optimization
   - Measurement methods and tools
   - Expected outcomes with specific targets

6. RISK MITIGATION:
   - Potential challenges identified
   - Contingency plans for each risk
   - Monitoring and adjustment strategies

IMPORTANT: Use insights from the document analysis to create specific, actionable strategies. Reference specific details from the documents in your recommendations.""",
                agent=self.agents["campaign_strategist"].create_agent(),
                expected_output="Comprehensive campaign strategy with specific tactics, detailed timelines, budget recommendations, and measurable outcomes based on document analysis"
            ),
            Task(
                description=f"""Create engaging, platform-specific content based on the campaign strategy:

TARGET AUDIENCE: {target_audience}
CAMPAIGN GOAL: {campaign_goal}

Develop content for:
- Blog posts and articles
- Social media posts
- Video scripts
- Infographics and visual content
- Landing page copy
- Ad copy variations

Make content specific to the target audience and campaign goals.""",
                agent=self.agents["content_creator"].create_agent(),
                expected_output="Multi-channel content calendar with specific copy, creative briefs, and content variations tailored to the target audience"
            ),
            Task(
                description=f"""Develop platform-specific social media strategy:

TARGET AUDIENCE: {target_audience}
CAMPAIGN GOAL: {campaign_goal}

Create strategies for:
- Instagram (posts, stories, reels)
- Facebook (posts, ads, groups)
- Twitter/X (tweets, threads, engagement)
- LinkedIn (professional content, articles)
- TikTok (viral content, trends)
- YouTube (video content, shorts)

Include specific post ideas, hashtag strategies, engagement tactics, and influencer collaboration ideas.""",
                agent=self.agents["social_media_specialist"].create_agent(),
                expected_output="Platform-specific social media strategy with specific post ideas, hashtags, engagement tactics, and content calendar"
            ),
            Task(
                description=f"""Create comprehensive email marketing campaign:

TARGET AUDIENCE: {target_audience}
CAMPAIGN GOAL: {campaign_goal}

Develop:
- Email sequences and automation workflows
- Subject line variations
- Email templates and designs
- Segmentation strategies
- Send timing and frequency
- A/B testing recommendations
- Personalization tactics""",
                agent=self.agents["email_marketing_expert"].create_agent(),
                expected_output="Complete email marketing campaign with sequences, templates, automation workflows, and personalization strategies"
            ),
            Task(
                description=f"""Develop comprehensive A/B testing strategy:

CAMPAIGN GOAL: {campaign_goal}
TARGET AUDIENCE: {target_audience}

Create testing plans for:
- Ad creatives and copy
- Landing page elements
- Email subject lines and content
- Social media posts
- Call-to-action buttons
- Pricing and offers

Include statistical significance requirements, testing timelines, and analysis frameworks.""",
                agent=self.agents["ab_testing_analyst"].create_agent(),
                expected_output="Detailed A/B testing plan with specific test variants, statistical requirements, timelines, and analysis frameworks"
            ),
            Task(
                description=f"""Create visual design guidelines and assets:

TARGET AUDIENCE: {target_audience}
CAMPAIGN GOAL: {campaign_goal}

Develop:
- Brand color palette and usage guidelines
- Typography system and hierarchy
- Imagery style and photography guidelines
- Logo usage and variations
- Social media visual templates
- Ad creative templates
- Website design elements
- Print materials guidelines""",
                agent=self.agents["visual_designer"].create_agent(),
                expected_output="Comprehensive visual design system with specific guidelines, templates, and brand consistency rules"
            ),
            Task(
                description=f"""Optimize campaign performance and ROI:

CAMPAIGN GOAL: {campaign_goal}
TARGET AUDIENCE: {target_audience}

Develop:
- KPI framework and tracking setup
- Performance monitoring dashboards
- Optimization strategies and tactics
- Budget allocation recommendations
- ROI measurement and reporting
- Continuous improvement processes
- Competitive analysis and benchmarking""",
                agent=self.agents["performance_optimizer"].create_agent(),
                expected_output="Performance optimization plan with specific KPIs, tracking mechanisms, optimization strategies, and ROI measurement frameworks"
            )
        ]
        
        # Create crew with simplified configuration
        crew = Crew(
            agents=[agent.create_agent() for agent in self.agents.values()],
            tasks=tasks,
            process=Process.sequential,  # Sequential processing for reliability
            verbose=False,  # Reduce verbosity for cleaner execution
            memory=False,  # Disable memory to avoid complexity
            planning=False  # Disable planning to avoid delegation issues
        )
        
        return crew
