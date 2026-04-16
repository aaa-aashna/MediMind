from utils import calculate_risk_score, check_emergency, get_daily_tips
import random

class MediMindAssistant:
    def __init__(self):
        # Basic pattern recognition using keyword grouping
        self.condition_map = {
            'common cold': ['runny nose', 'congestion', 'sore throat', 'mild cough', 'sneezing'],
            'flu (influenza)': ['fever', 'chills', 'muscle ache', 'fatigue', 'weakness', 'dry cough'],
            'allergies': ['itchy eyes', 'sneezing', 'runny nose', 'watery eyes', 'rash'],
            'gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'stomach cramps', 'abdominal pain'],
            'migraine': ['severe headache', 'throbbing pain', 'light sensitivity', 'nausea', 'aura'],
            'covid-19 (suspected)': ['loss of taste', 'loss of smell', 'fever', 'dry cough', 'fatigue', 'shortness of breath'],
            'acid reflux / gerd': ['heartburn', 'acid taste', 'chest burning', 'burping']
        }
        
        # Recommendations mapped to condition
        self.recommendations_map = {
            'common cold': {
                'otc': ['Paracetamol or Ibuprofen (for discomfort)', 'Saline nasal spray'],
                'home': ['Stay hydrated', 'Rest', 'Warm tea with honey', 'Steam inhalation'],
                'lifestyle': ['Avoid cold beverages', 'Keep warm']
            },
            'flu (influenza)': {
                'otc': ['Paracetamol (for fever)', 'Cough suppressants (if coughing)'],
                'home': ['Ample rest', 'High fluid intake (water, broths)', 'Warm compresses'],
                'lifestyle': ['Isolate to prevent spreading', 'Sleep 8+ hours']
            },
            'allergies': {
                'otc': ['Antihistamines (e.g., Cetirizine, Loratadine) - check for drowsiness'],
                'home': ['Cold compress for eyes', 'Rinse the nasal passages'],
                'lifestyle': ['Avoid known allergens', 'Keep windows closed during high pollen seasons']
            },
            'gastroenteritis': {
                'otc': ['Oral rehydration salts (ORS)'],
                'home': ['BRAT diet (Bananas, Rice, Applesauce, Toast)', 'Clear fluids', 'Rest'],
                'lifestyle': ['Avoid dairy, caffeine, and spicy foods until recovered']
            },
            'migraine': {
                'otc': ['Ibuprofen or Aspirin (if no contraindications)'],
                'home': ['Rest in a dark, quiet room', 'Cold pack on forehead'],
                'lifestyle': ['Identify and avoid triggers (e.g., certain foods, stress, lack of sleep)']
            },
            'covid-19 (suspected)': {
                'otc': ['Paracetamol (for fever)'],
                'home': ['Isolation', 'Rest', 'Hydration', 'Monitor oxygen levels if possible'],
                'lifestyle': ['Wear a mask if around others in the household']
            },
            'acid reflux / gerd': {
                'otc': ['Antacids (e.g., Calcium Carbonate)'],
                'home': ['Elevate the head of your bed', 'Chew gum to increase saliva'],
                'lifestyle': ['Avoid eating 2-3 hours before bed', 'Reduce intake of acidic or spicy foods']
            }
        }
    
    def _map_condition(self, symptoms_text):
        """Maps free text symptoms to conditions using basic keyword grouping."""
        symptoms_text = symptoms_text.lower()
        best_match = 'unknown condition'
        highest_score = 0
        
        for condition, keywords in self.condition_map.items():
            score = sum(1 for kw in keywords if kw in symptoms_text)
            if score > highest_score:
                highest_score = score
                best_match = condition
                
        # Calculate a pseudo-confidence score based on keywords matched vs total text words
        # This is basic logic to keep things explainable and avoid randomness.
        if highest_score > 0:
            confidence = min(100, 40 + (highest_score * 15))
        else:
            confidence = 30 # Baseline for unknown
            
        return best_match, confidence

    def analyze(self, symptoms, age_group, allergies, severity, duration):
        """Main evaluation engine."""
        
        # 1. Emergency Detection
        is_emergency = check_emergency(symptoms, duration)
        
        # 2. Risk Score
        risk_score = calculate_risk_score(severity, duration, age_group)
        if is_emergency:
            risk_score = 100
            
        # 3. Urgency Level
        if risk_score >= 70:
            urgency = "High (Doctor Recommended)"
        elif risk_score >= 40:
            urgency = "Medium (Monitor Closely)"
        else:
            urgency = "Low (Self-Care)"
            
        # 4. Map Symptoms to Condition
        condition, confidence = self._map_condition(symptoms)
        if is_emergency:
            confidence = max(confidence, 80) # Increased confidence due to severe indicators
            
        # 5. Smart Recommendations
        recs = self.recommendations_map.get(condition, {
            'otc': ['Consult a pharmacist for symptomatic relief'],
            'home': ['Rest', 'Hydration'],
            'lifestyle': ['Monitor symptoms closely']
        })
        
        # 6. Safety Layer (Allergies & Contraindications)
        warnings = []
        allergies_lower = allergies.lower()
        if 'ibuprofen' in allergies_lower or 'nsaid' in allergies_lower:
            warnings.append("ALLERGY ALERT: Avoid Ibuprofen, Aspirin, or any NSAIDs.")
            # Filter recommendations safely
            recs['otc'] = [med for med in recs['otc'] if 'ibuprofen' not in med.lower() and 'aspirin' not in med.lower()]
            
        if 'paracetamol' in allergies_lower or 'acetaminophen' in allergies_lower:
            warnings.append("ALLERGY ALERT: Avoid Paracetamol (Acetaminophen).")
            recs['otc'] = [med for med in recs['otc'] if 'paracetamol' not in med.lower()]
            
        if 'aspirin' in allergies_lower and age_group.lower() == 'child':
            warnings.append("SAFETY WARNING: Aspirin is strictly contraindicated for children (risk of Reye's syndrome).")
            
        if not warnings and allergies_lower not in ['none', 'no', 'n/a', '']:
            warnings.append(f"Please consult a doctor to ensure OTC medications do not conflict with your allergy: {allergies}")
            
        if is_emergency:
            warnings.append("EMERGENCY DETECTED: DO NOT RELY ON HOME CARE.")

        # 7. Doctor Advice
        if is_emergency:
            doctor_advice = "🚨 SEEK IMMEDIATE MEDICAL ATTENTION. Visit the nearest emergency room or call emergency services."
        elif risk_score >= 70:
            doctor_advice = "Please schedule an appointment with a healthcare provider as soon as possible."
        elif risk_score >= 40:
             doctor_advice = "Monitor your symptoms. If they worsen or persist for another 48 hours, consult a doctor."
        else:
             doctor_advice = "Routine monitoring. Consult a doctor if symptoms worsen unexpectedly."
             
        # Format Results
        result = {
            "Condition": condition.title(),
            "Confidence_Score": f"{confidence}%",
            "Risk_Score": f"{risk_score}/100",
            "Urgency": urgency,
            "Care_Suggestions": {
                "OTC_Medicines": recs['otc'] if risk_score < 80 else ["Avoid self-medication due to high risk"],
                "Home_Remedies": recs['home'],
                "Lifestyle": recs['lifestyle']
            },
            "Warnings": warnings if warnings else ["No known critical conflicts based on inputs."],
            "Doctor_Advice": doctor_advice,
            "Health_Tips": get_daily_tips()
        }
        
        return result
