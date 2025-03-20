import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
import tempfile
import random
import time
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample coding questions
QUESTIONS = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {
                "input": {"nums": [2, 7, 11, 15], "target": 9},
                "output": [0, 1],
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": {"nums": [3, 2, 4], "target": 6},
                "output": [1, 2],
                "explanation": "Because nums[1] + nums[2] == 6, we return [1, 2]."
            },
            {
                "input": {"nums": [3, 3], "target": 6},
                "output": [0, 1],
                "explanation": "Because nums[0] + nums[1] == 6, we return [0, 1]."
            }
        ],
        "constraints": [
            "2 <= nums.length <= 104",
            "-109 <= nums[i] <= 109",
            "-109 <= target <= 109",
            "Only one valid answer exists."
        ],
        "function_signature": {
            "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your code here\n    }\n}",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    std::vector<int> twoSum(std::vector<int>& nums, int target) {\n        // Your code here\n    }\n};",
            "python": "def two_sum(nums, target):\n    # Your code here\n    pass"
        }
    },
    {
        "id": 2,
        "title": "Palindrome Number",
        "difficulty": "Easy",
        "description": "Given an integer x, return true if x is a palindrome, and false otherwise. A palindrome is a number that reads the same backward as forward.",
        "examples": [
            {
                "input": {"x": 121},
                "output": True,
                "explanation": "121 reads as 121 from left to right and from right to left."
            },
            {
                "input": {"x": -121},
                "output": False,
                "explanation": "From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome."
            },
            {
                "input": {"x": 10},
                "output": False,
                "explanation": "Reads 01 from right to left. Therefore it is not a palindrome."
            }
        ],
        "constraints": [
            "-231 <= x <= 231 - 1"
        ],
        "function_signature": {
            "java": "class Solution {\n    public boolean isPalindrome(int x) {\n        // Your code here\n    }\n}",
            "cpp": "class Solution {\npublic:\n    bool isPalindrome(int x) {\n        // Your code here\n    }\n};",
            "python": "def is_palindrome(x):\n    # Your code here\n    pass"
        }
    },
    {
        "id": 3,
        "title": "Reverse String",
        "difficulty": "Easy",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s. You must do this by modifying the input array in-place with O(1) extra memory.",
        "examples": [
            {
                "input": {"s": ["h", "e", "l", "l", "o"]},
                "output": ["o", "l", "l", "e", "h"],
                "explanation": "Reverse the string 'hello' to get 'olleh'."
            },
            {
                "input": {"s": ["H", "a", "n", "n", "a", "h"]},
                "output": ["h", "a", "n", "n", "a", "H"],
                "explanation": "Reverse the string 'Hannah' to get 'hannaH'."
            }
        ],
        "constraints": [
            "1 <= s.length <= 105",
            "s[i] is a printable ascii character."
        ],
        "function_signature": {
            "java": "class Solution {\n    public void reverseString(char[] s) {\n        // Your code here\n    }\n}",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    void reverseString(std::vector<char>& s) {\n        // Your code here\n    }\n};",
            "python": "def reverse_string(s):\n    # Your code here\n    pass"
        }
    }
]

# Wrapper code for testing solutions
WRAPPERS = {
    "java": {
        "two_sum": """import java.util.Arrays;

%s

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] nums = %s;
        int target = %d;
        int[] result = solution.twoSum(nums, target);
        System.out.println(Arrays.toString(result));
    }
}
""",
        "is_palindrome": """
%s

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int x = %d;
        boolean result = solution.isPalindrome(x);
        System.out.println(result);
    }
}
""",
        "reverse_string": """import java.util.Arrays;

%s

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        char[] s = %s;
        solution.reverseString(s);
        System.out.println(Arrays.toString(s));
    }
}
"""
    },
    "cpp": {
        "two_sum": """#include <iostream>
#include <vector>

%s

int main() {
    std::vector<int> nums = %s;
    int target = %d;
    Solution solution;
    std::vector<int> result = solution.twoSum(nums, target);
    std::cout << "[";
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << result[i];
    }
    std::cout << "]" << std::endl;
    return 0;
}
""",
        "is_palindrome": """#include <iostream>

%s

int main() {
    int x = %d;
    Solution solution;
    bool result = solution.isPalindrome(x);
    std::cout << (result ? "true" : "false") << std::endl;
    return 0;
}
""",
        "reverse_string": """#include <iostream>
#include <vector>

%s

int main() {
    std::vector<char> s = %s;
    Solution solution;
    solution.reverseString(s);
    std::cout << "[";
    for (size_t i = 0; i < s.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << "'" << s[i] << "'";
    }
    std::cout << "]" << std::endl;
    return 0;
}
"""
    },
    "python": {
        "two_sum": """
%s

nums = %s
target = %d
result = two_sum(nums, target)
print(result)
""",
        "is_palindrome": """
%s

x = %d
result = is_palindrome(x)
print(result)
""",
        "reverse_string": """
%s

s = %s
reverse_string(s)
print(s)
"""
    }
}

