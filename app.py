import sys
from assistant import MediMindAssistant

def print_separator():
    print("\n" + "="*50 + "\n")

def main():
    print_separator()
    print(" " * 10 + "🧠 MediMind AI+ 🧠")
    print("  Advanced Intelligent Healthcare Assistant")
    print_separator()
    print("⚠️  SAFETY DISCLAIMER: This system is for informational")
    print("purposes only and does not replace professional medical advice.")
    print_separator()
    
    print("Please provide some information so I can assist you better.\n")
    
    # 1. Symptoms
    symptoms = input("📝 What are your symptoms? (free text): ")
    if not symptoms.strip():
        print("Symptoms cannot be empty. Exiting.")
        sys.exit(1)
        
    # 2. Age group
    print("\nSelect your age group:")
    print("1: Child (0-12)")
    print("2: Adult (13-64)")
    print("3: Elderly (65+)")
    age_choice = input("Choice (1-3): ").strip()
    age_map = {'1': 'child', '2': 'adult', '3': 'elderly'}
    age_group = age_map.get(age_choice, 'adult')
    
    # 3. Allergy status
    allergies = input("\nDo you have any allergies? (Type 'none' or list them): ")
    if not allergies.strip():
        allergies = 'none'
        
    # 4. Severity level
    print("\nSelect symptom severity:")
    print("1: Mild")
    print("2: Moderate")
    print("3: Severe")
    sev_choice = input("Choice (1-3): ").strip()
    sev_map = {'1': 'mild', '2': 'moderate', '3': 'severe'}
    severity = sev_map.get(sev_choice, 'moderate')
    
    # 5. Duration
    try:
        duration = int(input("\nHow many days have you had these symptoms?: ").strip())
    except ValueError:
        print("Invalid input for duration. Defaulting to 1 day.")
        duration = 1
        
    print_separator()
    print("⏳ Analyzing your symptoms... Please wait.")
    print_separator()
    
    # Initialize and run assistant
    assistant = MediMindAssistant()
    result = assistant.analyze(symptoms, age_group, allergies, severity, duration)
    
    # Display Results
    print("📊 ANALYSIS RESULTS 📊\n")
    
    print(f"🩺 Possible Condition : {result['Condition']}")
    print(f"🎯 Confidence Score : {result['Confidence_Score']}")
    print(f"⚠️ Health Risk Score: {result['Risk_Score']} ({result['Urgency']})")
    print("\n🏥 Doctor Advice:")
    print(f"   {result['Doctor_Advice']}")
    print("\n🚫 WARNINGS & SAFETY:")
    for warn in result['Warnings']:
        print(f"   - {warn}")
        
    print("\n💊 Suggested Care:")
    print("   [OTC Medicines]")
    for otc in result['Care_Suggestions']['OTC_Medicines']:
        print(f"   - {otc}")
    print("   [Home Remedies]")
    for home in result['Care_Suggestions']['Home_Remedies']:
        print(f"   - {home}")
    print("   [Lifestyle]")
    for life in result['Care_Suggestions']['Lifestyle']:
        print(f"   - {life}")
        
    print("\n💡 Daily Health Tips:")
    for tip in result['Health_Tips']:
        print(f"   - {tip}")
        
    print_separator()
    print("Stay safe and healthy! Restart the application for new symptom queries.")
    print_separator()

if __name__ == "__main__":
    main()
