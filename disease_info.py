def get_disease_info(self, disease_type):
    """Get information about a specific disease"""
    disease_info = {
        'Healthy_Apple': {
            'name': 'Healthy Apple',
            'description': 'The apple appears to be healthy with no visible signs of disease.',
            'severity': 'None',
            'recommendations': 'Continue regular care and monitoring.'
        },
        'Blotch_Apple': {
            'name': 'Apple Blotch',
            'description': 'A fungal disease that causes dark, irregular spots on apple skin.',
            'severity': 'Moderate',
            'recommendations': 'Remove affected fruits, improve air circulation, apply fungicide if necessary.'
        },
        'Scab_Apple': {
            'name': 'Apple Scab',
            'description': 'A fungal disease causing dark, scaly lesions on apple skin and leaves.',
            'severity': 'Moderate to High',
            'recommendations': 'Remove infected plant material, improve air circulation, apply preventive fungicide sprays.'
        },
        'Rot_Apple': {
            'name': 'Apple Rot',
            'description': 'Bacterial or fungal rot causing decay and browning of apple tissue.',
            'severity': 'High',
            'recommendations': 'Remove and dispose of affected fruits immediately to prevent spread. Check storage conditions.'
        }
    }
    
    return disease_info.get(disease_type, {
        'name': disease_type.title(),
        'description': 'Unknown disease type',
        'severity': 'Unknown',
        'recommendations': 'Consult with agricultural specialist.'
    })
