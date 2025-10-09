import streamlit as st
import joblib
import re
from pathlib import Path
from docx import Document
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from rapidfuzz import process
import os
import importlib

# ===============================
# 📌 City/State Reference
# ===============================
CITIES_AND_STATES = [
    "Mumbai", "Pune", "Delhi", "Bengaluru", "Chennai", "Hyderabad",
    "Kolhapur", "Mohol", "Solapur", "Nashik", "Nagpur", "Goa", "Thane",
    "Aurangabad", "Ahmedabad", "Indore", "Jaipur", "Kolkata", "Surat",
    "Lucknow", "Ranchi", "Bhopal", "Patna", "Kanpur", "Vadodara",
    "Noida", "Gurgaon", "Chandigarh", "Coimbatore", "Vizag",
    "Maharashtra", "Maharastra", "Karnataka", "Gujarat", "Tamil Nadu",
    "Telangana", "West Bengal", "Rajasthan", "Madhya Pradesh", "Goa",
    "Uttar Pradesh", "Punjab", "Haryana", "Odisha", "Kerala", "Assam"
]

def get_best_location(text):
    result = process.extractOne(text, CITIES_AND_STATES, score_cutoff=70)
    return result[0] if result else None

# ===============================
# 📘 Text Extractors
# ===============================
def text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join(page.get_text("text") for page in doc)

def text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

