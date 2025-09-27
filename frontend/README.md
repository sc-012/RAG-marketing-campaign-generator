# DynamicRAGSystem Frontend

React frontend for the AI Marketing Campaign Generator with Material-UI components.

## 🚀 Quick Start

### Prerequisites

- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create environment file:**
   ```bash
   echo "REACT_APP_API_URL=http://localhost:8000" > .env
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## 🏗️ Architecture

- **React 18**: Modern JavaScript library for building UIs
- **Material-UI (MUI)**: Comprehensive component library
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling with responsive design

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html          # HTML template
│   └── manifest.json       # PWA manifest
├── src/
│   ├── App.js              # Main React component
│   ├── App.css             # Custom styles
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
└── package.json            # Dependencies and scripts
```

## 🎨 Features

### File Upload
- Drag and drop file upload
- Support for PDF, CSV, TXT, MD, DOCX files
- Real-time upload progress
- File validation and error handling

### Campaign Parameters
- **Campaign Goals**: Brand Awareness, Lead Generation, Sales Conversion, etc.
- **Target Audiences**: Gen Z, Millennials, Small Business Owners, etc.
- **Tones**: Professional, Casual, Inspirational, Humorous, etc.
- **Query Input**: Free-form text for campaign description

### Campaign Generation
- AI-powered campaign generation
- Real-time loading states
- Copy-to-clipboard functionality
- Responsive design for all devices

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```bash
REACT_APP_API_URL=http://localhost:8000
GENERATE_SOURCEMAP=false
```

### API Configuration

The frontend communicates with the backend through the `REACT_APP_API_URL` environment variable. For production deployment, update this to your backend URL.

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile phones (320px - 767px)

## 🎯 Component Structure

### App.js
Main component containing:
- File upload section
- Campaign parameters form
- Campaign results display
- Error handling and notifications

### Key Features
- **State Management**: React hooks for component state
- **Form Handling**: Controlled components with validation
- **API Integration**: Axios for HTTP requests
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during operations

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect GitHub repository to Vercel**
2. **Set build settings:**
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

3. **Set environment variables:**
   - `REACT_APP_API_URL`: Your backend API URL

4. **Deploy**: Vercel will automatically deploy on every push

### Netlify

1. **Build the project:**
   ```bash
   npm run build
   ```

2. **Deploy the `build` folder to Netlify**

3. **Set environment variables in Netlify dashboard**

### Manual Deployment

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Serve the `build` folder with any static file server**

## 🔧 Development

### Available Scripts

- `npm start`: Start development server
- `npm run build`: Build for production
- `npm test`: Run tests
- `npm run eject`: Eject from Create React App

### Development Server

The development server runs on `http://localhost:3000` and includes:
- Hot reloading
- Error overlay
- Source maps
- ESLint integration

### Code Structure

```javascript
// Main App component structure
function App() {
  // State management
  const [file, setFile] = useState(null);
  const [campaign, setCampaign] = useState(null);
  // ... other state

  // Event handlers
  const handleFileUpload = async (event) => { /* ... */ };
  const handleGenerateCampaign = async () => { /* ... */ };
  // ... other handlers

  return (
    <div className="App">
      {/* AppBar */}
      {/* File Upload Section */}
      {/* Campaign Parameters */}
      {/* Campaign Results */}
      {/* Notifications */}
    </div>
  );
}
```

## 🎨 Styling

### Material-UI Theme
The application uses Material-UI's default theme with custom overrides for:
- Color scheme
- Typography
- Component spacing
- Responsive breakpoints

### Custom CSS
Additional styling in `App.css` and `index.css` for:
- Custom animations
- Responsive design
- Print styles
- Scrollbar customization

## 🔍 API Integration

### Axios Configuration
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// File upload
const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

// Campaign generation
const response = await axios.post(`${API_BASE_URL}/query`, formData);
```

### Error Handling
- Network errors
- API errors
- File validation errors
- User input validation

## 🧪 Testing

### Manual Testing
1. **File Upload**: Test with different file types and sizes
2. **Form Validation**: Test required field validation
3. **API Integration**: Test with backend running
4. **Responsive Design**: Test on different screen sizes

### Automated Testing
```bash
npm test
```

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**:
   ```
   Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
   ```
   Solution: Ensure backend CORS is configured for frontend URL

2. **API Connection Errors**:
   ```
   Network Error
   ```
   Solution: Check if backend is running and `REACT_APP_API_URL` is correct

3. **Build Errors**:
   ```
   Module not found
   ```
   Solution: Run `npm install` to install dependencies

4. **File Upload Errors**:
   ```
   File type not supported
   ```
   Solution: Check file type is in allowed list (PDF, CSV, TXT, MD, DOCX)

### Debug Mode

Enable debug logging by adding to `.env`:
```bash
REACT_APP_DEBUG=true
```

## 📚 Dependencies

### Core Dependencies
- `react`: UI library
- `react-dom`: DOM rendering
- `@mui/material`: Material-UI components
- `@mui/icons-material`: Material-UI icons
- `axios`: HTTP client

### Development Dependencies
- `react-scripts`: Create React App scripts
- `web-vitals`: Performance monitoring

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] Campaign history and favorites
- [ ] Export campaigns to PDF/Word
- [ ] Advanced file management
- [ ] Real-time collaboration
- [ ] Offline support with PWA
- [ ] Advanced analytics dashboard
