import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Paper,
  Grid,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Chip,
  Divider,
  IconButton,
  Snackbar,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import {
  Upload as UploadIcon,
  Send as SendIcon,
  Campaign as CampaignIcon,
  Insights as InsightsIcon,
  ContentCopy as CopyIcon
} from '@mui/icons-material';
import axios from 'axios';
import './App.css';

// Create a theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  // State management
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [campaign, setCampaign] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [showTemplates, setShowTemplates] = useState(false);
  
  // Multi-Agent System State
  const [multiAgentStatus, setMultiAgentStatus] = useState(null);
  const [agentCapabilities, setAgentCapabilities] = useState([]);
  const [multiAgentCampaign, setMultiAgentCampaign] = useState(null);
  const [showMultiAgent, setShowMultiAgent] = useState(false);
  const [generatingMultiAgent, setGeneratingMultiAgent] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [agentDetails, setAgentDetails] = useState({});

  // Form parameters
  const [goal, setGoal] = useState('');
  const [audience, setAudience] = useState('');
  const [tone, setTone] = useState('');
  const [query, setQuery] = useState('');

  // API base URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Load templates and multi-agent data on component mount
  React.useEffect(() => {
    loadTemplates();
    loadMultiAgentData();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/campaign-templates`);
      setTemplates(response.data.templates);
    } catch (err) {
      console.error('Error loading templates:', err);
    }
  };

  const loadMultiAgentData = async () => {
    try {
      // Load multi-agent status
      const statusResponse = await axios.get(`${API_BASE_URL}/multi-agent-status`);
      setMultiAgentStatus(statusResponse.data);
      
      // Load agent capabilities
      const capabilitiesResponse = await axios.get(`${API_BASE_URL}/agent-capabilities`);
      setAgentCapabilities(capabilitiesResponse.data.agents);
    } catch (err) {
      console.error('Error loading multi-agent data:', err);
    }
  };

  // Campaign goals options
  const goalOptions = [
    'Brand Awareness',
    'Lead Generation',
    'Sales Conversion',
    'Customer Retention',
    'Product Launch',
    'Event Promotion',
    'Social Media Growth',
    'Website Traffic'
  ];

  // Audience options
  const audienceOptions = [
    'Gen Z (18-26)',
    'Millennials (27-42)',
    'Gen X (43-58)',
    'Baby Boomers (59-77)',
    'Small Business Owners',
    'Enterprise Decision Makers',
    'Tech Enthusiasts',
    'Health & Wellness',
    'Fashion & Beauty',
    'Sports & Fitness',
    'Gaming Community',
    'Parents & Families'
  ];

  // Tone options
  const toneOptions = [
    'Professional',
    'Casual',
    'Inspirational',
    'Humorous',
    'Urgent',
    'Educational',
    'Conversational',
    'Authoritative',
    'Friendly',
    'Motivational'
  ];

  // Handle file upload
  const handleFileUpload = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const _response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(`File "${selectedFile.name}" uploaded and indexed successfully!`);
      setSnackbarOpen(true);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Error uploading file';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
      setSnackbarOpen(true);
    } finally {
      setUploading(false);
    }
  };

  // Handle campaign generation
  const handleGenerateCampaign = async () => {
    if (!goal || !audience || !tone || !query.trim()) {
      setError('Please fill in all fields');
      setSnackbarOpen(true);
      return;
    }

    setGenerating(true);
    setError('');
    setCampaign(null);

    const formData = new FormData();
    formData.append('goal', goal);
    formData.append('audience', audience);
    formData.append('tone', tone);
    formData.append('query', query);

    try {
      const response = await axios.post(`${API_BASE_URL}/query`, formData);
      setCampaign(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Error generating campaign';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
      setSnackbarOpen(true);
    } finally {
      setGenerating(false);
    }
  };

  // Handle template generation
  const handleGenerateTemplate = async () => {
    if (!goal || !audience || !tone || !query.trim() || !selectedTemplate) {
      setError('Please fill in all fields and select a template');
      setSnackbarOpen(true);
      return;
    }

    setGenerating(true);
    setError('');
    setCampaign(null);

    const formData = new FormData();
    formData.append('template_type', selectedTemplate);
    formData.append('goal', goal);
    formData.append('audience', audience);
    formData.append('tone', tone);
    formData.append('query', query);

    try {
      const response = await axios.post(`${API_BASE_URL}/generate-template`, formData);
      setCampaign(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Error generating template';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
      setSnackbarOpen(true);
    } finally {
      setGenerating(false);
    }
  };

  const handleGenerateMultiAgentCampaign = async () => {
    if (!goal || !audience || !tone || !query.trim()) {
      setError('Please fill in all fields');
      setSnackbarOpen(true);
      return;
    }

    setGeneratingMultiAgent(true);
    setError('');
    setMultiAgentCampaign(null);
    setSelectedAgent(null);
    setAgentDetails({});

    const formData = new FormData();
    formData.append('goal', goal);
    formData.append('audience', audience);
    formData.append('tone', tone);
    formData.append('query', query);
    formData.append('template_type', selectedTemplate || '');
    formData.append('additional_params', '');

    try {
      const response = await axios.post(`${API_BASE_URL}/multi-agent-campaign`, formData);
      setMultiAgentCampaign(response.data);
      
      // Extract individual agent contributions
      extractAgentContributions(response.data);
      
      setSuccess('Multi-Agent Campaign generated successfully!');
      setSnackbarOpen(true);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Error generating multi-agent campaign';
      setError(typeof errorMsg === 'string' ? errorMsg : JSON.stringify(errorMsg));
      setSnackbarOpen(true);
    } finally {
      setGeneratingMultiAgent(false);
    }
  };

  const extractAgentContributions = (campaignData) => {
    const contributions = {};
    const campaign = campaignData.multi_agent_campaign;
    
    if (campaign) {
      // Document Analyzer contribution
      if (campaign.campaign_overview?.document_analysis) {
        contributions['Document Analyzer'] = {
          role: 'Senior Marketing Document Analyst',
          contribution: campaign.campaign_overview.document_analysis,
          description: 'Analyzed uploaded documents to extract brand identity, target audience insights, and key messages.'
        };
      }
      
      // Campaign Strategist contribution
      if (campaign.campaign_overview?.strategy) {
        contributions['Campaign Strategist'] = {
          role: 'Senior Marketing Campaign Strategist',
          contribution: campaign.campaign_overview.strategy,
          description: 'Developed comprehensive campaign strategy including audience targeting, messaging, and channel selection.'
        };
      }
      
      // Content Creator contribution
      if (campaign.content) {
        contributions['Content Creator'] = {
          role: 'Senior Content Marketing Specialist',
          contribution: campaign.content,
          description: 'Created detailed content calendar, post templates, and multi-channel content strategies.'
        };
      }
      
      // Social Media Specialist contribution
      if (campaign.content?.platform_strategy) {
        contributions['Social Media Specialist'] = {
          role: 'Senior Social Media Marketing Specialist',
          contribution: campaign.content.platform_strategy,
          description: 'Developed platform-specific strategies for Instagram, Facebook, Twitter, LinkedIn, and TikTok.'
        };
      }
      
      // Email Marketing Expert contribution
      if (campaign.content?.email_campaigns) {
        contributions['Email Marketing Expert'] = {
          role: 'Senior Email Marketing Specialist',
          contribution: campaign.content.email_campaigns,
          description: 'Designed email marketing campaigns with subject lines, content structure, and automation workflows.'
        };
      }
      
      // A/B Testing Analyst contribution
      if (campaign.optimization?.ab_testing) {
        contributions['A/B Testing Analyst'] = {
          role: 'Senior A/B Testing and Optimization Specialist',
          contribution: campaign.optimization.ab_testing,
          description: 'Created A/B testing strategies and statistical analysis frameworks for campaign optimization.'
        };
      }
      
      // Visual Designer contribution
      if (campaign.content?.visual_guidelines) {
        contributions['Visual Designer'] = {
          role: 'Senior Visual Designer and Brand Specialist',
          contribution: campaign.content.visual_guidelines,
          description: 'Provided visual design guidelines, brand consistency recommendations, and creative templates.'
        };
      }
      
      // Performance Optimizer contribution
      if (campaign.optimization) {
        contributions['Performance Optimizer'] = {
          role: 'Senior Performance Marketing and Analytics Specialist',
          contribution: campaign.optimization,
          description: 'Defined KPIs, tracking mechanisms, and optimization roadmaps for campaign success measurement.'
        };
      }
    }
    
    setAgentDetails(contributions);
  };

  const handleAgentClick = (agentName) => {
    setSelectedAgent(agentName);
  };

  const renderAgentContribution = (contribution) => {
    if (!contribution) return <Typography variant="body2">No contribution data available.</Typography>;

    // Handle different types of contributions based on agent
    if (selectedAgent === 'A/B Testing Analyst') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            A/B Testing Strategy
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Document Analyzer') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Document Analysis
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Content Creator') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Content Strategy
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Email Marketing Expert') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Email Marketing Strategy
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Visual Designer') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Visual Design Guidelines
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Performance Optimizer') {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Performance Optimization
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-line', lineHeight: 1.6 }}>
            {typeof contribution === 'string' ? contribution : JSON.stringify(contribution, null, 2)}
          </Typography>
        </Box>
      );
    }
    
    if (selectedAgent === 'Campaign Strategist' && contribution.campaign_overview) {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Campaign Strategy Overview
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              <strong>Objective:</strong> {contribution.campaign_overview.objective}
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              <strong>Target Audience:</strong> {contribution.campaign_overview.target_audience}
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
              <strong>Campaign Type:</strong> {contribution.campaign_overview.campaign_type}
            </Typography>
          </Box>

          {contribution.campaign_overview.key_differentiators && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Key Differentiators:</strong>
              </Typography>
              <ul>
                {contribution.campaign_overview.key_differentiators.map((diff, index) => (
                  <li key={index}>
                    <Typography variant="body2">{diff}</Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}

          {contribution.campaign_overview.expected_outcomes && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Expected Outcomes:</strong>
              </Typography>
              <ul>
                {contribution.campaign_overview.expected_outcomes.map((outcome, index) => (
                  <li key={index}>
                    <Typography variant="body2">{outcome}</Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}

          {contribution.target_audience_strategy && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" gutterBottom color="primary">
                Target Audience Strategy
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Primary Audience:</strong> {contribution.target_audience_strategy.primary_audience}
              </Typography>
              
              {contribution.target_audience_strategy.audience_segments && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    <strong>Audience Segments:</strong>
                  </Typography>
                  {contribution.target_audience_strategy.audience_segments.map((segment, index) => (
                    <Box key={index} sx={{ ml: 2, mb: 1 }}>
                      <Typography variant="body2">
                        <strong>{segment.name}:</strong> {segment.description} (Priority: {segment.priority})
                      </Typography>
                    </Box>
                  ))}
                </Box>
              )}
            </Box>
          )}

          {contribution.messaging_strategy && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" gutterBottom color="primary">
                Messaging Strategy
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Core Message:</strong> {contribution.messaging_strategy.core_message}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Tone of Voice:</strong> {contribution.messaging_strategy.tone_of_voice}
              </Typography>
            </Box>
          )}

          {contribution.channel_strategy && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="h6" gutterBottom color="primary">
                Channel Strategy
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Primary Channels:</strong> {contribution.channel_strategy.primary_channels?.join(', ')}
              </Typography>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Secondary Channels:</strong> {contribution.channel_strategy.secondary_channels?.join(', ')}
              </Typography>
            </Box>
          )}
        </Box>
      );
    }

    // Handle other agents
    if (selectedAgent === 'Document Analyzer' && contribution.brand_identity) {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Document Analysis Results
          </Typography>
          <Typography variant="subtitle1" gutterBottom>
            <strong>Brand Tone:</strong> {contribution.brand_identity.tone}
          </Typography>
          <Typography variant="subtitle1" gutterBottom>
            <strong>Brand Voice:</strong> {contribution.brand_identity.voice}
          </Typography>
          {contribution.key_messages && contribution.key_messages.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>Key Messages Identified:</strong>
              </Typography>
              <ul>
                {contribution.key_messages.map((message, index) => (
                  <li key={index}>
                    <Typography variant="body2">{message}</Typography>
                  </li>
                ))}
              </ul>
            </Box>
          )}
        </Box>
      );
    }

    // Handle Social Media Specialist
    if (selectedAgent === 'Social Media Specialist' && contribution.Instagram) {
      return (
        <Box>
          <Typography variant="h6" gutterBottom color="primary">
            Platform-Specific Strategies
          </Typography>
          {Object.entries(contribution).map(([platform, strategy]) => (
            <Box key={platform} sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                <strong>{platform}:</strong>
              </Typography>
              <Typography variant="body2" sx={{ ml: 2 }}>
                <strong>Content Types:</strong> {strategy.content_types?.join(', ')}
              </Typography>
              <Typography variant="body2" sx={{ ml: 2 }}>
                <strong>Posting Frequency:</strong> {strategy.posting_frequency}
              </Typography>
              <Typography variant="body2" sx={{ ml: 2 }}>
                <strong>Optimal Times:</strong> {strategy.optimal_times?.join(', ')}
              </Typography>
            </Box>
          ))}
        </Box>
      );
    }

    // Default fallback for other agents
    return (
      <Box>
        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
          {JSON.stringify(contribution, null, 2)}
        </Typography>
      </Box>
    );
  };

  // Copy campaign to clipboard
  const handleCopyCampaign = () => {
    if (campaign) {
      navigator.clipboard.writeText(campaign.campaign);
      setSuccess('Campaign copied to clipboard!');
      setSnackbarOpen(true);
    }
  };

  // Clear form
  const handleClearForm = () => {
    setGoal('');
    setAudience('');
    setTone('');
    setQuery('');
    setCampaign(null);
    setError('');
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
      <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
        <Toolbar>
          <CampaignIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            DynamicRAGSystem - AI Marketing Campaign Generator
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* File Upload Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                <UploadIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Upload Marketing Documents
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Upload PDFs, CSVs, or text files to build your knowledge base for AI-powered campaign generation.
              </Typography>
              
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Button
                  variant="contained"
                  component="label"
                  startIcon={<UploadIcon />}
                  disabled={uploading}
                >
                  {uploading ? 'Uploading...' : 'Choose File'}
                  <input
                    type="file"
                    hidden
                    accept=".pdf,.txt,.csv,.md,.docx"
                    onChange={handleFileUpload}
                  />
                </Button>
                
                {file && (
                  <Chip
                    label={file.name}
                    onDelete={() => setFile(null)}
                    color="primary"
                    variant="outlined"
                  />
                )}
                
                {uploading && <CircularProgress size={24} />}
              </Box>
            </Paper>
          </Grid>

          {/* Multi-Agent System Status */}
          {multiAgentStatus && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3, backgroundColor: multiAgentStatus.multi_agent_available ? '#e8f5e8' : '#fff3e0' }}>
                <Typography variant="h5" gutterBottom>
                  <InsightsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Multi-Agent AI System
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {multiAgentStatus.multi_agent_available 
                    ? '8 specialized AI agents are ready to collaborate on your marketing campaigns'
                    : 'Multi-agent system is not available - using single-agent mode'
                  }
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
                  <Chip 
                    label={multiAgentStatus.system_status} 
                    color={multiAgentStatus.multi_agent_available ? 'success' : 'warning'}
                    variant="outlined"
                  />
                  <Chip 
                    label={`${agentCapabilities.length} Agents Available`} 
                    color="primary"
                    variant="outlined"
                  />
                </Box>

                {agentCapabilities.length > 0 && (
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      Available AI Agents:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                      {agentCapabilities.map((agent, index) => (
                        <Chip
                          key={index}
                          label={agent.name}
                          color="primary"
                          size="small"
                          title={agent.role}
                        />
                      ))}
                    </Box>
                  </Box>
                )}
              </Paper>
            </Grid>
          )}

          {/* Campaign Parameters Section */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                <InsightsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Campaign Parameters
              </Typography>
              
              <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Campaign Goal</InputLabel>
                    <Select
                      value={goal}
                      label="Campaign Goal"
                      onChange={(e) => setGoal(e.target.value)}
                    >
                      {goalOptions.map((option) => (
                        <MenuItem key={option} value={option}>
                          {option}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Target Audience</InputLabel>
                    <Select
                      value={audience}
                      label="Target Audience"
                      onChange={(e) => setAudience(e.target.value)}
                    >
                      {audienceOptions.map((option) => (
                        <MenuItem key={option} value={option}>
                          {option}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12} md={4}>
                  <FormControl fullWidth>
                    <InputLabel>Tone</InputLabel>
                    <Select
                      value={tone}
                      label="Tone"
                      onChange={(e) => setTone(e.target.value)}
                    >
                      {toneOptions.map((option) => (
                        <MenuItem key={option} value={option}>
                          {option}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Campaign Query"
                    placeholder="Describe your product, service, or campaign idea..."
                    multiline
                    rows={3}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    helperText="Be specific about what you want to promote or achieve"
                  />
                </Grid>

                <Grid item xs={12}>
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'space-between', alignItems: 'center' }}>
                    <Button
                      variant="outlined"
                      onClick={() => setShowTemplates(!showTemplates)}
                      startIcon={<CampaignIcon />}
                    >
                      {showTemplates ? 'Hide Templates' : 'Show Templates'}
                    </Button>
                    
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Button
                        variant="outlined"
                        onClick={handleClearForm}
                        disabled={generating}
                      >
                        Clear
                      </Button>
                      <Button
                        variant="contained"
                        startIcon={generating ? <CircularProgress size={20} /> : <SendIcon />}
                        onClick={handleGenerateCampaign}
                        disabled={generating || !goal || !audience || !tone || !query.trim()}
                      >
                        {generating ? 'Generating...' : 'Generate Campaign'}
                      </Button>
                    </Box>
                  </Box>
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Campaign Generation Buttons */}
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                <SendIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Generate Campaign
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Choose how you want to generate your marketing campaign
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
                {/* Multi-Agent Campaign Button */}
                {multiAgentStatus?.multi_agent_available && (
                  <Button
                    variant="contained"
                    size="large"
                    color="success"
                    startIcon={generatingMultiAgent ? <CircularProgress size={20} /> : <InsightsIcon />}
                    onClick={handleGenerateMultiAgentCampaign}
                    disabled={generatingMultiAgent || generating || !goal || !audience || !tone || !query.trim()}
                    sx={{ minWidth: 250 }}
                  >
                    {generatingMultiAgent ? 'Multi-Agents Working...' : '🤖 Multi-Agent Campaign'}
                  </Button>
                )}
                
                {/* Single Agent Campaign Button */}
                <Button
                  variant="contained"
                  size="large"
                  startIcon={generating ? <CircularProgress size={20} /> : <SendIcon />}
                  onClick={handleGenerateCampaign}
                  disabled={generating || generatingMultiAgent || !goal || !audience || !tone || !query.trim()}
                  sx={{ minWidth: 200 }}
                >
                  {generating ? 'Generating...' : 'Single Agent Campaign'}
                </Button>
                
                {/* Show Templates Button */}
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<CampaignIcon />}
                  onClick={() => setShowTemplates(!showTemplates)}
                  sx={{ minWidth: 200 }}
                >
                  {showTemplates ? 'Hide Templates' : 'Show Templates'}
                </Button>
              </Box>
              
              {multiAgentStatus?.multi_agent_available && (
                <Box sx={{ mt: 2, p: 2, backgroundColor: '#f5f5f5', borderRadius: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Multi-Agent Campaign:</strong> Uses 8 specialized AI agents working together to create comprehensive, professional-grade marketing campaigns with detailed strategies, content calendars, and optimization plans.
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>

          {/* Campaign Templates Section */}
          {showTemplates && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h5" gutterBottom>
                  <CampaignIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Campaign Templates
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Choose a specialized template for more detailed campaign generation
                </Typography>
                
                <Grid container spacing={2}>
                  {templates.map((template) => (
                    <Grid item xs={12} md={6} key={template.id}>
                      <Card 
                        sx={{ 
                          cursor: 'pointer',
                          border: selectedTemplate === template.id ? 2 : 1,
                          borderColor: selectedTemplate === template.id ? 'primary.main' : 'divider',
                          '&:hover': { boxShadow: 3 }
                        }}
                        onClick={() => setSelectedTemplate(template.id)}
                      >
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            {template.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {template.description}
                          </Typography>
                          <Box sx={{ mb: 2 }}>
                            <Typography variant="subtitle2" gutterBottom>
                              Channels:
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                              {template.channels.map((channel) => (
                                <Chip key={channel} label={channel} size="small" variant="outlined" />
                              ))}
                            </Box>
                          </Box>
                          <Box>
                            <Typography variant="subtitle2" gutterBottom>
                              Components:
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                              {template.components.map((component) => (
                                <Chip key={component} label={component} size="small" color="primary" />
                              ))}
                            </Box>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
                
                {selectedTemplate && (
                  <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
                    <Button
                      variant="contained"
                      size="large"
                      startIcon={generating ? <CircularProgress size={20} /> : <SendIcon />}
                      onClick={handleGenerateTemplate}
                      disabled={generating || !goal || !audience || !tone || !query.trim()}
                    >
                      {generating ? 'Generating Template...' : 'Generate Template Campaign'}
                    </Button>
                  </Box>
                )}
              </Paper>
            </Grid>
          )}

          {/* Campaign Results Section */}
          {campaign && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h5">
                    {campaign.template_type ? `Generated ${campaign.template_type.replace('_', ' ').toUpperCase()} Campaign` : 'Generated Campaign'}
                  </Typography>
                  <IconButton onClick={handleCopyCampaign} color="primary">
                    <CopyIcon />
                  </IconButton>
                </Box>

                <Divider sx={{ mb: 2 }} />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Parameters Used:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={`Goal: ${campaign.parameters.goal}`} color="primary" variant="outlined" />
                    <Chip label={`Audience: ${campaign.parameters.audience}`} color="secondary" variant="outlined" />
                    <Chip label={`Tone: ${campaign.parameters.tone}`} color="success" variant="outlined" />
                  </Box>
                </Box>

                <Card>
                  <CardContent>
                    <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                      {campaign.campaign}
                    </Typography>
                  </CardContent>
                </Card>

                {campaign.context_used > 0 && (
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                    Generated using {campaign.context_used} relevant document(s) from your knowledge base
                  </Typography>
                )}
              </Paper>
            </Grid>
          )}

          {/* Multi-Agent Campaign Results Section */}
          {multiAgentCampaign && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h5" color="success.main">
                    🤖 Multi-Agent Campaign Generated
                  </Typography>
                  <IconButton onClick={() => navigator.clipboard.writeText(JSON.stringify(multiAgentCampaign, null, 2))} color="primary">
                    <CopyIcon />
                  </IconButton>
                </Box>

                <Divider sx={{ mb: 2 }} />

                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Parameters Used:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    <Chip label={`Goal: ${multiAgentCampaign.parameters.goal}`} color="primary" variant="outlined" />
                    <Chip label={`Audience: ${multiAgentCampaign.parameters.audience}`} color="secondary" variant="outlined" />
                    <Chip label={`Tone: ${multiAgentCampaign.parameters.tone}`} color="success" variant="outlined" />
                    <Chip label={`Agents Used: ${multiAgentCampaign.agents_used.length}`} color="info" variant="outlined" />
                  </Box>
                </Box>

                {/* Agents Used */}
                <Box sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6">
                      AI Agents That Worked on This Campaign (Click to see individual contributions):
                    </Typography>
                    {selectedAgent && (
                      <Button 
                        size="small" 
                        variant="outlined" 
                        onClick={() => setSelectedAgent(null)}
                        sx={{ ml: 2 }}
                      >
                        Clear Selection
                      </Button>
                    )}
                  </Box>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {multiAgentCampaign.agents_used.map((agent, index) => (
                      <Chip 
                        key={index} 
                        label={agent} 
                        color={selectedAgent === agent ? "primary" : "success"} 
                        variant={selectedAgent === agent ? "filled" : "outlined"}
                        onClick={() => handleAgentClick(agent)}
                        sx={{ 
                          cursor: 'pointer',
                          '&:hover': { 
                            backgroundColor: selectedAgent === agent ? 'primary.dark' : 'success.light',
                            color: 'white'
                          }
                        }}
                      />
                    ))}
                  </Box>
                  {selectedAgent && (
                    <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                      Selected: {selectedAgent} - Click another agent to switch or "Clear Selection" to hide details
                    </Typography>
                  )}
                </Box>

                {/* Individual Agent Contribution */}
                {selectedAgent && agentDetails[selectedAgent] && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom color="primary">
                      🤖 {selectedAgent} - Individual Contribution
                    </Typography>
                    <Card sx={{ border: '2px solid', borderColor: 'primary.main' }}>
                      <CardContent>
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                            <strong>Role:</strong> {agentDetails[selectedAgent].role}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            <strong>Description:</strong> {agentDetails[selectedAgent].description}
                          </Typography>
                        </Box>
                        <Divider sx={{ mb: 2 }} />
                        <Typography variant="h6" gutterBottom>
                          Contribution Details:
                        </Typography>
                        <Box sx={{ maxHeight: '400px', overflowY: 'auto' }}>
                          {renderAgentContribution(agentDetails[selectedAgent].contribution)}
                        </Box>
                      </CardContent>
                    </Card>
                  </Box>
                )}

                {/* Executive Summary */}
                {multiAgentCampaign.multi_agent_campaign?.executive_summary && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Executive Summary:
                    </Typography>
                    <Card>
                      <CardContent>
                        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
                          {multiAgentCampaign.multi_agent_campaign.executive_summary}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Box>
                )}

                {/* Next Steps */}
                {multiAgentCampaign.multi_agent_campaign?.next_steps && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      Next Steps:
                    </Typography>
                    <Box sx={{ pl: 2 }}>
                      {multiAgentCampaign.multi_agent_campaign.next_steps.map((step, index) => (
                        <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                          {index + 1}. {step}
                        </Typography>
                      ))}
                    </Box>
                  </Box>
                )}

                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  Generated by {multiAgentCampaign.agents_used.length} specialized AI agents working in collaboration
                </Typography>
              </Paper>
            </Grid>
          )}

        </Grid>
      </Container>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSnackbarOpen(false)}
          severity={error ? 'error' : 'success'}
          sx={{ width: '100%' }}
        >
          {error ? (typeof error === 'string' ? error : String(error)) : (typeof success === 'string' ? success : String(success))}
        </Alert>
      </Snackbar>
      </div>
    </ThemeProvider>
  );
}

export default App;
