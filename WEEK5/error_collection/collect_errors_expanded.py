"""
Week 7 - Expanded Error Collector
Compiles all 240 sample programs and collects errors into CSV.
"""

import subprocess
import os
import csv
import re
from pathlib import Path
from collections import Counter

SAMPLE_DIR = "WEEK5/error_collection/sample_programs"
OUTPUT_CSV = "WEEK5/error_collection/output/collected_errors.csv"

CATEGORIES = {
    'missing_semicolon': 'Missing Semicolon',
    'undeclared': 'Undeclared Variable',
    'unmatched_braces': 'Unmatched Braces',
    'unmatched_parens': 'Unmatched Parentheses',
    'type_mismatch': 'Type Mismatch',
    'missing_return': 'Missing Return Statement',
    'invalid_decl': 'Invalid Syntax in Declarations',
    'missing_header': 'Missing Header Include'
}

def infer_category(filename):
    for key, cat in CATEGORIES.items():
        if key in filename.lower():
            return cat
    return 'Unknown'

def compile_and_capture(filepath):
    compiler = 'gcc' if filepath.suffix == '.c' else 'g++'
    try:
        result = subprocess.run(
            [compiler, '-c', str(filepath), '-o', '/dev/null', '-Wall'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return result.stderr
        # Also grab warnings even on success
        if result.stderr:
            return result.stderr
        return None
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {str(e)}"

def parse_errors(error_output, filepath, errors_list):
    pattern = r'([^:]+):(\d+):(\d+):\s*(error|warning):\s*(.+)'
    matches = re.finditer(pattern, error_output, re.MULTILINE)
    for match in matches:
        file, line, col, err_type, message = match.groups()
        errors_list.append({
            'source_file': filepath.name,
            'error_category': infer_category(filepath.name),
            'line_number': int(line),
            'column_number': int(col),
            'error_type': err_type,
            'error_message': message.strip(),
            'full_output': error_output.strip()
        })

def main():
    sample_files = list(Path(SAMPLE_DIR).glob('*.cpp')) + list(Path(SAMPLE_DIR).glob('*.c'))
    sample_files.sort()
    
    print(f"\n{'='*60}")
    print(f"  EXPANDED ERROR COLLECTION")
    print(f"{'='*60}")
    print(f"  Found {len(sample_files)} sample programs\n")
    
    errors = []
    success_count = 0
    
    for i, fp in enumerate(sample_files, 1):
        output = compile_and_capture(fp)
        if output and output not in ("TIMEOUT",) and not output.startswith("ERROR:"):
            parse_errors(output, fp, errors)
        else:
            success_count += 1
        
        if i % 40 == 0:
            print(f"  Progress: {i}/{len(sample_files)} files processed...")
    
    print(f"\n  Files with errors:   {len(sample_files) - success_count}")
    print(f"  Files compiled OK:   {success_count}")
    print(f"  Total error rows:    {len(errors)}")
    
    # Save CSV
    fieldnames = ['source_file','error_category','line_number','column_number',
                  'error_type','error_message','full_output']
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(errors)
    
    print(f"\n  ✔ Saved: {OUTPUT_CSV}")
    
    # Report
    cats = Counter(e['error_category'] for e in errors)
    print(f"\n{'='*60}")
    print("  BREAKDOWN BY CATEGORY")
    print(f"{'='*60}")
    for cat, count in sorted(cats.items()):
        pct = count / len(errors) * 100
        print(f"  {cat:<40} {count:>4} ({pct:5.1f}%)")
    print(f"{'='*60}\n")
    
    return errors

if __name__ == "__main__":
    main()
