# MediMind AI+

**MediMind AI+** is an advanced, safety-first intelligent healthcare assistant CLI application. It allows users to input their symptoms and relevant health information (age, allergies, symptom severity, and duration) and receive a context-aware analysis, including possible conditions, risk and urgency classification, and personalized health guidance.

## Overview
MediMind AI+ bridges the gap between raw symptom-checking and safe, actionable guidance. It employs rule-based pattern recognition to maintain explainability while acting as a crucial first line of information before consulting professional medical help.

## Problem Statement
When looking up symptoms online, users often find generalized, alarming, or overly complex medical information ("Cyberchondria"). There is a need for an easy-to-use system that maps symptoms safely, accounts for contraindications (allergies, age), determines the urgency of the medical situation, and provides safe Home/OTC remedies without making medical overclaims.

## Features
- **Intelligent Symptom Analysis**: Maps free-text symptoms to common conditions.
- **Risk Scoring Engine**: Combines severity, duration, and age group to generate a unified Health Risk Score (0-100) and urgency classification (Low, Medium, High).
- **Safety Layer & Conflict Detection**: Identifies drug-allergy conflicts (e.g., NSAID/Aspirin avoidance) and flags contraindicated treatments (e.g., aspirin for children).
- **Emergency Detection**: Scans for high-risk flags like chest pain, breathing issues, or prolonged high fever.
- **Personalized Advice & Health Tips**: Delivers targeted recommendations based on condition alongside actionable daily health tips.

## Architecture
The project follows a clean, modular structure:
- `app.py`: The user entry point handling CLI interactions and input processing.
- `assistant.py`: The primary logic engine containing `MediMindAssistant` which conducts symptom mapping, calculates confidence, builds recommendations, and applies the safety layer.
- `utils.py`: Contains pure, helper functions like `calculate_risk_score`, `check_emergency`, and `get_daily_tips` to decouple domain logic from state.
- `README.md`: System documentation.

*Total Project Size is kept minimal (Under 1MB), with zero external dependencies.*

## Approach & Logic
1. **Explainable Pattern Recognition**: Instead of unpredictable LLM text generation, symptoms are mapped against a keyword density dictionary. This yields consistent, non-hallucinated conditions.
2. **Confidence Scoring**: Calculated heuristically based on the ratio of accurate keyword matches.
3. **Progressive Fallback**: If a condition cannot be matched confidently, the system defaults to conservative, generic safe-care advice and prompts clinical evaluation.

## Safety Considerations
- **Strict Disclaimers**: Displayed prominently upon initialization to ensure users know this tool does not replace professional medical advice.
- **Emergency Escalation**: Specific keyword triggers (chest pain, shortness of breath) immediately override standard logic to recommend calling emergency services.
- **Prescription Exclusion**: The system **only** recommends Over-The-Counter (OTC) medication and highlights home/lifestyle modifications.

## Testing Scenarios
To verify the engine, you can run `python app.py` and test the following edge cases:
1. **Severe Emergency**: Input "chest pain and shortness of breath", Duration: 1 day, Severity: Severe. Expected: Immediate emergency warning and high risk.
2. **Allergy Conflict**: Input "headache and fever", Allergies: "ibuprofen". Expected: OTC recommendations omit Ibuprofen/NSAIDs with explicit warnings.
3. **Child Safety**: Age Group: Child, Symptoms: "fever". Expected: Specific warning against Aspirin to prevent Reye's Syndrome.
4. **Routine Mild Symptom**: Symptoms: "runny nose, sneezing", Duration: 2 days, Severity: Mild. Expected: Common cold mapping with low risk and saline spray recommendations.

## Google Ecosystem Integration (Future Roadmap)
This prototype is designed to easily scale utilizing the Google Cloud and AI ecosystem:
- **Google Gemini API**: Can replace the basic keyword-matching algorithm in `assistant.py` with LLM-powered context understanding, allowing semantic parsing of complex, multi-lingual symptom descriptions.
- **Google Fit**: Can be integrated to fetch real-time health metrics (heart rate, sleep data, steps) to augment the Risk Score automatically.
- **Google Cloud Healthcare API**: Standardize user health records seamlessly (FHIR standards) and securely integrate with professional clinician dashboards if escalated.
