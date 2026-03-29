# fix_suggestions.py

def get_fix_suggestion(error_label):

    fixes = {

        "Missing Semicolon": {
            "explanation": "A statement must end with a semicolon (;).",
            "fix": [
                "Go to the line mentioned in error",
                "Add ';' at the end"
            ],
            "example": {
                "wrong": "int x = 10",
                "correct": "int x = 10;"
            }
        },

        "Undeclared Variable": {
            "explanation": "Variable is used before declaration.",
            "fix": [
                "Declare the variable before using it",
                "Check spelling of variable name"
            ],
            "example": {
                "wrong": "x = 5;",
                "correct": "int x = 5;"
            }
        },

        "Unmatched Braces": {
            "explanation": "Curly braces {} are not balanced.",
            "fix": [
                "Check opening '{' and closing '}'",
                "Ensure all blocks are closed"
            ],
            "example": {
                "wrong": "if(x>0){ printf(\"Hi\");",
                "correct": "if(x>0){ printf(\"Hi\"); }"
            }
        },

        "Unmatched Parentheses": {
            "explanation": "Parentheses () are not balanced.",
            "fix": [
                "Check '(' and ')'",
                "Fix missing parenthesis"
            ],
            "example": {
                "wrong": "if(x > 5 {",
                "correct": "if(x > 5) {"
            }
        },

        "Type Mismatch": {
            "explanation": "Wrong data type used in assignment.",
            "fix": [
                "Ensure correct data type is used",
                "Convert type if needed"
            ],
            "example": {
                "wrong": "int x = \"Hello\";",
                "correct": "string x = \"Hello\";"
            }
        },

        "Missing Return Statement": {
            "explanation": "Function must return a value.",
            "fix": [
                "Add return statement",
                "Ensure all paths return value"
            ],
            "example": {
                "wrong": "int func() { }",
                "correct": "int func() { return 0; }"
            }
        },

        "Invalid Syntax in Declarations": {
            "explanation": "Incorrect declaration syntax.",
            "fix": [
                "Check datatype spelling",
                "Fix declaration format"
            ],
            "example": {
                "wrong": "intger x = 5;",
                "correct": "int x = 5;"
            }
        },

        "Missing Header Include": {
            "explanation": "Required header file is missing.",
            "fix": [
                "Add appropriate #include",
                "Check required libraries"
            ],
            "example": {
                "wrong": "printf(\"Hi\");",
                "correct": "#include <stdio.h>\nprintf(\"Hi\");"
            }
        }
    }

    return fixes.get(error_label, {
        "explanation": "Unknown error",
        "fix": ["Check code manually"],
        "example": {"wrong": "-", "correct": "-"}
    })