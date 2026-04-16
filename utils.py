import random

def calculate_risk_score(severity: str, duration: int, age_group: str) -> int:
    """
    Combines severity, duration, and age group to output a Health Risk Score (0-100).
    """
    score = 0
    
    # Severity weighting
    severity = severity.lower().strip()
    if severity == 'mild':
        score += 10
    elif severity == 'moderate':
        score += 30
    elif severity == 'severe':
        score += 50
        
    # Duration weighting
    if duration > 14:
        score += 30
    elif duration > 7:
        score += 20
    elif duration > 3:
        score += 10
    else:
        score += 5
        
    # Age group weighting
    age_group = age_group.lower().strip()
    if age_group == 'elderly':
        score += 20
    elif age_group == 'child':
        score += 15
    else: # adult
        score += 5
        
    # Cap at 100
    return min(score, 100)

def check_emergency(symptoms: str, duration: int) -> bool:
    """
    Detects dangerous symptom combinations indicating an emergency.
    """
    symptoms_lower = symptoms.lower()
    emergency_keywords = ['chest pain', 'breathing issue', 'difficulty breathing', 'shortness of breath']
    
    # Check for direct emergency keywords
    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return True
            
    # Check for prolonged high fever
    if 'high fever' in symptoms_lower and duration >= 3:
        return True
        
    return False

def get_daily_tips() -> list:
    """
    Generates 1-2 smart health tips.
    """
    all_tips = [
        "Hydration: Aim to drink at least 8 glasses of water a day to keep your body functioning optimally.",
        "Rest cycles: Ensure you get 7-9 hours of quality sleep each night for physical and mental recovery.",
        "Nutrition: Incorporate a variety of colorful fruits and vegetables into your meals for essential vitamins.",
        "Movement: Take brief 5-minute walks every hour to maintain healthy blood circulation.",
        "Mental well-being: Practice 5 minutes of deep breathing or meditation to manage stress."
    ]
    return random.sample(all_tips, 2)
