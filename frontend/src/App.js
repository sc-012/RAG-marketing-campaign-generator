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
  Snackbar
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

function App() {
  // State management
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [campaign, setCampaign] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  // Form parameters
  const [goal, setGoal] = useState('');
  const [audience, setAudience] = useState('');
  const [tone, setTone] = useState('');
  const [query, setQuery] = useState('');

  // API base URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(`File "${selectedFile.name}" uploaded and indexed successfully!`);
      setSnackbarOpen(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error uploading file');
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
      setError(err.response?.data?.detail || 'Error generating campaign');
      setSnackbarOpen(true);
    } finally {
      setGenerating(false);
    }
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
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
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
                </Grid>
              </Grid>
            </Paper>
          </Grid>

          {/* Campaign Results Section */}
          {campaign && (
            <Grid item xs={12}>
              <Paper elevation={3} sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h5">
                    Generated Campaign
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
          {error || success}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default App;
