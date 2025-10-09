# =============================
# 📦 Block 1: Setup & Imports
# =============================

import os
import re
import spacy
import joblib
import fitz  # PyMuPDF
import unicodedata
import pytesseract
from PIL import Image
from pathlib import Path
from docx import Document
from rapidfuzz import process

print("✅ All libraries imported successfully.")

# =============================
# 📄 Block 2: Text Extraction + Cleaning
# =============================

# -------- PDF Extraction --------
def text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text_blocks = [page.get_text("text") for page in doc]
    return "\n".join(text_blocks)

# -------- DOCX Extraction --------
def text_from_docx(path: str) -> str:
    doc = Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)

# -------- Image (OCR) Extraction --------
def text_from_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)

# -------- TXT Extraction --------
def text_from_txt(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")

# -------- Unified Extractor --------
def extract_text(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return text_from_pdf(path)
    elif ext == ".docx":
        return text_from_docx(path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return text_from_image(path)
    elif ext == ".txt":
        return text_from_txt(path)
    else:
        raise ValueError(f"❌ Unsupported file type: {ext}")


# -------- Cleaning Function --------
def clean_resume_text(text):
    """
    Cleans extracted resume text to make it model-ready.
    Fixes spacing, normalization, and unwanted artifacts.
    """

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Fix cases like 'A N I S' → 'ANIS'
    text = re.sub(r'(?<=\b[A-Z])(?:\s(?=[A-Z]\b))+', '', text)

    # Fix random double spaces → single space
    text = re.sub(r'\s{2,}', ' ', text)

    # Fix broken lines like "P R O J E C T S" → "PROJECTS"
    text = re.sub(r'(\b[A-Z]\s){2,}[A-Z]\b', lambda m: m.group(0).replace(' ', ''), text)

    # Preserve proper newlines between sections
    text = re.sub(r'(\n\s*){2,}', '\n\n', text)

    # Remove extra symbols or underscores
    text = re.sub(r'[_•·●◆▶-]+', '', text)

    # Strip trailing/leading whitespace
    text = text.strip()

    return text

print("✅ Text extraction and cleaning functions are ready.")


resume_text = extract_text("Arman Resume 2025.pdf")
clean_text = clean_resume_text(resume_text)
print(clean_text[:500])


import re

def fix_broken_spacing_v2(text: str) -> str:
    """
    Final version — repairs PDFs with broken or glued text:
    - Fixes spaced letters ("M A C H I N E" -> "MACHINE")
    - Preserves valid spaces ("Machine Learning")
    - Restores emails and city names
    """
    # Step 1: Remove extra spaces but keep structure
    text = re.sub(r'\s{2,}', ' ', text)

    # Step 2: Fix all-caps split words: "D A T A" → "DATA"
    text = re.sub(r'(?<=\b)(?:[A-Z]\s){2,}[A-Z]\b', lambda m: m.group(0).replace(" ", ""), text)

    # Step 3: Fix mixed-case split words: "M a c h i n e" → "Machine"
    text = re.sub(r'(?<=\b)(?:[A-Za-z]\s){2,}[A-Za-z]\b', lambda m: m.group(0).replace(" ", ""), text)

    # Step 4: Fix emails like "a n i s @ g m a i l . c o m"
    text = re.sub(r'((?:[a-zA-Z0-9]\s?)+@\s?(?:[a-zA-Z]\s?)+\.\s?(?:[a-zA-Z]{2,}))',
                  lambda m: m.group(0).replace(" ", ""), text)

    # Step 5: Fix phone numbers with spaces
    text = re.sub(r'(\+?\d[\d\s\-]{8,}\d)', lambda m: re.sub(r'\s+', '', m.group(0)), text)

    # Step 6: Fix cities/states like "M a h a r a s t r a" → "Maharastra"
    text = re.sub(r'(?<=\b)(?:[A-Za-z]\s){2,}[A-Za-z]\b', lambda m: m.group(0).replace(" ", ""), text)

    # Step 7: Normalize punctuation and remove artifacts
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    text = re.sub(r'[_•·●◆▶-]+', '', text)

    # Step 8: Final cleanup
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


print(fix_broken_spacing_v2(clean_text))


import re
import spacy
from rapidfuzz import process

# ===============================
# 📌 Load lightweight SpaCy model for PERSON detection
# ===============================
nlp_name = spacy.load("en_core_web_sm")

# ===============================
# 📌 Predefined Skills Database
# ===============================
SKILLS_DB = [
    "Java","Spring Boot","Python","C++","C#","JavaScript","TypeScript","HTML","CSS","React","Angular","Vue.js",
    "Node.js","Express.js","Django","Flask","REST","GraphQL","Microservices","SQL","MySQL","PostgreSQL","MongoDB",
    "Oracle","SQLite","Redis","Docker","Kubernetes","Jenkins","Git","GitHub","Bitbucket","GitLab","AWS","Azure",
    "Google Cloud","Linux","CI/CD","Agile","Machine Learning","Deep Learning","TensorFlow","PyTorch","Pandas",
    "NumPy","Scikit-learn","Hadoop","Spark","Tableau","Power BI","Streamlit","Seaborn","Matplotlib","Data Science"
]

# ===============================
# 📌 City/State Database
# ===============================
CITIES_AND_STATES = [
    "Mumbai","Pune","Delhi","Bengaluru","Chennai","Hyderabad","Kolhapur","Mohol","Solapur","Nashik","Nagpur","Goa",
    "Thane","Aurangabad","Ahmedabad","Indore","Jaipur","Kolkata","Surat","Lucknow","Ranchi","Bhopal","Patna","Kanpur",
    "Vadodara","Noida","Gurgaon","Chandigarh","Coimbatore","Vizag","Maharashtra","Maharastra","Karnataka","Gujarat",
    "Tamil Nadu","Telangana","West Bengal","Rajasthan","Madhya Pradesh","Uttar Pradesh","Punjab","Haryana","Odisha",
    "Kerala","Assam","Ichalkaranji","Jaysingpur","Sangli"
]

# ===============================
# 📌 Fuzzy Location Matcher
# ===============================
def get_best_location(text):
    lines = [line for line in text.split("\n") if "," in line or "|" in line]
    combined = " ".join(lines) if lines else text
    result = process.extractOne(combined, CITIES_AND_STATES, score_cutoff=70)
    return result[0] if result else None


# ===============================
# 📌 Rule-Based Extraction (with improved name)
# ===============================
def extract_rule_based(text: str) -> dict:
    extracted = {}

     # ---- Improved Name Extraction (via SpaCy PERSON entity) ----
    doc = nlp_name(text)
    NAME_BLACKLIST = {"ENGINEER", "DEVELOPER", "PROJECT", "MANAGER", "SUMMARY"}
    top_lines = text.strip().split("\n")[:5]

    persons = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    for p in persons:
        if any(b in p.upper() for b in NAME_BLACKLIST):
            continue
        if 1 <= len(p.split()) <= 3:  # allow up to 3-word names
            for line in top_lines:
                if p in line:
                    extracted["name"] = p
                    break
        if extracted.get("name"):
            break
    if not extracted.get("name") and persons:
        extracted["name"] = persons[0]  # fallback

    # ---- Phone ----
    phone_pattern = r"(\+?\d{1,3}[\s-]?\d{5}[\s-]?\d{5}|\+?\d{1,3}[\s-]?\d{10}|\d{10})"
    phones = re.findall(phone_pattern, text)
    extracted["phone"] = phones[0] if phones else None

    # ---- Email ----
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    extracted["email"] = emails[0] if emails else None

    # ---- LinkedIn ----
    linkedin_pattern = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/[A-Za-z0-9\/\-\_]+"
    linkedin = re.findall(linkedin_pattern, text)
    extracted["linkedin"] = linkedin[0] if linkedin else None

    # ---- GitHub ----
    github_pattern = r"(?:https?:\/\/)?(?:www\.)?github\.com\/[A-Za-z0-9\/\-\_]+"
    github = re.findall(github_pattern, text)
    extracted["github"] = github[0] if github else None

    # ---- Skills ----
    found_skills = [skill for skill in SKILLS_DB if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]
    extracted["skills"] = sorted(set(found_skills))

    # ---- Years of Experience ----
    yoe_pattern = r"(\d+\+?\s*(?:years|yrs))"
    yoe_match = re.search(yoe_pattern, text, re.IGNORECASE)
    extracted["yoe"] = yoe_match.group(1) if yoe_match else None

   
    # ---- Fuzzy Location ----
    location = get_best_location(text)
    extracted["location"] = location

    return extracted

print("🔍 Extracted Entities:")
print(extract_rule_based(clean_text))



import joblib

# ===============================
# 📌 Run extraction on example resume text
# ===============================
sample_text = """
Anis Shaikh
Machine Learning Engineer
Mohol Maharastra | anis.shaikh@example.com | +91 98765 43210
LinkedIn | GitHub
Bachelor of Technology in Artificial Intelligence and Data Science (CGPA: 8.50)
Graduation Year: 2026
"""

# Extract structured entities
extracted_data = extract_rule_based(clean_text)

print("🔍 Final Refined Entities:")
print(extracted_data)

# ===============================
# 📦 Save as Joblib file for later use
# ===============================
joblib.dump(extracted_data, "resume_entities.joblib")
print("✅ Saved parsed entities to resume_entities.joblib")


import joblib

# ===============================
# 📂 Load the saved joblib file
# ===============================
loaded_entities = joblib.load("resume_entities.joblib")

print("📦 Loaded Entities from Joblib:")
for key, value in loaded_entities.items():
    print(f"{key}: {value}")
