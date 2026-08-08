from flask import Flask, render_template, request
from ausbildung_matcher import Applicant, AusbildungPosition, MatchingEngine

app = Flask(__name__)

POSITIONS = {
    "fiae": AusbildungPosition(
        title="Fachinformatiker für Anwendungsentwicklung",
        min_language="B2",
        required_skills=["python", "sql", "git", "logic & algorithms"],
        preferred_education="Abitur / IT-Studium"
    ),
    "fisi": AusbildungPosition(
        title="Fachinformatiker für Systemintegration",
        min_language="B2",
        required_skills=["networking", "linux", "hardware", "bash"],
        preferred_education="Abitur"
    )
}

@app.route('/')
def home():
    return render_template('index.html', positions=POSITIONS)

@app.route('/analyze', methods=['POST'])
def analyze():
    user_name = request.form.get('name')
    user_lang = request.form.get('language')
    user_edu = request.form.get('education')
    
    raw_skills = request.form.get('skills', '')
    user_skills = [s.strip() for s in raw_skills.split(',') if s.strip()]
    
    selected_pos_key = request.form.get('position')
    target_position = POSITIONS.get(selected_pos_key, POSITIONS["fiae"])

    applicant = Applicant(
        name=user_name,
        language_level=user_lang,
        education=user_edu,
        skills=user_skills
    )

    engine = MatchingEngine(applicant=applicant, position=target_position)
    match_result = engine.calculate_score()
    advices = engine.generate_feedback(match_result)

    return render_template(
        'result.html',
        applicant=applicant,
        position=target_position,
        result=match_result,
        advices=advices
    )

if __name__ == '__main__':
    app.run(debug=True)