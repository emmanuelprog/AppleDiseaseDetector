from app import db
from datetime import datetime

class Detection(db.Model):
    """Model for storing apple disease detection results"""
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    disease_type = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Detection {self.id}: {self.disease_type} ({self.confidence:.2f}%)>'
    
    @property
    def formatted_timestamp(self):
        """Return formatted timestamp for display"""
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    @property
    def disease_display_name(self):
        """Return human-readable disease name"""
        disease_names = {
            'Healthy_Apple': 'Healthy Apple',
            'Blotch_Apple': 'Apple Blotch',
            'Scab_Apple': 'Apple Scab',
            'Rot_Apple': 'Apple Rot'
        }
        return disease_names.get(self.disease_type, self.disease_type.title())
    
    @property
    def confidence_class(self):
        """Return Bootstrap class based on confidence level"""
        if self.confidence >= 90:
            return 'success'
        elif self.confidence >= 70:
            return 'warning'
        else:
            return 'danger'
    
    @property
    def disease_severity_class(self):
        """Return Bootstrap class based on disease type"""
        if self.disease_type == 'Healthy_Apple':
            return 'success'
        elif self.disease_type in ['blotch_apple', 'scab_apple']:
            return 'warning'
        else:  # rot_apple
            return 'danger'
