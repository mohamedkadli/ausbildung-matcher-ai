from typing import List, Dict

class Applicant:
    def __init__(self, name: str, language_level: str, education: str, skills: List[str]):
        self.name = name
        self.language_level = language_level.strip()
        self.education = education.strip()
        self.skills = [s.lower().strip() for s in skills]

class AusbildungPosition:
    def __init__(self, title: str, min_language: str, required_skills: List[str], preferred_education: str):
        self.title = title
        self.min_language = min_language.upper()
        self.required_skills = [s.lower().strip() for s in required_skills]
        self.preferred_education = preferred_education

class MatchingEngine:
    LANG_WEIGHTS = {
        'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 
        'C1': 5, 'C2': 6, 'Muttersprache': 6
    }

    def __init__(self, applicant: Applicant, position: AusbildungPosition):
        self.applicant = applicant
        self.position = position

    def calculate_score(self) -> Dict:
        app_lang_val = self.LANG_WEIGHTS.get(self.applicant.language_level, 0)
        req_lang_val = self.LANG_WEIGHTS.get(self.position.min_language, 0)
        
        # 1. Sprachbewertung (35 Punkte)
        if app_lang_val >= req_lang_val:
            lang_score = 35.0
        else:
            lang_score = max(0.0, 35.0 - (req_lang_val - app_lang_val) * 12.0)

        # 2. Skills-Bewertung (45 Punkte)
        matched_skills = [s for s in self.position.required_skills if s in self.applicant.skills]
        missing_skills = [s for s in self.position.required_skills if s not in self.applicant.skills]
        
        if self.position.required_skills:
            skill_score = (len(matched_skills) / len(self.position.required_skills)) * 45.0
        else:
            skill_score = 45.0

        # 3. Bildungsbewertung (20 Punkte)
        edu = self.applicant.education.lower()
        if "bachelor it" in edu or "master it" in edu or "it-studium" in edu or "ki" in edu or "informatik" in edu:
            edu_score = 20.0
        elif "bac+1" in edu or "bac+2" in edu or "berufsausbildung" in edu or "fachhochschulreife" in edu:
            edu_score = 18.0
        elif "abitur" in edu or "baccalauréat" in edu or "anderes studium" in edu:
            edu_score = 16.0
        elif "realschulabschluss" in edu:
            edu_score = 14.0
        else:
            edu_score = 10.0

        total_score = round(lang_score + skill_score + edu_score, 1)

        return {
            "total_score": total_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "language_satisfied": app_lang_val >= req_lang_val
        }

    def generate_feedback(self, match_result: Dict) -> List[str]:
        feedback = []
        
        if not match_result["language_satisfied"]:
            feedback.append(
                f"⚠️ Sprachniveau verbessern: Erforderlich ist mindestens {self.position.min_language}, "
                f"aktuelles Niveau ist {self.applicant.language_level}."
            )
        else:
            feedback.append("✅ Deutschkenntnisse erfüllen die Anforderungen der Stelle perfekt.")

        if match_result["missing_skills"]:
            missing_str = ", ".join(match_result["missing_skills"]).title()
            feedback.append(
                f"💡 Empfohlene Skill-Erweiterung: Vertiefen Sie Ihre Kenntnisse in: {missing_str}."
            )
        else:
            feedback.append("🔥 Alle geforderten Kernkompetenzen sind im Profil vorhanden!")

        if match_result["total_score"] >= 75.0:
            feedback.append("🚀 Exzellente Bewerbungschancen! Bereiten Sie Ihre Unterlagen (Lebenslauf & Anschreiben) vor.")
        else:
            feedback.append("📌 Tipp: Erstellen Sie ein kleines Praxisprojekt zu den fehlenden Skills auf GitHub.")

        return feedback