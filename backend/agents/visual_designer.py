"""
Visual Designer Agent - Specialized in visual design and branding
"""
from .base_agent import BaseMarketingAgent
from typing import Dict, Any, List

class VisualDesignerAgent(BaseMarketingAgent):
    """Agent specialized in visual design and brand consistency"""
    
    def __init__(self, llm=None):
        super().__init__(
            name="Visual Designer",
            role="Senior Visual Designer and Brand Specialist",
            goal="Create compelling visual designs that enhance brand identity and drive engagement across all marketing channels",
            backstory="""You are a creative visual designer with 12+ years of experience in brand design, 
            marketing visuals, and digital design. You excel at creating cohesive visual identities, 
            designing for multiple platforms, and ensuring brand consistency. You understand color theory, 
            typography, layout principles, and how to create visuals that resonate with target audiences."""
        )
    
    async def create_visual_guidelines(self, document_analysis: Dict[str, Any], 
                                     campaign_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive visual design guidelines"""
        
        return {
            "brand_identity": self._develop_brand_identity(document_analysis),
            "color_palette": self._create_color_palette(document_analysis),
            "typography_system": self._create_typography_system(document_analysis),
            "visual_elements": self._define_visual_elements(document_analysis),
            "platform_adaptations": self._create_platform_adaptations(),
            "design_templates": self._create_design_templates(),
            "asset_guidelines": self._create_asset_guidelines(),
            "brand_consistency": self._create_consistency_guidelines()
        }
    
    def _develop_brand_identity(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive brand identity"""
        brand_identity = document_analysis.get("brand_identity", {})
        
        return {
            "brand_personality": {
                "traits": ["Professional", "Innovative", "Trustworthy", "Approachable"],
                "voice": brand_identity.get("voice", "First Person"),
                "tone": brand_identity.get("tone", "Professional"),
                "values": ["Quality", "Innovation", "Customer Focus", "Integrity"]
            },
            "visual_style": {
                "aesthetic": "Modern and clean",
                "mood": "Confident and approachable",
                "style_keywords": ["Minimalist", "Professional", "Contemporary", "Sophisticated"]
            },
            "brand_attributes": {
                "primary": "Trust and reliability",
                "secondary": "Innovation and progress",
                "tertiary": "Customer-centric approach"
            }
        }
    
    def _create_color_palette(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive color palette"""
        existing_colors = document_analysis.get("brand_identity", {}).get("colors", [])
        
        return {
            "primary_colors": {
                "main": existing_colors[0] if existing_colors else "#2563EB",
                "secondary": existing_colors[1] if len(existing_colors) > 1 else "#1E40AF",
                "accent": existing_colors[2] if len(existing_colors) > 2 else "#3B82F6"
            },
            "secondary_colors": {
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "info": "#06B6D4"
            },
            "neutral_colors": {
                "black": "#000000",
                "dark_gray": "#374151",
                "medium_gray": "#6B7280",
                "light_gray": "#D1D5DB",
                "white": "#FFFFFF"
            },
            "color_usage": {
                "primary": "Main brand elements, CTAs, headers",
                "secondary": "Supporting elements, borders, accents",
                "neutral": "Text, backgrounds, subtle elements",
                "semantic": "Status indicators, alerts, notifications"
            },
            "accessibility": {
                "contrast_ratio": "Minimum 4.5:1 for normal text",
                "color_blind_friendly": "Tested for colorblind accessibility",
                "high_contrast": "Alternative high-contrast palette available"
            }
        }
    
    def _create_typography_system(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive typography system"""
        existing_fonts = document_analysis.get("brand_identity", {}).get("fonts", [])
        
        return {
            "font_families": {
                "primary": existing_fonts[0] if existing_fonts else "Inter",
                "secondary": existing_fonts[1] if len(existing_fonts) > 1 else "Roboto",
                "display": existing_fonts[2] if len(existing_fonts) > 2 else "Poppins"
            },
            "font_scale": {
                "h1": {"size": "48px", "weight": "700", "line_height": "1.2"},
                "h2": {"size": "36px", "weight": "600", "line_height": "1.3"},
                "h3": {"size": "24px", "weight": "600", "line_height": "1.4"},
                "h4": {"size": "20px", "weight": "500", "line_height": "1.4"},
                "body_large": {"size": "18px", "weight": "400", "line_height": "1.6"},
                "body": {"size": "16px", "weight": "400", "line_height": "1.6"},
                "body_small": {"size": "14px", "weight": "400", "line_height": "1.5"},
                "caption": {"size": "12px", "weight": "400", "line_height": "1.4"}
            },
            "font_usage": {
                "headings": "Primary font family for all headings",
                "body_text": "Primary font family for body text",
                "captions": "Secondary font family for captions and labels",
                "display": "Display font for special emphasis"
            },
            "web_fonts": {
                "google_fonts": ["Inter", "Roboto", "Poppins"],
                "fallbacks": ["Arial", "Helvetica", "sans-serif"]
            }
        }
    
    def _define_visual_elements(self, document_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Define visual design elements"""
        return {
            "logo_usage": {
                "primary_logo": "Full color logo for most applications",
                "secondary_logo": "Monochrome version for special applications",
                "icon_logo": "Icon-only version for small spaces",
                "clear_space": "Minimum clear space around logo"
            },
            "imagery_style": {
                "photography": "Professional, high-quality, authentic",
                "illustrations": "Clean, modern, brand-consistent",
                "icons": "Minimalist, consistent style, recognizable",
                "patterns": "Subtle, geometric, brand-aligned"
            },
            "layout_principles": {
                "grid_system": "12-column responsive grid",
                "spacing": "Consistent 8px base unit",
                "alignment": "Left-aligned text, centered elements",
                "hierarchy": "Clear visual hierarchy with size and weight"
            },
            "interactive_elements": {
                "buttons": "Rounded corners, consistent padding, hover states",
                "forms": "Clean inputs, clear labels, helpful error states",
                "navigation": "Clear hierarchy, intuitive organization",
                "cards": "Subtle shadows, rounded corners, consistent spacing"
            }
        }
    
    def _create_platform_adaptations(self) -> Dict[str, Any]:
        """Create platform-specific design adaptations"""
        return {
            "email_design": {
                "width": "600px maximum",
                "background": "White or light neutral",
                "images": "Optimized for email clients",
                "fonts": "Web-safe fonts with fallbacks",
                "cta_buttons": "Large, prominent, contrasting colors"
            },
            "social_media": {
                "instagram": {
                    "post_size": "1080x1080px",
                    "story_size": "1080x1920px",
                    "aspect_ratio": "1:1 for posts, 9:16 for stories"
                },
                "facebook": {
                    "post_size": "1200x630px",
                    "cover_photo": "1200x675px",
                    "profile_picture": "170x170px"
                },
                "twitter": {
                    "post_size": "1200x675px",
                    "header": "1500x500px",
                    "profile_picture": "400x400px"
                },
                "linkedin": {
                    "post_size": "1200x627px",
                    "cover_photo": "1584x396px",
                    "profile_picture": "400x400px"
                }
            },
            "web_design": {
                "desktop": "1920px maximum width, responsive breakpoints",
                "tablet": "768px-1024px breakpoint",
                "mobile": "320px-767px breakpoint",
                "accessibility": "WCAG 2.1 AA compliance"
            },
            "print_design": {
                "business_cards": "3.5x2 inches, 300 DPI",
                "flyers": "8.5x11 inches, 300 DPI",
                "brochures": "8.5x11 inches, 300 DPI",
                "color_mode": "CMYK for print, RGB for digital"
            }
        }
    
    def _create_design_templates(self) -> Dict[str, Any]:
        """Create design templates for different use cases"""
        return {
            "email_templates": {
                "newsletter": {
                    "header": "Brand logo and navigation",
                    "hero_section": "Large image with headline",
                    "content_blocks": "Text and image combinations",
                    "footer": "Contact info and unsubscribe"
                },
                "promotional": {
                    "header": "Brand logo and offer highlight",
                    "main_content": "Offer details and CTA",
                    "social_proof": "Testimonials or reviews",
                    "footer": "Terms and contact info"
                }
            },
            "social_media_templates": {
                "instagram_post": {
                    "image_area": "1080x1080px",
                    "text_overlay": "Branded text treatment",
                    "logo_placement": "Bottom right corner",
                    "hashtag_area": "Caption space"
                },
                "facebook_post": {
                    "image_area": "1200x630px",
                    "text_area": "Post text with brand voice",
                    "cta_button": "Prominent call-to-action",
                    "branding": "Subtle brand elements"
                }
            },
            "web_templates": {
                "landing_page": {
                    "hero_section": "Headline, subheadline, CTA",
                    "features_section": "Product/service benefits",
                    "testimonials": "Social proof section",
                    "footer": "Contact and legal info"
                },
                "blog_post": {
                    "header": "Title, author, date",
                    "content": "Readable typography and spacing",
                    "sidebar": "Related content and CTAs",
                    "footer": "Social sharing and comments"
                }
            }
        }
    
    def _create_asset_guidelines(self) -> Dict[str, Any]:
        """Create guidelines for creating and using visual assets"""
        return {
            "image_requirements": {
                "resolution": "Minimum 72 DPI for web, 300 DPI for print",
                "formats": "JPEG for photos, PNG for graphics, SVG for icons",
                "optimization": "Compressed for web performance",
                "alt_text": "Descriptive alt text for accessibility"
            },
            "logo_guidelines": {
                "minimum_size": "24px height for digital, 0.5 inches for print",
                "clear_space": "Equal to height of logo on all sides",
                "backgrounds": "White, transparent, or brand color backgrounds only",
                "modifications": "No stretching, skewing, or color changes"
            },
            "color_usage": {
                "primary_colors": "Use for main brand elements and CTAs",
                "secondary_colors": "Use for supporting elements and accents",
                "neutral_colors": "Use for text, backgrounds, and subtle elements",
                "avoid": "Don't use colors outside the brand palette"
            },
            "file_organization": {
                "naming_convention": "brand_element_platform_size_version",
                "folder_structure": "Organize by platform and asset type",
                "version_control": "Keep previous versions for reference",
                "backup": "Regular backups of all brand assets"
            }
        }
    
    def _create_consistency_guidelines(self) -> Dict[str, Any]:
        """Create guidelines for maintaining brand consistency"""
        return {
            "brand_voice_consistency": {
                "tone": "Maintain consistent tone across all visual communications",
                "messaging": "Align visual elements with brand messaging",
                "personality": "Reflect brand personality in design choices"
            },
            "visual_consistency": {
                "colors": "Use brand colors consistently across all materials",
                "typography": "Apply typography system consistently",
                "spacing": "Maintain consistent spacing and layout principles",
                "imagery": "Use consistent image style and quality"
            },
            "platform_consistency": {
                "adaptation": "Adapt designs for platform while maintaining brand identity",
                "recognition": "Ensure brand is recognizable across all platforms",
                "cohesion": "Maintain visual cohesion across all touchpoints"
            },
            "quality_standards": {
                "resolution": "High-quality images and graphics",
                "alignment": "Proper alignment and spacing",
                "contrast": "Sufficient contrast for readability",
                "accessibility": "Meet accessibility standards"
            }
        }
