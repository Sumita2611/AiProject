import os
import logging
import google.generativeai as genai  # ✅ Corrected import
import pdfminer.high_level
import docx2txt
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

# ✅ Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# ✅ Configure Google Gemini API Key
genai.configure(api_key="AIzaSyDt0zEqI4kJPvA_LFPTBef5ZfWI-QoU5LA")  # Replace with your actual API key

# ✅ Define Upload Directory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create 'uploads' folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Setup Logging for Debugging
logging.basicConfig(level=logging.INFO)

# ✅ Resume Text Extraction Functions
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    return pdfminer.high_level.extract_text(pdf_path)

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX resume."""
    return docx2txt.process(docx_path)

# ✅ Helper Functions for Extracting Information from API Response
def extract_percentage(text):
    """Extract ATS match percentage from the response."""
    match = re.search(r'(\d+)%', text)
    return match.group(1) if match else "N/A"

def extract_missing_keywords(text):
    """Extract missing keywords from the response."""
    match = re.search(r'Missing Keywords: (.*)', text)
    return match.group(1).split(", ") if match else []

def extract_improvement_tips(text):
    """Extract improvement tips from the response."""
    match = re.search(r'Improvement Tips:\s*(.*)', text)
    return match.group(1).split(", ") if match else ["No improvement suggestions available."]

# ✅ Function to Analyze Resume with Google Gemini API
def analyze_resume_with_gemini(resume_text, job_description):
    """Analyze resume using Google Gemini API and extract ATS score, missing keywords, and improvement tips."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = """
    You are an ATS (Applicant Tracking System) expert. Compare the resume with the job description.
    1. Provide a percentage match as 'Match Score: XX%'.
    2. List missing keywords as 'Missing Keywords: keyword1, keyword2, keyword3'.
    3. Suggest 3-5 improvements as 'Improvement Tips: tip1, tip2, tip3'.
    Only provide these three points in your response.
    """

    try:
        response = model.generate_content([prompt, resume_text, job_description])
        response_text = response.text

        # ✅ Extract ATS match score, missing keywords, and improvement tips
        match_score = extract_percentage(response_text)
        missing_keywords = extract_missing_keywords(response_text)
        improvement_tips = extract_improvement_tips(response_text)

        return match_score, missing_keywords, improvement_tips

    except Exception as e:
        logging.error(f"Error with Gemini API: {e}")
        return "Error", [], ["Failed to process resume analysis."]

# ✅ Home Route
@app.route('/')
def home():
    return "Hello, ATS system is running!"

# ✅ Resume Processing API
@app.route('/process_resume', methods=['POST'])
def process_resume():
    try:
        # ✅ Validate Request
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resume or job description'}), 400

        resume_file = request.files['resume']
        job_description = request.form['job_description']

        # ✅ Validate File Selection
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # ✅ Save Uploaded File
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(resume_path)

        # ✅ Extract Resume Text
        if resume_file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_path)
        elif resume_file.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(resume_path)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        # ✅ Analyze Resume with Gemini API
        match_score, missing_keywords, improvement_tips = analyze_resume_with_gemini(resume_text, job_description)

        # ✅ Return the Analysis Results
        return jsonify({
            'match_score': match_score,
            'missing_keywords': missing_keywords,
            'improvement_tips': improvement_tips
        })

    except Exception as e:
        logging.error(f"Error processing resume: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)