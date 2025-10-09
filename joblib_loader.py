import joblib
import json

def load_parsed_entities(joblib_path="resume_entities.joblib"):
    """
    Loads parsed resume entities from a saved joblib file.
    No dependency on Spacy or trained model.
    """
    try:
        data = joblib.load(joblib_path)
        print("✅ Loaded entities successfully!")
        print(json.dumps(data, indent=4))
        return data
    except Exception as e:
        print(f"❌ Error loading joblib file: {e}")
        return None


if __name__ == "__main__":
    # Test loader
    entities = load_parsed_entities("resume_entities.joblib")
