


import subprocess  # Run external programs (gcc, g++)
import os          # Operating system functions
import csv         # Read/write CSV files
import re          # Regular expressions for pattern matching
from pathlib import Path  # Modern file path handling


class ErrorCollector:
    
    def __init__(self, sample_dir, output_csv):

        self.sample_dir = sample_dir    # Where sample programs are
        self.output_csv = output_csv    # Where to save results
        self.errors = []                # List to store all errors
    
    
   
    def compile_and_capture(self, filepath):
       
        # Choosing compiler based on file extension
        ext = filepath.suffix
        compiler = 'gcc' if ext == '.c' else 'g++'
        
        try:
            # Runing the compiler
            result = subprocess.run(
                [compiler, '-c', str(filepath), '-o', '/dev/null'],
                capture_output=True,  # Captures stdout and stderr
                text=True,            # Returns output as string
                timeout=5             # Killed if takes more than 5 seconds
            )
            
            # if compilation failed
            if result.returncode != 0:
                return result.stderr  # Returnss error messages
            else:
                return None  # implies Compilation is successful
                
        except subprocess.TimeoutExpired:  # for timeout case
            return "TIMEOUT"
            
        except Exception as e: # other error cases
            return f"ERROR: {str(e)}"
    

    def parse_error_message(self, error_output, filepath):
      
        # Regular expression to match GCC error format
        pattern = r'([^:]+):(\d+):(\d+):\s*(error|warning):\s*(.+)'
        
        # Find all error messages in the output
        matches = re.finditer(pattern, error_output, re.MULTILINE)
        
        # Process each error found
        for match in matches:
            file, line, col, err_type, message = match.groups()
            
            # Store structured error information
            self.errors.append({
                'source_file': filepath.name,
                'error_category': self.infer_category(filepath.name),
                'line_number': int(line),
                'column_number': int(col),
                'error_type': err_type,
                'error_message': message.strip(),
                'full_output': error_output
            })
    
    
    def infer_category(self, filename):
       
        # Mapping of filename patterns to categories
        categories = {
            'missing_semicolon': 'Missing Semicolon',
            'undeclared': 'Undeclared Variable',
            'unmatched_braces': 'Unmatched Braces',
            'unmatched_parens': 'Unmatched Parentheses',
            'type_mismatch': 'Type Mismatch',
            'missing_return': 'Missing Return Statement',
            'invalid_decl': 'Invalid Syntax in Declarations',
            'missing_header': 'Missing Header Include'
        }
        
        # Check if filename contains any category keyword
        for key, category in categories.items():
            if key in filename.lower():
                return category
        
        return 'Unknown'
    
        
    def collect_all_errors(self):
        """
        Process all C/C++ files in the sample directory.
        
        Steps:
        1. Find all .c and .cpp files
        2. Compile each one
        3. Parse and store error messages
        """
        
        # Find all C and C++ files
        sample_files = (
            list(Path(self.sample_dir).glob('*.c')) + 
            list(Path(self.sample_dir).glob('*.cpp'))
        )
        
        print(f"\n{'='*60}")
        print(f"STARTING ERROR COLLECTION")
        print(f"{'='*60}")
        print(f"Found {len(sample_files)} sample programs\n")
        
        # Process each file
        for i, filepath in enumerate(sample_files, 1):
            print(f"[{i}/{len(sample_files)}] Processing: {filepath.name}")
            
            error_output = self.compile_and_capture(filepath)
            
            if error_output:  # if anystring is returned by compile and capture function
                self.parse_error_message(error_output, filepath)
                print(f"     ✓ Errors captured")
            else: # if no errors
                print(f"     ✗ No errors (compiled successfully)")
        
        print(f"\n{'='*60}")
        print(f"Total Errors Collected: {len(self.errors)}")
        print(f"{'='*60}\n")
    
    
    def save_to_csv(self):
        
        if not self.errors:
            print("⚠ No errors to save!")
            return
        
        # Define CSV column headers
        fieldnames = [
            'source_file', 
            'error_category', 
            'line_number', 
            'column_number', 
            'error_type', 
            'error_message', 
            'full_output'
        ]
        
        # Write to CSV file
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.errors)
        
        print(f"✓ Saved to: {self.output_csv}")
    
    
    def generate_report(self):
        
        from collections import Counter
        
        # Count errors by category
        categories = Counter(e['error_category'] for e in self.errors)
        
        print(f"\n{'='*60}")
        print("ERROR COLLECTION REPORT")
        print(f"{'='*60}")
        print(f"Total Errors: {len(self.errors)}")
        print(f"\nBreakdown by Category:")
        print(f"{'-'*60}")
        
        for category, count in categories.most_common():
            percentage = (count / len(self.errors)) * 100
            print(f"  {category:.<45} {count:>3} ({percentage:>5.1f}%)")
        
        print(f"{'='*60}\n")


# MAIN 

if __name__ == "__main__":
    
    # Create error collector
    collector = ErrorCollector(
        sample_dir='sample_programs',
        output_csv='output/collected_errors.csv'
    )
    
    # Run collection process
    collector.collect_all_errors()
    collector.save_to_csv()
    collector.generate_report()
    
    print("="*60 + "\n")
    print("✓ Error collection complete!")
    print("="*60 + "\n")