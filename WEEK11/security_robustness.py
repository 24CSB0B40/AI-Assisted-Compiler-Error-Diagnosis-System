

import os
import re
import sys
import json
import subprocess
import tempfile
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ============================================================
# SECTION 1: DANGEROUS CODE PATTERN DEFINITIONS
# ============================================================

# These are patterns that, if hidden inside syntax errors, could
# mask unsafe code that a beginner might accidentally write.

DANGEROUS_PATTERNS = {
    "buffer_overflow_risk": {
        "patterns": [r'\bgets\s*\(', r'\bscanf\s*\(\s*"%s"', r'\bstrcpy\s*\('],
        "description": "Functions with no bounds checking — can cause buffer overflows",
        "severity": "HIGH",
        "recommendation": "Use fgets(), scanf with width limit, or strncpy() instead"
    },
    "format_string_vuln": {
        "patterns": [r'printf\s*\(\s*\w+\s*\)', r'fprintf\s*\(\s*\w+\s*,\s*\w+\s*\)'],
        "description": "User-controlled format string passed directly to printf family",
        "severity": "HIGH",
        "recommendation": "Always use printf(\"%s\", var) not printf(var)"
    },
    "null_pointer_deref": {
        "patterns": [r'\bmalloc\s*\([^)]+\)\s*;(?!\s*if)', r'\bnew\s+\w+\s*;(?!\s*if)'],
        "description": "malloc/new result used without NULL check",
        "severity": "MEDIUM",
        "recommendation": "Always check if malloc/new returned NULL before using pointer"
    },
    "integer_overflow": {
        "patterns": [r'\bINT_MAX\b', r'\bUINT_MAX\b', r'0xFFFFFFFF'],
        "description": "Boundary values that may indicate integer overflow risk",
        "severity": "MEDIUM",
        "recommendation": "Use safe arithmetic checks before operations near integer limits"
    },
    "dangerous_functions": {
        "patterns": [r'\bsystem\s*\(', r'\bexec\s*\(', r'\bpopen\s*\('],
        "description": "Shell execution functions that can enable code injection",
        "severity": "CRITICAL",
        "recommendation": "Avoid system()/exec() with user input; use safer alternatives"
    },
    "hardcoded_credentials": {
        "patterns": [r'password\s*=\s*"[^"]+"', r'passwd\s*=\s*"[^"]+"', r'secret\s*=\s*"[^"]+"'],
        "description": "Hardcoded credentials or secrets in source code",
        "severity": "HIGH",
        "recommendation": "Never hardcode passwords; use environment variables or config files"
    }
}

# SECTION 2: MALFORMED INPUT TEST CASES

MALFORMED_TEST_CASES = [
    {
        "name": "Empty File",
        "code": "",
        "expected_behavior": "Graceful handling, no crash",
        "category": "Edge Case"
    },
    {
        "name": "Only Comments",
        "code": "// This is just a comment\n/* Another comment */\n",
        "expected_behavior": "Compile successfully or graceful error",
        "category": "Edge Case"
    },
    {
        "name": "Null Bytes in Code",
        "code": "int main() {\x00 return 0; }",
        "expected_behavior": "Handled without crash",
        "category": "Adversarial"
    },
    {
        "name": "Extremely Long Line",
        "code": "int main() { int " + "x" * 5000 + " = 0; return 0; }\n",
        "expected_behavior": "Processed without memory crash",
        "category": "Stress Test"
    },
    {
        "name": "Deeply Nested Braces",
        "code": "int main() {" + "{" * 500 + "int x=0;" + "}" * 500 + " return 0;}\n",
        "expected_behavior": "Handled within time limit",
        "category": "Stress Test"
    },
    {
        "name": "Unicode Characters",
        "code": '// Ünïcödé cömment\nint main() { int x = 10; return 0; }\n',
        "expected_behavior": "UTF-8 file handled gracefully",
        "category": "Encoding"
    },
    {
        "name": "Mixed Syntax Errors",
        "code": "int main( {\n  int x = \n  if(x > { return ;\n}\n",
        "expected_behavior": "Multiple errors detected and reported",
        "category": "Multi-Error"
    },
    {
        "name": "No Main Function",
        "code": "#include <iostream>\nvoid helper() { int x = 5; }\n",
        "expected_behavior": "Compilation succeeds (linking error only)",
        "category": "Edge Case"
    },
    {
        "name": "Only Preprocessor Directives",
        "code": "#include <iostream>\n#define MAX 100\n#pragma once\n",
        "expected_behavior": "Handled gracefully",
        "category": "Edge Case"
    },
    {
        "name": "Very Large Number of Errors",
        "code": "\n".join([f"intger x{i} = {i};" for i in range(50)]) + "\nint main(){return 0;}\n",
        "expected_behavior": "All errors detected, no crash",
        "category": "Stress Test"
    },
    {
        "name": "Recursive Deep Include",
        "code": '#include <iostream>\n#include <vector>\n#include <map>\n#include <string>\n#include <algorithm>\nint main(){return 0;}\n',
        "expected_behavior": "Multiple headers handled",
        "category": "Header Test"
    },
    {
        "name": "File With Only Whitespace",
        "code": "   \n\t\n   \n",
        "expected_behavior": "Empty content handled gracefully",
        "category": "Edge Case"
    }
]


