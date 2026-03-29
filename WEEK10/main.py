import subprocess
import json
import joblib
import pandas as pd
import re

from fix_suggestions import get_fix_suggestion

# ================================
# LOAD MODEL + METADATA
# ================================

MODEL_PATH = "WEEK8/model_training/best_model.pkl"
FEATURE_COLUMNS_PATH = "WEEK8/model_training/feature_columns.json"
LABEL_MAP_PATH = "WEEK7/output/label_mapping.json"

model = joblib.load(MODEL_PATH)

with open(FEATURE_COLUMNS_PATH) as f:
    feature_cols = json.load(f)

with open(LABEL_MAP_PATH) as f:
    label_map = json.load(f)

# ================================
# STEP 1: COMPILE CODE
# ================================

def compile_code(file_path):
    compiler = "gcc" if file_path.endswith(".c") else "g++"

    result = subprocess.run(
        [compiler, "-c", file_path],
        capture_output=True,
        text=True
    )

    return result.stderr


# ================================
# STEP 2: PARSE ERROR
# ================================

def parse_error(error_output):
    pattern = r'(.+):(\d+):(\d+):\s*(error|warning):\s*(.+)'
    match = re.search(pattern, error_output)

    if match:
        return {
            "line": int(match.group(2)),
            "column": int(match.group(3)),
            "message": match.group(5)
        }
    return None


# ================================
# STEP 3: SIMPLE FEATURE EXTRACTION
# ================================

def extract_features(error):
    msg = error["message"].lower()

    features = {
        "line_number": error["line"],
        "column_number": error["column"],
        "msg_has_expected": int("expected" in msg),
        "msg_has_declared": int("declared" in msg),
        "msg_has_before": int("before" in msg),
        "msg_has_type": int("type" in msg),
        "msg_has_conversion": int("convert" in msg),
        "msg_has_return": int("return" in msg),
        "msg_has_control": int("control" in msg),
        "msg_has_implicit": int("implicit" in msg),
        "msg_has_unknown": int("unknown" in msg),
        "msg_mentions_semicolon": int(";" in msg),
        "msg_mentions_brace": int("{" in msg or "}" in msg),
        "msg_mentions_paren": int("(" in msg or ")" in msg),
        "msg_length": len(msg),
        "msg_word_count": len(msg.split()),

        # Dummy defaults (keep model happy)
        "code_length": 0,
        "code_ends_semicolon": 0,
        "code_has_declaration": 0,
        "code_open_braces": 0,
        "code_close_braces": 0,
        "code_open_parens": 0,
        "code_close_parens": 0,
        "code_has_assignment": 0,
        "code_has_comparison": 0,
        "code_has_string": 0,
        "brace_balance": 0,
        "paren_balance": 0,
        "total_braces": 0,
        "total_parens": 0
    }

    return pd.DataFrame([features])[feature_cols]


# ================================
# STEP 4: PREDICT ERROR TYPE
# ================================

def predict_error(features):
    pred = model.predict(features)[0]
    confidence = max(model.predict_proba(features)[0])

    label = label_map[str(pred)]
    return label, confidence


# ================================
# STEP 5: DISPLAY OUTPUT
# ================================

def display_output(error, label, confidence, suggestion):

    print("\n" + "="*60)
    print(" AI-ASSISTED COMPILER OUTPUT")
    print("="*60)

    print(f"\n Original Error:")
    print(f"  {error['message']}")

    print(f"\n Predicted Type: {label}")
    print(f" Confidence: {confidence*100:.2f}%")

    print("\n Explanation:")
    print(f"  {suggestion['explanation']}")

    print("\n Fix Steps:")
    for i, step in enumerate(suggestion['fix'], 1):
        print(f"  {i}. {step}")

    print("\n Example:")
    print(f"  Wrong:   {suggestion['example']['wrong']}")
    print(f"  Correct: {suggestion['example']['correct']}")

    print("="*60)


# ================================
# MAIN DRIVER
# ================================

def run_system(file_path):

    error_output = compile_code(file_path)

    if not error_output:
        print("✅ No errors. Code compiled successfully.")
        return

    error = parse_error(error_output)

    if not error:
        print("⚠️ Could not parse error.")
        print(error_output)
        return

    features = extract_features(error)
    label, confidence = predict_error(features)

    suggestion = get_fix_suggestion(label)

    display_output(error, label, confidence, suggestion)


# ================================
# ENTRY POINT
# ================================

if __name__ == "__main__":
    file_path = input("Enter C/C++ file path: ")
    run_system(file_path)