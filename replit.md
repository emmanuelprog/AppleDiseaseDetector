# Apple Disease Detector

## Overview

This is a Flask-based web application for detecting diseases in apple images. The system allows users to upload apple images and receive instant analysis results identifying potential diseases including blotch, scab, rot, or healthy status. The application uses a mock detection model for MVP purposes and stores detection history in a database.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Bootstrap 5 with dark theme, vanilla JavaScript
- **Structure**: Traditional server-rendered templates using Jinja2
- **Styling**: Custom CSS with CSS variables for theming, responsive design
- **Icons**: Feather icons for consistent iconography
- **User Experience**: Single-page upload flow with image preview and history viewing

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Application Structure**: Modular design with separate files for models, detection logic, and main application
- **Session Management**: Flask sessions for user state tracking
- **File Handling**: Secure file uploads with validation and storage
- **Error Handling**: Comprehensive logging and flash message system

### Database Architecture
- **ORM**: SQLAlchemy with declarative base
- **Default Database**: SQLite for development (configurable via environment variables)
- **Schema**: Single `Detection` model storing analysis results
- **Features**: Pagination support, indexed session tracking

## Key Components

### Detection Model (`models.py`)
- Stores upload results with metadata
- Tracks session-based user activity
- Provides display formatting methods
- Implements confidence scoring and severity classification

### Disease Detection Engine (`disease_detector.py`)
- Mock ML model for MVP implementation
- Image preprocessing using PIL
- Feature extraction (RGB statistics, brightness)
- Randomized detection results for demonstration

### File Upload System
- Secure filename handling with UUID generation
- File type validation (PNG, JPG, JPEG, WEBP)
- Size limits (16MB maximum)
- Image preprocessing and storage

### Template System
- Base template with consistent navigation
- Upload interface with drag-and-drop support
- Results display with confidence indicators
- Paginated history view

## Data Flow

1. **Image Upload**: User selects image file through web interface
2. **Validation**: Server validates file type, size, and security
3. **Processing**: Image is preprocessed and analyzed by detection engine
4. **Storage**: Results saved to database with session tracking
5. **Display**: Results shown with confidence scores and recommendations
6. **History**: Past detections accessible through paginated history view

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **SQLAlchemy**: Database ORM and migrations
- **Pillow (PIL)**: Image processing and manipulation
- **Werkzeug**: WSGI utilities and file handling

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Feather Icons**: Icon library for consistent styling
- **Vanilla JavaScript**: Client-side interactivity

### Infrastructure
- **Database**: SQLite (default) or PostgreSQL via DATABASE_URL
- **File Storage**: Local filesystem with organized upload directory
- **Session Storage**: Flask's built-in session management

## Deployment Strategy

### Configuration
- Environment-based configuration using `os.environ`
- Configurable database URL for different environments
- Session secret key management
- Debug mode toggling for development/production

### File Structure
- Static assets served directly by Flask
- Upload directory automatically created
- Modular code organization for maintainability

### Scalability Considerations
- Database connection pooling configured
- File upload size limits enforced
- Session-based user tracking (no authentication required)
- Ready for containerization with proper environment variables

### Security Features
- Secure filename generation using UUID
- File type validation and sanitization
- CSRF protection through Flask's built-in features
- ProxyFix middleware for proper header handling behind proxies

The application is designed as an MVP with a mock detection model that can be easily replaced with a real ML model in production. The architecture supports horizontal scaling and can be deployed to various platforms with minimal configuration changes.