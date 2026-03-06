import pandas as pd
import re
from pathlib import Path


#  SECTION 1: ERROR MESSAGE FEATURE EXTRACTION

def analyze_error_message(error_message):

    # Convert to lowercase for case-insensitive matching
    message = error_message.lower()
    
    # Feature 1-9: Keyword Detection
    has_expected   = 1 if 'expected' in message else 0
    has_declared   = 1 if ('declared' in message or 'undeclared' in message) else 0
    has_before     = 1 if 'before' in message else 0
    has_type       = 1 if 'type' in message else 0
    has_conversion = 1 if ('conversion' in message or 'convert' in message) else 0
    has_return     = 1 if 'return' in message else 0
    has_control    = 1 if 'control' in message else 0
    has_implicit   = 1 if 'implicit' in message else 0
    has_unknown    = 1 if 'unknown' in message else 0
    
    # Feature 10-12: Symbol Mentions
    mentions_semicolon = 1 if ("';'" in error_message or 'semicolon' in message) else 0
    mentions_brace     = 1 if ("'{'" in error_message or "'}'" in error_message or 'brace' in message) else 0
    mentions_paren     = 1 if ("'('" in error_message or "')'" in error_message or 'parenthes' in message) else 0
    
    # Feature 13-14: Message Statistics
    message_length = len(error_message)
    word_count     = len(error_message.split())
    
    return {
        'msg_has_expected':      has_expected,
        'msg_has_declared':      has_declared,
        'msg_has_before':        has_before,
        'msg_has_type':          has_type,
        'msg_has_conversion':    has_conversion,
        'msg_has_return':        has_return,
        'msg_has_control':       has_control,
        'msg_has_implicit':      has_implicit,
        'msg_has_unknown':       has_unknown,
        'msg_mentions_semicolon': mentions_semicolon,
        'msg_mentions_brace':    mentions_brace,
        'msg_mentions_paren':    mentions_paren,
        'msg_length':            message_length,
        'msg_word_count':        word_count,
    }


#  SECTION 2: SOURCE CODE READING
#
#  FIX: The original code hardcoded the path
#       '../WEEK5/error_collection/sample_programs'
#  which doesn't exist on most machines.
#  Now we search several candidate directories automatically.

_input_csv_path = 'output/collected_errors.csv'   # updated at runtime