# Route to get a random question
@app.route('/get_question', methods=['GET'])
def get_question():
    question = random.choice(QUESTIONS)
    return jsonify(question)

# Function to run code with the appropriate compiler/interpreter
def run_code(language, code, input_data=None):
    if language == "java":
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".java", delete=False) as temp:
            temp.write(code.encode())
            temp_path = temp.name
        
        # Compile Java code
        compile_result = subprocess.run(["javac", temp_path], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return {"passed": False, "error": compile_result.stderr}
        
        # Run Java code
        class_path = os.path.dirname(temp_path)
        run_result = subprocess.run(["java", "-cp", class_path, "Main"], capture_output=True, text=True)
        
        # Clean up
        os.unlink(temp_path)
        try:
            os.unlink(os.path.join(class_path, "Main.class"))
        except:
            pass  # Ignore if file doesn't exist
        
        if run_result.returncode != 0:
            return {"passed": False, "error": run_result.stderr}
        
        return {"passed": True, "output": run_result.stdout.strip()}
    
    elif language == "cpp":
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp:
            temp.write(code.encode())
            temp_path = temp.name
        
        # Compile C++ code
        output_path = temp_path + ".out"
        compile_result = subprocess.run(["g++", temp_path, "-o", output_path], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return {"passed": False, "error": compile_result.stderr}
        
        # Run C++ code
        run_result = subprocess.run([output_path], capture_output=True, text=True)
        
        # Clean up
        os.unlink(temp_path)
        try:
            os.unlink(output_path)
        except:
            pass  # Ignore if file doesn't exist
        
        if run_result.returncode != 0:
            return {"passed": False, "error": run_result.stderr}
        
        return {"passed": True, "output": run_result.stdout.strip()}
    
    elif language == "python":
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
            temp.write(code.encode())
            temp_path = temp.name
        
        # Run Python code
        run_result = subprocess.run(["python", temp_path], capture_output=True, text=True)
        
        # Clean up
        os.unlink(temp_path)
        
        if run_result.returncode != 0:
            return {"passed": False, "error": run_result.stderr}
        
        return {"passed": True, "output": run_result.stdout.strip()}
    
    else:
        return {"passed": False, "error": "Unsupported language"}

# Helper to format input data for wrappers
def format_input_data(language, data_type, data):
    if language == "java":
        if data_type == "array":
            return "{" + ", ".join(map(str, data)) + "}"
        elif data_type == "char_array":
            return "new char[]{" + ", ".join(f"'{c}'" for c in data) + "}"
        return str(data)
    elif language == "cpp":
        if data_type == "array":
            return "{" + ", ".join(map(str, data)) + "}"
        elif data_type == "char_array":
            return "{" + ", ".join(f"'{c}'" for c in data) + "}"
        return str(data)
    elif language == "python":
        if data_type == "array":
            return str(data)
        elif data_type == "char_array":
            return str([c for c in data])
        return str(data)

# Route to run a test case
@app.route('/run_test_case', methods=['POST'])
def run_test_case():
    data = request.json
    language = data.get('language')
    code = data.get('code')
    test_case = data.get('test_case')
    
    if not all([language, code, test_case]):
        return jsonify({"passed": False, "error": "Missing required parameters"}), 400
    
    # Find the question based on test case
    question_title = None
    for question in QUESTIONS:
        if any(example == test_case for example in question.get('examples', [])):
            question_title = question['title'].lower().replace(' ', '_')
            break
    
    if not question_title:
        return jsonify({"passed": False, "error": "Invalid test case"}), 400
    
    # Format the input data according to the question
    input_data = test_case['input']
    wrapped_code = ""
    
    if question_title == "two_sum":
        nums_str = format_input_data(language, "array", input_data["nums"])
        target = input_data["target"]
        wrapped_code = WRAPPERS[language]["two_sum"] % (code, nums_str, target)
    elif question_title == "palindrome_number":
        x = input_data["x"]
        wrapped_code = WRAPPERS[language]["is_palindrome"] % (code, x)
    elif question_title == "reverse_string":
        s_str = format_input_data(language, "char_array", input_data["s"])
        wrapped_code = WRAPPERS[language]["reverse_string"] % (code, s_str)
    else:
        return jsonify({"passed": False, "error": "Unsupported question type"}), 400
    
    # Run the code
    result = run_code(language, wrapped_code)
    
    # Check if output matches expected output
    if result["passed"]:
        expected_output = str(test_case.get('output')).replace("'", '"').lower()
        actual_output = result["output"].replace("'", '"').lower()
        
        # Normalize the outputs for comparison
        try:
            expected_json = json.loads(expected_output) if expected_output[0] in "[{" else expected_output
            actual_json = json.loads(actual_output) if actual_output[0] in "[{" else actual_output
            result["passed"] = expected_json == actual_json
            result["expected"] = test_case.get('output')
            result["actual"] = actual_output
        except:
            # If JSON parsing fails, do a string comparison
            result["passed"] = expected_output.strip() == actual_output.strip()
            result["expected"] = test_case.get('output')
            result["actual"] = result["output"]
    
    return jsonify(result)

# Route to submit a solution
@app.route('/submit_solution', methods=['POST'])
def submit_solution():
    data = request.json
    language = data.get('language')
    code = data.get('code')
    description = data.get('question_description')
    examples = data.get('examples')
    
    if not all([language, code, description, examples]):
        return jsonify({"success": False, "error": "Missing required parameters"}), 400
    
    # Find the question based on description
    question = None
    for q in QUESTIONS:
        if q['description'] == description:
            question = q
            break
    
    if not question:
        return jsonify({"success": False, "error": "Invalid question"}), 400
    
    # Run all test cases
    all_passed = True
    test_results = []
    
    for example in examples:
        # Format the input data according to the question
        input_data = example['input']
        wrapped_code = ""
        
        if question['title'].lower() == "two sum":
            nums_str = format_input_data(language, "array", input_data["nums"])
            target = input_data["target"]
            wrapped_code = WRAPPERS[language]["two_sum"] % (code, nums_str, target)
        elif question['title'].lower() == "palindrome number":
            x = input_data["x"]
            wrapped_code = WRAPPERS[language]["is_palindrome"] % (code, x)
        elif question['title'].lower() == "reverse string":
            s_str = format_input_data(language, "char_array", input_data["s"])
            wrapped_code = WRAPPERS[language]["reverse_string"] % (code, s_str)
        else:
            return jsonify({"success": False, "error": "Unsupported question type"}), 400
        
        # Run the code
        result = run_code(language, wrapped_code)
        
        # Check if output matches expected output
        if result["passed"]:
            expected_output = str(example.get('output')).replace("'", '"').lower()
            actual_output = result["output"].replace("'", '"').lower()
            
            # Try to normalize the outputs for comparison
            try:
                expected_json = json.loads(expected_output) if expected_output[0] in "[{" else expected_output
                actual_json = json.loads(actual_output) if actual_output[0] in "[{" else actual_output
                result["passed"] = expected_json == actual_json
            except:
                # If JSON parsing fails, do a string comparison
                result["passed"] = expected_output.strip() == actual_output.strip()
        
        all_passed = all_passed and result["passed"]
        test_results.append(result)
    
    return jsonify({
        "success": all_passed,
        "test_results": test_results,
        "message": "All tests passed!" if all_passed else "Some tests failed."
    })

# Home route
@app.route('/')
def home():
    return "Coding Challenge Backend is running!"

# Status endpoint for debugging
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ok',
        'environment': os.environ.get('FLASK_ENV', 'production'),
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)