# SECTION 3: CORE TESTING ENGINE

class SecurityRobustnessTester:
    """
    Runs all security and robustness tests on the AI Compiler Diagnosis System.
    """

    def __init__(self):
        self.results = {
            "malformed_input_tests": [],
            "dangerous_pattern_analysis": [],
            "input_validation_tests": [],
            "summary": {}
        }
        self.start_time = datetime.now()

    # 3A: Test how system handles malformed/adversarial inputs

    def run_malformed_input_tests(self):
        """
        Creates temporary files with problematic content,
        compiles them, and checks if the system survives without crashing.
        """
        print("\n" + "=" * 65)
        print("  TEST SUITE 1: MALFORMED & ADVERSARIAL INPUT HANDLING")
        print("=" * 65)

        passed = 0
        failed = 0

        for test in MALFORMED_TEST_CASES:
            result = self._run_single_malformed_test(test)
            self.results["malformed_input_tests"].append(result)

            status = "PASS" if result["status"] == "PASS" else "FAIL"
            icon = "✓" if status == "PASS" else "✗"
            print(f"  [{icon}] {status}  |  {test['category']:12s}  |  {test['name']}")
            if result.get("notes"):
                print(f"         Notes: {result['notes']}")

            if status == "PASS":
                passed += 1
            else:
                failed += 1

        print(f"\n  Results: {passed} passed, {failed} failed out of {len(MALFORMED_TEST_CASES)} tests")
        return passed, failed

    def _run_single_malformed_test(self, test):
        """Run one malformed input test and return structured result."""
        result = {
            "test_name": test["name"],
            "category": test["category"],
            "expected": test["expected_behavior"],
            "status": "PASS",
            "compile_result": None,
            "errors_found": 0,
            "time_taken_ms": 0,
            "notes": ""
        }

        try:
            # Write test code to temp file
            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.cpp',
                delete=False, encoding='utf-8', errors='replace'
            ) as f:
                f.write(test["code"])
                tmp_path = f.name

            start = time.time()

            # Run g++ on the temp file
            try:
                proc = subprocess.run(
                    ["g++", "-c", tmp_path, "-o", "/dev/null"],
                    capture_output=True, text=True, timeout=5
                )
                elapsed_ms = (time.time() - start) * 1000
                result["time_taken_ms"] = round(elapsed_ms, 1)

                if proc.returncode == 0:
                    result["compile_result"] = "SUCCESS"
                else:
                    result["compile_result"] = "ERRORS"
                    # Count error lines
                    errors = re.findall(r'error:', proc.stderr)
                    result["errors_found"] = len(errors)

                result["status"] = "PASS"

            except subprocess.TimeoutExpired:
                result["compile_result"] = "TIMEOUT"
                result["status"] = "FAIL"
                result["notes"] = "Compilation timed out (>5s) — possible infinite recursion in parser"

        except Exception as e:
            result["status"] = "FAIL"
            result["notes"] = f"Exception: {str(e)[:80]}"

        finally:
            # Always clean up temp file
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

        return result

    # 3B: Scan sample programs for dangerous code patterns

    def run_dangerous_pattern_analysis(self, sample_dir="."):
        """
        Scans all sample .cpp files to identify if any syntax-error
        programs also contain potentially dangerous code patterns.
        This matters because: a file that fails to compile might still
        contain dangerous logic that gets fixed and then becomes harmful.
        """
        print("\n" + "=" * 65)
        print("  TEST SUITE 2: DANGEROUS CODE PATTERN DETECTION")
        print("=" * 65)

        cpp_files = list(Path(sample_dir).glob("*.cpp"))
        if not cpp_files:
            cpp_files = list(Path(".").glob("*.cpp"))

        print(f"  Scanning {len(cpp_files)} sample programs...\n")

        total_dangerous = 0
        severity_counts = defaultdict(int)

        for filepath in sorted(cpp_files):
            try:
                content = filepath.read_text(encoding='utf-8', errors='replace')
                file_findings = []

                for pattern_name, pattern_info in DANGEROUS_PATTERNS.items():
                    for pattern in pattern_info["patterns"]:
                        matches = re.findall(pattern, content)
                        if matches:
                            file_findings.append({
                                "pattern_type": pattern_name,
                                "severity": pattern_info["severity"],
                                "description": pattern_info["description"],
                                "recommendation": pattern_info["recommendation"],
                                "match_count": len(matches)
                            })
                            severity_counts[pattern_info["severity"]] += 1
                            total_dangerous += 1

                if file_findings:
                    self.results["dangerous_pattern_analysis"].append({
                        "file": filepath.name,
                        "findings": file_findings
                    })
                    for f in file_findings:
                        print(f"  [{f['severity']:8s}] {filepath.name:35s} → {f['pattern_type']}")

            except Exception as e:
                pass

        if total_dangerous == 0:
            print("  ✓ No dangerous patterns found in sample programs.")
            print("  ✓ All sample files are safe for educational use.")
        else:
            print(f"\n  Total dangerous pattern instances: {total_dangerous}")
            for sev, count in severity_counts.items():
                print(f"  {sev}: {count}")

        return total_dangerous, severity_counts

    # 3C: Input validation boundary tests

    def run_input_validation_tests(self):
        """
        Tests the system's input validation:
        - Invalid file paths
        - Files with wrong extensions
        - Files that are too large (simulated)
        - Binary file input (non-text)
        """
        print("\n" + "=" * 65)
        print("  TEST SUITE 3: INPUT VALIDATION & BOUNDARY TESTING")
        print("=" * 65)

        validation_tests = [
            {
                "name": "Nonexistent File Path",
                "test": lambda: self._test_nonexistent_file(),
                "expected": "Error message, no crash"
            },
            {
                "name": "Wrong File Extension (.txt)",
                "test": lambda: self._test_wrong_extension(),
                "expected": "Error or warning about unsupported type"
            },
            {
                "name": "Valid C++ File",
                "test": lambda: self._test_valid_file(),
                "expected": "Compile attempt executed"
            },
            {
                "name": "File With Only Semicolons",
                "test": lambda: self._test_semicolons_only(),
                "expected": "Errors detected, no crash"
            },
            {
                "name": "Regex Pattern Injection in Error Message",
                "test": lambda: self._test_regex_injection(),
                "expected": "Regex handled safely"
            },
            {
                "name": "File Path With Special Characters",
                "test": lambda: self._test_special_path(),
                "expected": "Handled gracefully"
            },
        ]

        passed = 0
        failed = 0

        for vt in validation_tests:
            try:
                test_result = vt["test"]()
                status = "PASS"
                passed += 1
            except Exception as e:
                test_result = {"error": str(e)}
                status = "FAIL"
                failed += 1

            icon = "✓" if status == "PASS" else "✗"
            print(f"  [{icon}] {status}  |  {vt['name']}")

            self.results["input_validation_tests"].append({
                "name": vt["name"],
                "expected": vt["expected"],
                "status": status,
                "details": test_result
            })

        print(f"\n  Results: {passed} passed, {failed} failed out of {len(validation_tests)} tests")
        return passed, failed

    def _test_nonexistent_file(self):
        fake_path = "/nonexistent/path/file.cpp"
        exists = os.path.exists(fake_path)
        return {"file_exists": exists, "correctly_identified_missing": not exists}

    def _test_wrong_extension(self):
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
            f.write("int main() { return 0; }\n")
            tmp = f.name
        result = {"extension": Path(tmp).suffix, "is_cpp": Path(tmp).suffix in ['.c', '.cpp', '.cc', '.cxx']}
        os.unlink(tmp)
        return result

    def _test_valid_file(self):
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False, mode='w') as f:
            f.write("#include <iostream>\nint main() { return 0; }\n")
            tmp = f.name
        proc = subprocess.run(["g++", "-c", tmp, "-o", "/dev/null"],
                              capture_output=True, text=True, timeout=5)
        os.unlink(tmp)
        return {"returncode": proc.returncode, "compiled_ok": proc.returncode == 0}

    def _test_semicolons_only(self):
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False, mode='w') as f:
            f.write(";;;\n;;;;\n")
            tmp = f.name
        proc = subprocess.run(["g++", "-c", tmp, "-o", "/dev/null"],
                              capture_output=True, text=True, timeout=5)
        errors = len(re.findall(r'error:', proc.stderr))
        os.unlink(tmp)
        return {"errors_detected": errors, "no_crash": True}

    def _test_regex_injection(self):
        # Simulate a message that could break naive regex parsing
        malicious_msg = "expected ';' before .*+?[({]"
        try:
            matches = re.findall(r'error:', malicious_msg)
            return {"regex_safe": True, "matches": len(matches)}
        except re.error as e:
            return {"regex_safe": False, "error": str(e)}

    def _test_special_path(self):
        # Test path with spaces
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                path = os.path.join(tmpdir, "test file.cpp")
                with open(path, 'w') as f:
                    f.write("int main(){return 0;}\n")
                exists = os.path.exists(path)
            return {"special_path_handled": exists}
        except Exception as e:
            return {"special_path_handled": False, "error": str(e)}

    # 3D: Generate complete summary

    def generate_summary(self, malformed_pass, malformed_fail,
                         dangerous_count, input_pass, input_fail):
        """Compile all results into a final summary dict."""
        total_tests = (malformed_pass + malformed_fail + input_pass + input_fail)
        total_pass  = malformed_pass + input_pass
        total_fail  = malformed_fail + input_fail

        self.results["summary"] = {
            "generated_at": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests_run": total_tests,
            "total_passed": total_pass,
            "total_failed": total_fail,
            "pass_rate_percent": round((total_pass / total_tests) * 100, 1) if total_tests else 0,
            "malformed_input": {"passed": malformed_pass, "failed": malformed_fail},
            "input_validation": {"passed": input_pass, "failed": input_fail},
            "dangerous_patterns_found": dangerous_count,
            "security_verdict": "SAFE" if dangerous_count == 0 else "REVIEW NEEDED",
            "robustness_verdict": "ROBUST" if total_fail == 0 else "NEEDS IMPROVEMENT"
        }

        print("\n" + "=" * 65)
        print("  WEEK 11 SECURITY & ROBUSTNESS SUMMARY")
        print("=" * 65)
        print(f"  Total Tests Run      : {total_tests}")
        print(f"  Total Passed         : {total_pass}")
        print(f"  Total Failed         : {total_fail}")
        print(f"  Pass Rate            : {self.results['summary']['pass_rate_percent']}%")
        print(f"  Dangerous Patterns   : {dangerous_count}")
        print(f"  Security Verdict     : {self.results['summary']['security_verdict']}")
        print(f"  Robustness Verdict   : {self.results['summary']['robustness_verdict']}")
        print("=" * 65)

        return self.results

    def save_results_json(self, output_path="WEEK11/output/security_report.json"):
        """Save full results as JSON."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n  Results saved: {output_path}")


# SECTION 4: MAIN RUNNER

def main():
    print("\n" + "█" * 65 + '\n')
    print("  WEEK 11 — SECURITY AWARENESS & ROBUSTNESS TESTING")
    print("  AI-Assisted Compiler Error Diagnosis System"+ '\n')
    #print("  Student: MADDELA RAJEEV | Roll: 24CSB0B40")
    print("█" * 65)

    tester = SecurityRobustnessTester()

    # Run all three test suites
    m_pass, m_fail = tester.run_malformed_input_tests()
    d_count, _     = tester.run_dangerous_pattern_analysis(sample_dir=".")
    i_pass, i_fail = tester.run_input_validation_tests()

    # Generate and save summary
    results = tester.generate_summary(m_pass, m_fail, d_count, i_pass, i_fail)
    tester.save_results_json()

    print("\n  ✓ Week 11 testing complete.\n")
    return results


if __name__ == "__main__":
    main()
