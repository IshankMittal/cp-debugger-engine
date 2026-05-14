from flask import Flask, request, jsonify, render_template
import requests
import subprocess
import tempfile
import os
import re

app = Flask(__name__)

LLAMA_URL = "http://localhost:8080/v1/completions"
MODEL_NAME = "deepseek-coder-6.7b-instruct-q4_k_m.gguf"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/debug", methods=["POST"])
def debug_code():
    try:
        data = request.json or {}
        code = data.get("code", "")
        fix_mode = data.get("fix", False)

        # -----------------------
        # REAL COMPILER CHECK
        # -----------------------

        with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as tmp:
            tmp.write(code.encode())
            tmp_path = tmp.name

        compile_process = subprocess.run(
            ["g++", tmp_path],
            capture_output=True,
            text=True
        )

        # these lines are used to remove unnessary details in output 
        '''
        before: return 0, unnessary space got add in output, looks like this
        
        Compiler Errors:
        C:\Users\ISHANK\AppData\Local\Temp\tmp9pg_307c.cpp: In function 'int main()':
        C:\Users\ISHANK\AppData\Local\Temp\tmp9pg_307c.cpp:5:20: error: expected ';' before 'return'
            5 |     cout << "Hello"
            |                    ^
            |                    ;
            6 |     return 0;
            |     ~~~~~~          

        after: clean output, looks like this
        
        In function 'int main()':
        5:20: error: expected ';' before '}' token
            5 |     cout << "Hello"
            |                    ^
            |                    ;   
        
        
        basically to cleaner output
        '''
        compiler_errors = compile_process.stderr
        
        compiler_errors = re.sub(
            r"C:.*?\.cpp:",
            "",
            compiler_errors
        )
        
        os.remove(tmp_path)
        
        compiler_errors = re.sub(
            r".*return 0;.*\n?",
            "",
            compiler_errors
        )
        
        compiler_errors = re.sub(
            r"\n\s*\d+\s*\|\s*}\s*\n\s*\|\s*~?",
            "",
            compiler_errors
        )

        # If compile error and fix_mode OFF → show compiler error
        if compiler_errors and not fix_mode:
            return jsonify({
                "analysis": f"Compiler Errors:\n\n{compiler_errors}"
            })

        # -----------------------
        # TASK DECISION
        # -----------------------

        if compiler_errors and fix_mode:
            task = f"""
The compiler produced the following errors:

{compiler_errors}

Fix the code completely.
Output ONLY valid C++ code.
"""
            max_tokens = 256

        elif fix_mode:
            task = """
Provide FULL corrected and optimized C++ code.
Output ONLY valid C++ code.
"""
            max_tokens = 256

        else:
            task = """
Analyze:
- Logical mistakes
- Edge cases
- Time complexity
- Improvements

Do NOT rewrite full code.
"""
            max_tokens = 200

        # -----------------------
        # BUILD PROMPT
        # -----------------------

        prompt = f"""[INST]
You are an elite competitive programming expert.

{task}

Code:
{code}
[/INST]"""

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.0,
            "stop": ["</s>", "[INST]"]
        }

        response = requests.post(LLAMA_URL, json=payload)

        if response.status_code != 200:
            return jsonify({
                "analysis": f"LLM Error:\n{response.text}"
            })

        result = response.json()

        if "choices" not in result:
            return jsonify({
                "analysis": f"Unexpected LLM response:\n{result}"
            })

        output_text = result["choices"][0]["text"]

        # -----------------------
        # CLEAN OUTPUT
        # -----------------------

        if fix_mode:
            # Extract only C++ program
            match = re.search(r"#include[\s\S]*?\n}", output_text)
            if match:
                output_text = match.group(0)
            else:
                match = re.search(r"int\s+main[\s\S]*?\n}", output_text)
                if match:
                    output_text = match.group(0)
                else:
                    output_text = "Could not extract valid C++ code."
        else:
            # Clean tags for analysis mode
            for tag in [
                "[RESP]", "[/RESP]",
                "[SOLUTION]", "[/SOLUTION]",
                "[SOL]", "[/SOL]",
                "[WRAP]", "[/WRAP]",
                "[ANSWER]", "[/ANSWER]",
                "[OUT]", "[/OUT]",
                "[EXP]", "[/EXP]",
                "[RSLT]", "[/RSLT]"
            ]:
                output_text = output_text.replace(tag, "")

            output_text = output_text.replace("```cpp", "")
            output_text = output_text.replace("```", "")

        output_text = output_text.strip()

        # 🔥 THIS WAS MISSING BEFORE
        return jsonify({"analysis": output_text})

    except Exception as e:
        return jsonify({"analysis": f"Server Error:\n{str(e)}"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)