import time
from itertools import combinations

# 🌟 30 core symptoms you provided
BASE_SYMPTOMS = [
    "abdominal pain", "body aches", "burning urination", "chest pain",
    "chills", "cloudy urine", "cold intolerance", "cough", "diarrhea",
    "dry cough", "ear pain", "fatigue", "fever", "frequent urination",
    "headache", "high fever", "irritability", "itching", "joint pain",
    "lower abdominal pain", "muscle pain", "nausea", "rash", "runny nose",
    "shortness of breath", "sore throat", "sneezing", "swollen lymph nodes",
    "vomiting", "weight gain"
]

class MedicalDiagnosisAI:
    """
    🧠  Medical Diagnosis AI
    ───────────────────────
    • Curated rules for 1‑, 2‑, 3‑, 4‑symptom conditions
    • PLUS every pair (435) of the 30 base symptoms
    • AI overlap scoring if no exact match
    """

    def __init__(self):
        # ───── Hand‑crafted sample rules (keep your originals here) ─────
        curated_rules = [
            # 4‑symptom examples
            {
                'symptoms': ['fever', 'cough', 'sore throat', 'runny nose'],
                'diagnosis': 'Common Cold 🤧',
                'consult'  : '👨‍⚕️ General Physician'
            },
            {
                'symptoms': ['fever', 'high fever', 'chills', 'body aches'],
                'diagnosis': 'Flu (Influenza) 🤒',
                'consult'  : '👨‍⚕️ General Physician'
            },

            # 3‑symptom example
            {
                'symptoms': ['fever', 'rash', 'joint pain'],
                'diagnosis': 'Dengue Fever 🦟',
                'consult'  : '👨‍⚕️ General Physician'
            },

            # 2‑symptom example
            {
                'symptoms': ['fever', 'cough'],
                'diagnosis': 'Viral Infection 🦠',
                'consult'  : '👨‍⚕️ General Physician'
            },

            # 1‑symptom example
            {
                'symptoms': ['fever'],
                'diagnosis': 'Isolated Fever 🌡️',
                'consult'  : '👨‍⚕️ General Physician'
            },
            {
                'symptoms': ['fever', 'cough', 'sore throat', 'runny nose',
                             'sneezing', 'nasal congestion', 'mild headache',
                             'fatigue'],
                'diagnosis': 'Common Cold',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fever', 'high fever', 'chills', 'dry cough',
                             'shortness of breath', 'fatigue', 'body aches',
                             'headache'],
                'diagnosis': 'Flu (Influenza)',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['headache', 'nausea', 'vomiting', 'sensitivity to light',
                             'sensitivity to sound', 'visual disturbances',
                             'pulsating pain'],
                'diagnosis': 'Migraine',
                'consult': 'Neurologist'
            },
            {
                'symptoms': ['skin rash', 'itching', 'swelling', 'hives',
                             'redness', 'watery eyes'],
                'diagnosis': 'Allergic Reaction',
                'consult': 'Allergist or Dermatologist'
            },
            {
                'symptoms': ['stomach pain', 'abdominal cramps', 'nausea',
                             'vomiting', 'diarrhea', 'fever'],
                'diagnosis': 'Food Poisoning',
                'consult': 'Gastroenterologist'
            },
            {
                'symptoms': ['fever', 'body aches', 'chills', 'weakness'],
                'diagnosis': 'General Viral Infection',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fatigue', 'difficulty concentrating', 'insomnia',
                             'irritability', 'muscle tension'],
                'diagnosis': 'Stress or Sleep Deprivation',
                'consult': 'Psychologist or General Physician'
            },
            {
                'symptoms': ['fever', 'dry cough', 'tiredness', 'loss of taste',
                             'loss of smell', 'shortness of breath', 'sore throat'],
                'diagnosis': 'COVID‑19',
                'consult': 'General Physician or Pulmonologist'
            },
            {
                'symptoms': ['fever', 'severe headache', 'pain behind eyes',
                             'joint pain', 'muscle pain', 'rash', 'nausea'],
                'diagnosis': 'Dengue Fever',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fever', 'chills', 'sweating', 'headache',
                             'nausea', 'vomiting', 'muscle pain'],
                'diagnosis': 'Malaria',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fever', 'abdominal pain', 'headache',
                             'constipation', 'poor appetite', 'rash'],
                'diagnosis': 'Typhoid Fever',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fever', 'fatigue', 'itching', 'blister rash',
                             'loss of appetite'],
                'diagnosis': 'Chickenpox',
                'consult': 'General Physician or Dermatologist'
            },

            # ─── DOUBLE-SYMPTOM CONDITIONS ───
            {
                'symptoms': ['fever', 'cough'],
                'diagnosis': 'Possible Viral Respiratory Infection',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['fever', 'rash'],
                'diagnosis': 'Viral Exanthem (e.g., Dengue, Measles)',
                'consult': 'Dermatologist or General Physician'
            },
            {
                'symptoms': ['headache', 'fever'],
                'diagnosis': 'Possible Flu or Meningitis',
                'consult': 'General Physician or Neurologist'
            },
            {
                'symptoms': ['nausea', 'vomiting'],
                'diagnosis': 'Gastro-intestinal Upset',
                'consult': 'Gastroenterologist'
            },
            {
                'symptoms': ['chills', 'sweating'],
                'diagnosis': 'Possible Malaria or Infection',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['joint pain', 'muscle pain'],
                'diagnosis': 'Possible Viral Infection (e.g., Chikungunya)',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['loss of taste', 'loss of smell'],
                'diagnosis': 'Possible Early COVID‑19',
                'consult': 'General Physician or ENT Specialist'
            },

            # ─── SINGLE-SYMPTOM CONDITIONS ───
            {
                'symptoms': ['fever'],
                'diagnosis': 'Isolated Fever – monitor closely',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['cough'],
                'diagnosis': 'Isolated Cough – possible irritation or early cold',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['headache'],
                'diagnosis': 'Tension Headache',
                'consult': 'General Physician or Neurologist'
            },
            {
                'symptoms': ['skin rash'],
                'diagnosis': 'Possible Allergy or Skin Infection',
                'consult': 'Dermatologist'
            },
            {
                'symptoms': ['stomach pain'],
                'diagnosis': 'Gastric Irritation or Indigestion',
                'consult': 'Gastroenterologist'
            },
            {
                'symptoms': ['fatigue'],
                'diagnosis': 'General Fatigue – may be stress, anemia, or poor sleep',
                'consult': 'General Physician'
            },
            {
                'symptoms': ['diarrhea'],
                'diagnosis': 'Acute Gastroenteritis',
                'consult': 'Gastroenterologist'
            },
            
            {
                'symptoms': ['abdominal pain'],
                'diagnosis': 'Gastric Irritation or Indigestion',
                'Doctor to consult': 'Gastroenterologist'
            },
            {
                'symptoms': ['body aches'],
                'diagnosis': 'Combination of body aches – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['burning urination'],
                'diagnosis': 'Combination of burning urination – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['chest pain'],
                'diagnosis': 'Combination of chest pain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['chills'],
                'diagnosis': 'Combination of chills – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['cloudy urine'],
                'diagnosis': 'Combination of cloudy urine – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['cold intolerance'],
                'diagnosis': 'Combination of cold intolerance – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['cough'],
                'diagnosis': 'Isolated Cough – possible irritation or early cold',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['diarrhea'],
                'diagnosis': 'Acute Gastroenteritis',
                'Doctor to consult': 'Gastroenterologist'
            },
            {
                'symptoms': ['dry cough'],
                'diagnosis': 'Combination of dry cough – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['ear pain'],
                'diagnosis': 'Combination of ear pain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['fatigue'],
                'diagnosis': 'General Fatigue – may be stress, anemia, or poor sleep',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['fever'],
                'diagnosis': 'Isolated Fever – monitor closely',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['frequent urination'],
                'diagnosis': 'Combination of frequent urination – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['headache'],
                'diagnosis': 'Tension Headache',
                'Doctor to consult': 'General Physician or Neurologist'
            },
            {
                'symptoms': ['high fever'],
                'diagnosis': 'Combination of high fever – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['irritability'],
                'diagnosis': 'Combination of irritability – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['itching'],
                'diagnosis': 'Combination of itching – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['joint pain'],
                'diagnosis': 'Combination of joint pain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['lower abdominal pain'],
                'diagnosis': 'Combination of lower abdominal pain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['muscle pain'],
                'diagnosis': 'Combination of muscle pain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['nausea'],
                'diagnosis': 'Combination of nausea – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['rash'],
                'diagnosis': 'Possible Allergy or Skin Infection',
                'Doctor to consult': 'Dermatologist'
            },
            {
                'symptoms': ['runny nose'],
                'diagnosis': 'Combination of runny nose – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['shortness of breath'],
                'diagnosis': 'Combination of shortness of breath – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['sore throat'],
                'diagnosis': 'Combination of sore throat – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['sneezing'],
                'diagnosis': 'Combination of sneezing – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['swollen lymph nodes'],
                'diagnosis': 'Combination of swollen lymph nodes – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['vomiting'],
                'diagnosis': 'Combination of vomiting – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            },
            {
                'symptoms': ['weight gain'],
                'diagnosis': 'Combination of weight gain – further evaluation 🩺',
                'Doctor to consult': 'General Physician'
            }


        ]

        # ───── Auto‑generated pair rules (435 total) ─────
        existing_pairs = {tuple(sorted(rule['symptoms']))
                          for rule in curated_rules if len(rule['symptoms']) == 2}

        pair_rules = [
            {
                'symptoms': [a, b],
                'diagnosis': f"Combination of {a} + {b} – further evaluation 🩺",
                'consult'  : '👨‍⚕️ General Physician'
            }
            for a, b in combinations(BASE_SYMPTOMS, 2)
            if tuple(sorted((a, b))) not in existing_pairs
        ]

        # Full knowledge base: curated + generated pairs
        self.knowledge_base = curated_rules + pair_rules

        # Set of all symptoms known to the system
        self.possible_symptoms = sorted(
            {s for rule in self.knowledge_base for s in rule['symptoms']}
        )

    # ───────────────────────── User input ─────────────────────────
    def get_user_symptoms(self):
        print("\n💬  Enter your symptoms (type 'done' to finish):")
        print("🗒  Examples:", ", ".join(self.possible_symptoms[:10]), "…")
        print("─────────────────────────────────────────────")
        entered = []
        while True:
            s = input("➡️  Symptom: ").strip().lower()
            if s == 'done':
                break
            if s in self.possible_symptoms:
                if s not in entered:
                    entered.append(s)
                    print(f"✅ Added: {s}")
                else:
                    print("⚠️  Already entered.")
            else:
                print("❌  Not recognized. Try again.")
        return entered

    # ───────────────────── Intelligent diagnosis ────────────────────
    def diagnose(self, symptoms):
        print("\n🔍  Evaluating your symptoms…")
        time.sleep(1)

        best_rule = None
        best_score = 0.0

        # Sort by longest rule first to prioritize specificity
        for rule in sorted(self.knowledge_base, key=lambda r: -len(r['symptoms'])):
            matches = sum(1 for s in rule['symptoms'] if s in symptoms)
            if matches == 0:
                continue
            score = matches / len(rule['symptoms'])  # overlap percentage

            # Exact match: rule fully covers user input
            if matches == len(rule['symptoms']) == len(symptoms):
                return rule['diagnosis'], rule['consult']

            # Otherwise track best partial match
            if score > best_score:
                best_score = score
                best_rule = rule

        if best_rule:
            return f"(AI) Closest match: {best_rule['diagnosis']}", best_rule['consult']

        # Should rarely happen, but just in case
        return "⚠️ AI could not confidently identify your condition.", "👨‍⚕️ General Physician"

    # ────────────────────────── Main loop ───────────────────────────
    def run(self):
        print("\n╔════════════════════════════════╗")
        print("║   🩺  MEDICAL DIAGNOSIS AI  🧠   ║")
        print("╚════════════════════════════════╝")
        print("------SYMPTOMNS LIST-------")
        print("abdominal pain  2. body aches  3. burning urination  4. chest pain  5. chills6. cloudy urine  7. cold intolerance  8. cough  9. diarrhea")  
        print("10. dry cough  11. ear pain  12. fatigue  13. fever  14. frequent urination  15. headache  16. high fever  17. irritability  18. itching")  
        print("19. joint pain  20. lower abdominal pain  21. muscle pain  22. nausea  23. rash  24. runny nose  25. shortness of breath  26. sore throat")
        print("27. sneezing  28. swollen lymph nodes  29. vomiting  30. weight gain etc.")

        symptoms = self.get_user_symptoms()
        if not symptoms:
            print("\n⚠️  No symptoms entered. Exiting.")
            return

        print(f"\n📋  You entered: {', '.join(symptoms)}")
        diagnosis, doctor = self.diagnose(symptoms)

        print("\n📊  ─── Diagnosis Result ───")
        print(f"🧬  Diagnosis : {diagnosis}")
        print(f"👨‍⚕️  Doctor to Consult  : {doctor}")
        print("────────────────────────────")
        print("⚠️  This is an AI-based suggestion only.")
        print("📞 Please consult a certified doctor in real life.")
        print("🙏 Thank you for using the system. Stay healthy!\n")


# 🚀  Run the program
if __name__ == "__main__":
    MedicalDiagnosisAI().run()