def text_from_txt(path):
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def text_from_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_text(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return text_from_pdf(file_path)
    elif ext == ".docx":
        return text_from_docx(file_path)
    elif ext == ".txt":
        return text_from_txt(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return text_from_image(file_path)
    else:
        st.error("Unsupported file type.")
        return ""

# ===============================
# 📋 Rule-Based Entity Extraction
# ===============================
SKILLS_LIST = [
    "Python","Java","C++","SQL","Power BI","Tableau",
    "Machine Learning","Data Science","React","Node.js","Django","Flask",
    "CSS","HTML","JavaScript","Pandas","NumPy","Matplotlib","Seaborn","MongoDB","MySQL"
]

def extract_entities(text):
    entities = {
        "Name": None, "Email": None, "Phone": None,
        "Skills": [], "YOE": None, "URLs": [], "Location": None,
        "Projects": []
    }

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
    if email_match:
        entities["Email"] = email_match.group()

    # Phone
    phone_match = re.search(r"\+?\d[\d\-\s]{8,}\d", text)
    if phone_match:
        entities["Phone"] = re.sub(r"\s+", "", phone_match.group())

    # URLs
    urls = re.findall(r"https?://[^\s]+", text)
    if urls:
        entities["URLs"] = urls

    # Skills
    skills = [s for s in SKILLS_LIST if re.search(rf"\b{s}\b", text, re.I)]
    if skills:
        entities["Skills"] = sorted(set(skills))

    # Years of experience
    yoe_match = re.search(r"(\d+\+?\s*(?:years|yrs))", text, re.IGNORECASE)
    if yoe_match:
        entities["YOE"] = yoe_match.group(1)

    # Location
    loc = get_best_location(text)
    if loc:
        entities["Location"] = loc

    # Name → first line guess
    first_line = text.strip().split("\n")[0] if text.strip() else ""
    name_match = re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*", first_line)
    if name_match:
        entities["Name"] = name_match.group()

    # Projects
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if re.search(r'\b(project|major project|minor project)\b', line, re.IGNORECASE):
            proj_name = re.sub(r'(?i).*project[:\-]?\s*', '', line).split("(")[0].strip(" -:•")
            tech_stack = [s for s in SKILLS_LIST if re.search(rf"\b{s}\b", line, re.I)]
            nearby = " ".join(lines[i+1:i+3])
            tech_stack += [s for s in SKILLS_LIST if re.search(rf"\b{s}\b", nearby, re.I)]
            tech_stack = sorted(set(tech_stack))
            entities["Projects"].append({"name": proj_name or None, "tech_stack": tech_stack or None})

    return entities

# ===============================
# 📦 Load & Save Joblib
# ===============================
def save_joblib(data, filename="resume_entities.joblib"):
    joblib.dump(data, filename)
    st.success(f"✅ Saved entities to `{filename}`")

def load_joblib(uploaded_file):
    try:
        if hasattr(uploaded_file, "read"):
            tmp = f"./tmp_uploaded_{uploaded_file.name}"
            with open(tmp, "wb") as f:
                f.write(uploaded.getvalue())
            data = joblib.load(tmp)
            try: os.remove(tmp)
            except: pass
        else:
            data = joblib.load(uploaded_file)
        st.success("✅ Loaded existing Joblib file.")
        return data
    except Exception as e:
        st.error(f"❌ Failed to load joblib: {e}")
        return {}

# ===============================
# 🚀 Try to load ML model if present
# ===============================
def try_load_model():
    candidates = ["resume_classifier.joblib", "svc_model.pkl", "model.joblib", "model.pkl"]
    for c in candidates:
        if os.path.exists(c):
            try:
                mdl = joblib.load(c)
                return mdl, c
            except Exception:
                import pickle
                try:
                    with open(c, "rb") as f:
                        mdl = pickle.load(f)
                    return mdl, c
                except Exception:
                    continue
    return None, None

# ===============================
# 🚀 Streamlit App UI (same structure)
# ===============================
st.set_page_config(page_title="Resume Parser", page_icon="📄", layout="wide")
st.title("📄Intelligent Job Tracker and Analyzer")
st.write("Upload your resume once → extract → save → reuse joblib forever!")

model, model_file = try_load_model()
if model:
    st.info(f"🔎 Model found and loaded from `{model_file}`", icon="🔧")

uploaded = st.file_uploader(
    "📁 Upload Resume or Joblib",
    type=["pdf", "docx", "txt", "jpg", "png", "joblib"],
    key="resume_uploader"
)

if uploaded:
    file_ext = Path(uploaded.name).suffix.lower()

    if file_ext == ".joblib":
        entities = load_joblib(uploaded)
        st.subheader("🔍 Loaded Entities (from joblib)")
        st.json(entities)

    else:
        temp_path = f"./temp_{uploaded.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getvalue())
        st.success("✅ File uploaded successfully!")

        resume_text = extract_text(temp_path)
        if not resume_text.strip():
            st.error("❌ Could not extract text from file.")
            try: os.remove(temp_path)
            except: pass
            st.stop()

        st.subheader("📘 Extracted Text Preview")
        st.text_area("Extracted Resume Text", resume_text[:1500], height=250)

        entities = {}
        predicted_category = None
        if model:
            try:
                pred = model.predict([resume_text])
                predicted_category = pred[0] if hasattr(pred, "__len__") else pred
            except Exception:
                predicted_category = None

        try:
            parsed = extract_entities(resume_text)
            entities = parsed
        except Exception as e:
            entities = {}
            st.error(f"Error while extracting entities: {e}")

        if predicted_category:
            st.subheader("🏷️ Predicted Category")
            st.write(predicted_category)

        st.subheader("🔍 Extracted Entities (Auto)")
        st.json(entities)

        save_joblib(entities)

        try: os.remove(temp_path)
        except: pass

    st.subheader("✏️ Edit / Fill Missing Fields")
    edited = {}
    cols = st.columns(2)
    with cols[0]:
        edited["Name"] = st.text_input("Full Name", entities.get("Name", ""), key="edit_name")
        edited["Email"] = st.text_input("Email", entities.get("Email", ""), key="edit_email")
        edited["Phone"] = st.text_input("Phone", entities.get("Phone", ""), key="edit_phone")
        edited["Location"] = st.text_input("Location (optional)", entities.get("Location", ""), key="edit_location")
    with cols[1]:
        edited["YOE"] = st.text_input("Years of Experience", entities.get("YOE", ""), key="edit_yoe")
        skills_str = ", ".join(entities.get("Skills", []))
        edited["Skills"] = [s.strip() for s in st.text_area("Skills (comma separated)", skills_str, key="edit_skills").split(",") if s.strip()]
        urls_str = "\n".join(entities.get("URLs", []))
        edited["URLs"] = [u.strip() for u in st.text_area("URLs (LinkedIn, GitHub, etc.)", urls_str, key="edit_urls").split("\n") if u.strip()]

    st.subheader("📂 Projects")
    projects_list = entities.get("Projects", []) or []
    edited_projects = []
    for i, proj in enumerate(projects_list):
        with st.expander(f"Project {i+1}", expanded=False):
            proj_name = st.text_input(f"Project Name {i+1}", proj.get("name") or proj.get("Project Name", ""), key=f"proj_name_{i}")
            tech_stack_str = ", ".join(proj.get("tech_stack") or proj.get("Tech Stack", []) or [])
            tech_stack = [s.strip() for s in st.text_area(f"Tech Stack {i+1}", tech_stack_str, key=f"proj_tech_{i}").split(",") if s.strip()]
            edited_projects.append({"Project Name": proj_name, "Tech Stack": tech_stack})

    edited["Projects"] = edited_projects

    if st.button("💾 Save Final Joblib", key="save_final"):
        save_joblib(edited)
        st.success("✅ Final entities saved successfully!")
        st.json(edited)

else:
    st.info("⬆️ Upload a Resume (`pdf`, `docx`, `txt`, `jpg`, `png`) or existing `.joblib` file.")