def find_source_file(source_file):
    """Search for a source file in multiple candidate directories."""
    candidates = [
        Path(_input_csv_path).parent / source_file,           # same folder as CSV
        Path.cwd() / source_file,                              # current working dir
        Path.cwd() / 'sample_programs' / source_file,          # sample_programs sub-dir
        Path('../WEEK5/error_collection/sample_programs') / source_file,  # original path
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def read_code_line(source_file, line_number):
    try:
        file_path = find_source_file(source_file)
        if file_path is None:
            return ""                           # file simply not available — return empty

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if 1 <= line_number <= len(lines):
            return lines[line_number - 1].strip()
        return ""

    except Exception:
        return ""


#  SECTION 3: CODE CONTEXT FEATURE EXTRACTION

def analyze_code_line(source_file, line_number):
    code_line = read_code_line(source_file, line_number)

    if not code_line:
        return {
            'code_length': 0, 'code_ends_semicolon': 0,
            'code_has_declaration': 0, 'code_open_braces': 0,
            'code_close_braces': 0, 'code_open_parens': 0,
            'code_close_parens': 0, 'code_has_assignment': 0,
            'code_has_comparison': 0, 'code_has_string': 0,
        }

    length               = len(code_line)
    ends_with_semicolon  = 1 if code_line.endswith(';') else 0
    type_keywords        = r'\b(int|float|double|char|bool|void|long|short|string|unsigned|const)\b'
    has_declaration      = 1 if re.search(type_keywords, code_line) else 0
    open_braces          = code_line.count('{')
    close_braces         = code_line.count('}')
    open_parens          = code_line.count('(')
    close_parens         = code_line.count(')')
    has_assignment       = 1 if ('=' in code_line and '==' not in code_line) else 0
    comparison_operators = ['==', '!=', '<', '>', '<=', '>=']
    has_comparison       = 1 if any(op in code_line for op in comparison_operators) else 0
    has_string           = 1 if ('"' in code_line or "'" in code_line) else 0

    return {
        'code_length':          length,
        'code_ends_semicolon':  ends_with_semicolon,
        'code_has_declaration': has_declaration,
        'code_open_braces':     open_braces,
        'code_close_braces':    close_braces,
        'code_open_parens':     open_parens,
        'code_close_parens':    close_parens,
        'code_has_assignment':  has_assignment,
        'code_has_comparison':  has_comparison,
        'code_has_string':      has_string,
    }


#  SECTION 4: STRUCTURAL FEATURE CALCULATION

def calculate_balance_features(code_features):
    return {
        'brace_balance': code_features['code_open_braces']  - code_features['code_close_braces'],
        'paren_balance': code_features['code_open_parens']  - code_features['code_close_parens'],
        'total_braces':  code_features['code_open_braces']  + code_features['code_close_braces'],
        'total_parens':  code_features['code_open_parens']  + code_features['code_close_parens'],
    }


#  SECTION 5: MAIN FEATURE EXTRACTION PIPELINE

def extract_features_for_one_error(error_row):
    message_features = analyze_error_message(error_row['error_message'])
    code_features    = analyze_code_line(error_row['source_file'], error_row['line_number'])
    balance_features = calculate_balance_features(code_features)

    return {
        'source_file':    error_row['source_file'],
        'error_category': error_row['error_category'],
        'line_number':    error_row['line_number'],
        'column_number':  error_row['column_number'],
        **message_features,
        **code_features,
        **balance_features,
    }


def extract_features_for_all_errors(input_csv, output_csv):
    global _input_csv_path
    _input_csv_path = input_csv          # let find_source_file know where the CSV is

    print("\n" + "="*70)
    print("  FEATURE EXTRACTION STARTED")
    print("="*70 + "\n")

    # STEP 1: Load errors
    print("Loading collected errors...")
    errors_df = pd.read_csv(input_csv)
    print(f"   Loaded {len(errors_df)} errors\n")

    # STEP 2: Count how many source files we can actually locate
    unique_files  = errors_df['source_file'].unique()
    found_files   = [f for f in unique_files if find_source_file(f) is not None]
    missing_files = [f for f in unique_files if find_source_file(f) is None]

    print(f"   Source files found   : {len(found_files)}/{len(unique_files)}")
    if missing_files:
        print(f"   Source files missing : {len(missing_files)} (code-line features will be 0 for these)")
    print()

    # STEP 3: Extract features
    print("Extracting features...")
    all_features = []
    for index, error_row in errors_df.iterrows():
        if (index + 1) % 20 == 0:
            print(f"   Progress: {index + 1}/{len(errors_df)} errors processed...")
        all_features.append(extract_features_for_one_error(error_row))

    print(f"   Extracted features for all {len(all_features)} errors\n")

    # STEP 4: Save
    print("Saving features to CSV...")
    features_df = pd.DataFrame(all_features)
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    features_df.to_csv(output_csv, index=False)
    print(f"   Saved to: {output_csv}\n")

    # STEP 5: Summary
    print("="*70)
    print("  FEATURE EXTRACTION COMPLETE!")
    print("="*70)
    print(f"\nDataset Summary:")
    print(f"   Total Samples : {len(features_df)}")
    print(f"   Total Columns : {len(features_df.columns)}")
    print(f"   ML Features   : {len(features_df.columns) - 4}")
    print(f"\nOutput File: {output_csv}")
    print("="*70 + "\n")


#  SECTION 6: RUN THE PROGRAM

if __name__ == "__main__":
    INPUT_FILE  = 'output/collected_errors.csv'
    OUTPUT_FILE = 'output/features_dataset.csv'
    extract_features_for_all_errors(INPUT_FILE, OUTPUT_FILE)